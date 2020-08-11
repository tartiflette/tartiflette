from functools import partial
from typing import Dict, List, Optional, Set, Tuple, Union

from tartiflette.execution.collect import get_field_entry_key
from tartiflette.language.ast import (
    FieldNode,
    FragmentSpreadNode,
    InlineFragmentNode,
)
from tartiflette.language.utils import get_wrapped_named_type
from tartiflette.types.helpers.definition import (
    is_interface_type,
    is_leaf_type,
    is_list_type,
    is_non_null_type,
    is_object_type,
)
from tartiflette.utils.errors import (
    graphql_error_from_nodes as raw_graphql_error_from_nodes,
)
from tartiflette.utils.type_from_ast import schema_type_from_ast
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("OverlappingFieldsCanBeMergedRule",)


graphql_error_from_nodes = partial(
    raw_graphql_error_from_nodes,
    extensions={
        "spec": "June 2018",
        "rule": "5.3.2",
        "tag": "field-selection-merging",
        "details": (
            "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging"
        ),
    },
)

ConflictReasonMessage = Union[str, List["ConflictReason"]]
ConflictReason = Tuple[str, "ConflictReasonMessage"]
Conflict = Tuple["ConflictReason", List["FieldNode"], List["FieldNode"]]
NodeAndDef = Tuple[
    "GraphQLCompositeType", "FieldNode", Optional["GraphQLField"]
]
NodeAndDefCollection = Dict[str, List["NodeAndDef"]]


def _reason_message(reason: ConflictReasonMessage) -> str:
    """
    Format the error message related to conflicts found.
    :param reason: list of conflict reason
    :type reason: ConflictReasonMessage
    :return: the formatted error message
    :rtype: str
    """
    return (
        reason
        if not isinstance(reason, list)
        else " and ".join(
            [
                f"subfields < {response_name} > conflict because "
                f"{_reason_message(sub_reason)}"
                for response_name, sub_reason in reason
            ]
        )
    )


class OverlappingFieldsCanBeMergedRule(ASTValidationRule):
    """
    A selection set is only valid if all fields (including spreading any
    fragments) either correspond to distinct response names or can be
    merged without ambiguity.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)

        # A memoization for when two fragments are compared "between" each
        # other forconflicts. Two fragments may be compared many times, so
        # memoizing this can dramatically improve the performance of this
        # validator.
        self._compared_fragment_pairs = PairSet()

        # A cache for the "field map" and list of fragment names found in any
        # given selection set. Selection sets may be asked for this information
        # multiple times, so this improves the performance of this validator.
        self._cached_fields_and_fragment_names = {}

    def enter_SelectionSet(  # pylint: disable=invalid-name
        self,
        node: "SelectionSetNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that fields can be merged without ambiguity.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: SelectionSetNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        conflicts = _find_conflicts_within_selection_set(
            self.context,
            self._cached_fields_and_fragment_names,
            self._compared_fragment_pairs,
            self.context.get_parent_type(),
            node,
        )

        for (response_name, reason), fields1, fields2 in conflicts:
            self.context.report_error(
                graphql_error_from_nodes(
                    f"Fields < {response_name} > conflict because "
                    f"{_reason_message(reason)}. Use different aliases on the "
                    "fields to fetch both if this was intentional.",
                    nodes=fields1 + fields2,
                )
            )


def _find_conflicts_within_selection_set(
    context: "ASTValidationContext",
    cached_fields_and_fragment_names: Dict[
        int, Tuple[NodeAndDefCollection, List[str]]
    ],
    compared_fragment_pairs: "PairSet",
    parent_type: Optional["GraphQLCompositeType"],
    selection_set: "SelectionSetNode",
) -> List[Conflict]:
    """
    Find all conflicts found "within" a selection set.
    :param context: context forwarded to the validation rule
    :param cached_fields_and_fragment_names: store fields and fragment names
    :param compared_fragment_pairs: a PairSet instance
    :param parent_type: current GraphQL parent type
    :param selection_set: current visited SelectionSetNode
    :type context: ASTValidationContext
    :type cached_fields_and_fragment_names: Dict[
        int, Tuple[NodeAndDefCollection, List[str]]
    ]
    :type compared_fragment_pairs: PairSet
    :type parent_type: Optional[GraphQLCompositeType]
    :type selection_set: SelectionSetNode
    :return: all conflicts found "within" the selection set
    :rtype: List[Conflict]
    """
    conflicts = []

    field_map, fragment_names = _get_fields_and_fragment_names(
        context, cached_fields_and_fragment_names, parent_type, selection_set
    )

    _collect_conflicts_within(
        context,
        conflicts,
        cached_fields_and_fragment_names,
        compared_fragment_pairs,
        field_map,
    )

    if fragment_names:
        for index, fragment_name in enumerate(fragment_names):
            _collect_conflicts_between_fields_and_fragment(
                context,
                conflicts,
                cached_fields_and_fragment_names,
                compared_fragment_pairs,
                False,
                field_map,
                fragment_name,
            )

            for other_fragment_name in fragment_names[index + 1 :]:
                _collect_conflicts_between_fragments(
                    context,
                    conflicts,
                    cached_fields_and_fragment_names,
                    compared_fragment_pairs,
                    False,
                    fragment_name,
                    other_fragment_name,
                )
    return conflicts


def _collect_conflicts_between_fields_and_fragment(
    context: "ASTValidationContext",
    conflicts: List[Conflict],
    cached_fields_and_fragment_names: Dict[
        int, Tuple[NodeAndDefCollection, List[str]]
    ],
    compared_fragment_pairs: "PairSet",
    are_mutually_exclusive: bool,
    field_map: NodeAndDefCollection,
    fragment_name: str,
) -> None:
    """
    Collect all conflicts found between a set of fields and a fragment
    reference.
    :param context: context forwarded to the validation rule
    :param conflicts: conflicts found
    :param cached_fields_and_fragment_names: store fields and fragment names
    :param compared_fragment_pairs: a PairSet instance
    :param are_mutually_exclusive: whether or not they are mutually exclusive
    :param field_map: collection of node and definitions
    :param fragment_name: name of the visited fragment
    :type context: ASTValidationContext
    :type conflicts: List[Conflict]
    :type cached_fields_and_fragment_names: Dict[
        int, Tuple[NodeAndDefCollection, List[str]]
    ]
    :type compared_fragment_pairs: PairSet
    :type are_mutually_exclusive: bool
    :type field_map: NodeAndDefCollection
    :type fragment_name: str
    """
    fragment = context.get_fragment(fragment_name)
    if not fragment:
        return None

    field_map_2, fragment_names_2 = _get_referenced_fields_and_fragment_names(
        context, cached_fields_and_fragment_names, fragment
    )

    if field_map is field_map_2:
        return None

    _collect_conflicts_between(
        context,
        conflicts,
        cached_fields_and_fragment_names,
        compared_fragment_pairs,
        are_mutually_exclusive,
        field_map,
        field_map_2,
    )

    for fragment_name_2 in fragment_names_2:
        _collect_conflicts_between_fields_and_fragment(
            context,
            conflicts,
            cached_fields_and_fragment_names,
            compared_fragment_pairs,
            are_mutually_exclusive,
            field_map,
            fragment_name_2,
        )

    return None


def _collect_conflicts_between_fragments(
    context: "ASTValidationContext",
    conflicts: List[Conflict],
    cached_fields_and_fragment_names: Dict[
        int, Tuple[NodeAndDefCollection, List[str]]
    ],
    compared_fragment_pairs: "PairSet",
    are_mutually_exclusive: bool,
    fragment_name_1: str,
    fragment_name_2: str,
) -> None:
    """
    Collect all conflicts found between two fragments.
    :param context: context forwarded to the validation rule
    :param conflicts: conflicts found
    :param cached_fields_and_fragment_names: store fields and fragment names
    :param compared_fragment_pairs: a PairSet instance
    :param are_mutually_exclusive: whether or not they are mutually exclusive
    :param fragment_name_1: name of the first fragment
    :param fragment_name_2: name of the second fragment
    :type context: ASTValidationContext
    :type conflicts: List[Conflict]
    :type cached_fields_and_fragment_names: Dict[
        int, Tuple[NodeAndDefCollection, List[str]]
    ]
    :type compared_fragment_pairs: PairSet
    :type are_mutually_exclusive: bool
    :type fragment_name_1: str
    :type fragment_name_2: str
    """
    if fragment_name_1 == fragment_name_2:
        return None

    if compared_fragment_pairs.has(
        fragment_name_1, fragment_name_2, are_mutually_exclusive
    ):
        return None

    compared_fragment_pairs.add(
        fragment_name_1, fragment_name_2, are_mutually_exclusive
    )

    fragment_1 = context.get_fragment(fragment_name_1)
    fragment_2 = context.get_fragment(fragment_name_2)
    if not fragment_1 or not fragment_2:
        return None

    field_map_1, fragment_names_1 = _get_referenced_fields_and_fragment_names(
        context, cached_fields_and_fragment_names, fragment_1,
    )
    field_map_2, fragment_names_2 = _get_referenced_fields_and_fragment_names(
        context, cached_fields_and_fragment_names, fragment_2,
    )

    _collect_conflicts_between(
        context,
        conflicts,
        cached_fields_and_fragment_names,
        compared_fragment_pairs,
        are_mutually_exclusive,
        field_map_1,
        field_map_2,
    )

    for nested_fragment_name_2 in fragment_names_2:
        _collect_conflicts_between_fragments(
            context,
            conflicts,
            cached_fields_and_fragment_names,
            compared_fragment_pairs,
            are_mutually_exclusive,
            fragment_name_1,
            nested_fragment_name_2,
        )

    for nested_fragment_name_1 in fragment_names_1:
        _collect_conflicts_between_fragments(
            context,
            conflicts,
            cached_fields_and_fragment_names,
            compared_fragment_pairs,
            are_mutually_exclusive,
            nested_fragment_name_1,
            fragment_name_2,
        )

    return None


def _find_conflicts_between_sub_selection_sets(
    context: "ASTValidationContext",
    cached_fields_and_fragment_names: Dict[
        int, Tuple[NodeAndDefCollection, List[str]]
    ],
    compared_fragment_pairs: "PairSet",
    are_mutually_exclusive: bool,
    parent_type_1: Optional["GraphQLCompositeType"],
    selection_set_1: "SelectionSetNode",
    parent_type_2: Optional["GraphQLCompositeType"],
    selection_set_2: "SelectionSetNode",
) -> List[Conflict]:
    """
    Find all conflicts found between two selection sets.

    Called when determining if conflicts exist between the sub-fields
    of two overlapping fields.
    :param context: context forwarded to the validation rule
    :param cached_fields_and_fragment_names: store fields and fragment names
    :param compared_fragment_pairs: a PairSet instance
    :param are_mutually_exclusive: whether or not they are mutually exclusive
    :param parent_type_1: the GraphQL type instance of the first parent
    :param selection_set_1: the first SelectionSetNode instance
    :param parent_type_2: the GraphQL type instance of the second parent
    :param selection_set_2: the second SelectionSetNode instance
    :type context: ASTValidationContext
    :type cached_fields_and_fragment_names: Dict[
        int, Tuple[NodeAndDefCollection, List[str]]
    ]
    :type compared_fragment_pairs: PairSet
    :type are_mutually_exclusive: bool
    :type parent_type_1: Optional[GraphQLCompositeType]
    :type selection_set_1: SelectionSetNode
    :type parent_type_2: Optional[GraphQLCompositeType]
    :type selection_set_2: SelectionSetNode
    :return: all conflicts found between two selection sets
    :rtype: List[Conflict]
    """
    conflicts = []

    field_map_1, fragment_names_1 = _get_fields_and_fragment_names(
        context,
        cached_fields_and_fragment_names,
        parent_type_1,
        selection_set_1,
    )
    field_map_2, fragment_names_2 = _get_fields_and_fragment_names(
        context,
        cached_fields_and_fragment_names,
        parent_type_2,
        selection_set_2,
    )

    _collect_conflicts_between(
        context,
        conflicts,
        cached_fields_and_fragment_names,
        compared_fragment_pairs,
        are_mutually_exclusive,
        field_map_1,
        field_map_2,
    )

    if fragment_names_2:
        for fragment_name_2 in fragment_names_2:
            _collect_conflicts_between_fields_and_fragment(
                context,
                conflicts,
                cached_fields_and_fragment_names,
                compared_fragment_pairs,
                are_mutually_exclusive,
                field_map_1,
                fragment_name_2,
            )

    if fragment_names_1:
        for fragment_name_1 in fragment_names_1:
            _collect_conflicts_between_fields_and_fragment(
                context,
                conflicts,
                cached_fields_and_fragment_names,
                compared_fragment_pairs,
                are_mutually_exclusive,
                field_map_2,
                fragment_name_1,
            )

    for fragment_name_1 in fragment_names_1:
        for fragment_name_2 in fragment_names_2:
            _collect_conflicts_between_fragments(
                context,
                conflicts,
                cached_fields_and_fragment_names,
                compared_fragment_pairs,
                are_mutually_exclusive,
                fragment_name_1,
                fragment_name_2,
            )
    return conflicts


def _collect_conflicts_within(
    context: "ASTValidationContext",
    conflicts: List[Conflict],
    cached_fields_and_fragment_names: Dict[
        int, Tuple[NodeAndDefCollection, List[str]]
    ],
    compared_fragment_pairs: "PairSet",
    field_map: NodeAndDefCollection,
) -> None:
    """
    Collect all Conflicts "within" one collection of fields.
    :param context: context forwarded to the validation rule
    :param conflicts: conflicts found
    :param cached_fields_and_fragment_names: store fields and fragment names
    :param compared_fragment_pairs: a PairSet instance
    :param field_map: collection of node and definitions
    :type context: ASTValidationContext
    :type conflicts: List[Conflict]
    :type cached_fields_and_fragment_names: Dict[
        int, Tuple[NodeAndDefCollection, List[str]]
    ]
    :type compared_fragment_pairs: PairSet
    :type field_map: NodeAndDefCollection
    """
    for response_name, fields in field_map.items():
        if len(fields) > 1:
            for index, field in enumerate(fields):
                for other_field in fields[index + 1 :]:
                    conflict = _find_conflict(
                        context,
                        cached_fields_and_fragment_names,
                        compared_fragment_pairs,
                        False,
                        response_name,
                        field,
                        other_field,
                    )
                    if conflict:
                        conflicts.append(conflict)


def _collect_conflicts_between(
    context: "ASTValidationContext",
    conflicts: List[Conflict],
    cached_fields_and_fragment_names: Dict[
        int, Tuple[NodeAndDefCollection, List[str]]
    ],
    compared_fragment_pairs: "PairSet",
    parent_fields_are_mutually_exclusive: bool,
    field_map_1: NodeAndDefCollection,
    field_map_2: NodeAndDefCollection,
) -> None:
    """
    Collect all Conflicts between two collections of fields.
    :param context: context forwarded to the validation rule
    :param conflicts: conflicts found
    :param cached_fields_and_fragment_names: store fields and fragment names
    :param compared_fragment_pairs: a PairSet instance
    :param parent_fields_are_mutually_exclusive: whether or not they are
    exclusive
    :param field_map_1: first collection of node and definitions
    :param field_map_2: second collection of node and definitions
    :type context: ASTValidationContext
    :type conflicts: List[Conflict]
    :type cached_fields_and_fragment_names: Dict[
        int, Tuple[NodeAndDefCollection, List[str]]
    ]
    :type compared_fragment_pairs: PairSet
    :type parent_fields_are_mutually_exclusive: bool
    :type field_map_1: NodeAndDefCollection
    :type field_map_2: NodeAndDefCollection
    """
    for response_name, fields_1 in field_map_1.items():
        fields_2 = field_map_2.get(response_name)
        if fields_2:
            for field_1 in fields_1:
                for field_2 in fields_2:
                    conflict = _find_conflict(
                        context,
                        cached_fields_and_fragment_names,
                        compared_fragment_pairs,
                        parent_fields_are_mutually_exclusive,
                        response_name,
                        field_1,
                        field_2,
                    )
                    if conflict:
                        conflicts.append(conflict)


def _find_conflict(
    context: "ASTValidationContext",
    cached_fields_and_fragment_names: Dict[
        int, Tuple[NodeAndDefCollection, List[str]]
    ],
    compared_fragment_pairs: "PairSet",
    parent_fields_are_mutually_exclusive: bool,
    response_name: str,
    field_1: NodeAndDef,
    field_2: NodeAndDef,
) -> Optional[Conflict]:
    """
    Determine whether or not there is a conflict between two particular
    fields.
    :param context: context forwarded to the validation rule
    :param cached_fields_and_fragment_names: store fields and fragment names
    :param compared_fragment_pairs: a PairSet instance
    :param parent_fields_are_mutually_exclusive: whether or not they are
    exclusive
    :param response_name: field query response name
    :param field_1: first field node and definitions
    :param field_2: second field node and definitions
    :type context: ASTValidationContext
    :type cached_fields_and_fragment_names: Dict[
        int, Tuple[NodeAndDefCollection, List[str]]
    ]
    :type compared_fragment_pairs: PairSet
    :type parent_fields_are_mutually_exclusive: bool
    :type response_name: str
    :type field_1: NodeAndDef
    :type field_2: NodeAndDef
    :return: whether or not there is a conflict between two particular fields
    :rtype: Optional[Conflict]
    """
    # pylint: disable=too-many-locals
    parent_type_1, node_1, def_1 = field_1
    parent_type_2, node_2, def_2 = field_2

    are_mutually_exclusive = parent_fields_are_mutually_exclusive or (
        parent_type_1 != parent_type_2
        and is_object_type(parent_type_1)
        and is_object_type(parent_type_2)
    )

    if not are_mutually_exclusive:
        name_1 = node_1.name.value
        name_2 = node_2.name.value
        if name_1 != name_2:
            return (
                (
                    response_name,
                    f"< {name_1} > and < {name_2} > are different fields",
                ),
                [node_1],
                [node_2],
            )

        args_1 = node_1.arguments or []
        args_2 = node_2.arguments or []

        if not _same_arguments(args_1, args_2):
            return (
                (response_name, "they have differing arguments"),
                [node_1],
                [node_2],
            )

    type_1 = def_1.type if def_1 else None
    type_2 = def_2.type if def_2 else None
    if type_1 and type_2 and _do_types_conflict(type_1, type_2):
        return (
            (
                response_name,
                f"they return conflicting types < {type_1} > and < {type_2} >",
            ),
            [node_1],
            [node_2],
        )

    selection_set_1 = node_1.selection_set
    selection_set_2 = node_2.selection_set
    if selection_set_1 and selection_set_2:
        conflicts = _find_conflicts_between_sub_selection_sets(
            context,
            cached_fields_and_fragment_names,
            compared_fragment_pairs,
            are_mutually_exclusive,
            get_wrapped_named_type(type_1),
            selection_set_1,
            get_wrapped_named_type(type_2),
            selection_set_2,
        )
        return _subfield_conflicts(conflicts, response_name, node_1, node_2)

    return None


def _same_arguments(
    arguments_1: "ArgumentNode", arguments_2: "ArgumentNode"
) -> bool:
    """
    Determine whether or not two argument are equals.
    :param arguments_1: first argument to check
    :param arguments_2: second argument to check
    :type arguments_1: ArgumentNode
    :type arguments_2: ArgumentNode
    :return: whether or not two argument are equals
    :rtype: bool
    """
    if len(arguments_1) != len(arguments_2):
        return False

    for argument_1 in arguments_1:
        for argument_2 in arguments_2:
            if argument_2.name.value == argument_1.name.value:
                if not _same_value(argument_1.value, argument_2.value):
                    return False
                break
        else:
            return False
    return True


def _same_value(value_1: "ValueNode", value_2: "ValueNode") -> bool:
    """
    Determine whether or not two value are equals.
    :param value_1: first value to check
    :param value_2: second value to check
    :type value_1: ValueNode
    :type value_2: ValueNode
    :return: whether or not two value are equals
    :rtype: bool
    """
    return str(value_1) == str(value_2)


def _do_types_conflict(
    type_1: "GraphQLOutputType", type_2: "GraphQLOutputType"
) -> bool:
    """
    Determine whether or not two GraphQLOutputType conflicts.
    :param type_1: first GraphQLOutputType to check
    :param type_2: second GraphQLOutputType to check
    :type type_1: GraphQLOutputType
    :type type_2: GraphQLOutputType
    :return: whether or not two GraphQLType conflicts
    :rtype: bool
    """
    if is_list_type(type_1):
        return (
            _do_types_conflict(type_1.wrapped_type, type_2.wrapped_type)
            if is_list_type(type_2)
            else True
        )
    if is_list_type(type_2):
        return True
    if is_non_null_type(type_1):
        return (
            _do_types_conflict(type_1.wrapped_type, type_2.wrapped_type)
            if is_non_null_type(type_2)
            else True
        )
    if is_non_null_type(type_2):
        return True
    if is_leaf_type(type_1) or is_leaf_type(type_2):
        return type_1 is not type_2
    return False


def _get_fields_and_fragment_names(
    context: "ASTValidationContext",
    cached_fields_and_fragment_names: Dict[
        int, Tuple[NodeAndDefCollection, List[str]]
    ],
    parent_type: Optional["GraphQLCompositeType"],
    selection_set: "SelectionSetNode",
) -> Tuple[NodeAndDefCollection, List[str]]:
    """
    Given a selection set, return the collection of fields as well as a
    list of fragment names referenced via fragment spreads.
    :param context: context forwarded to the validation rule
    :param cached_fields_and_fragment_names: store fields and fragment names
    :param parent_type: current GraphQL parent type instance
    :param selection_set: current SelectionSetNode
    :type context: ASTValidationContext
    :type cached_fields_and_fragment_names: Dict[
        int, Tuple[NodeAndDefCollection, List[str]]
    ]
    :type parent_type: Optional[GraphQLCompositeType]
    :type selection_set: SelectionSetNode,
    :return: the collection of fields as well as a list of fragment names
    :rtype: Tuple[NodeAndDefCollection, List[str]]
    """
    cached = cached_fields_and_fragment_names.get(id(selection_set))
    if not cached:
        node_and_defs = {}
        fragment_names = set()
        _collect_fields_and_fragment_names(
            context, parent_type, selection_set, node_and_defs, fragment_names,
        )
        cached = (node_and_defs, sorted(fragment_names))
        cached_fields_and_fragment_names[id(selection_set)] = cached
    return cached


def _get_referenced_fields_and_fragment_names(
    context: "ASTValidationContext",
    cached_fields_and_fragment_names: Dict[
        int, Tuple[NodeAndDefCollection, List[str]]
    ],
    fragment: "FragmentDefinitionNode",
) -> Tuple[NodeAndDefCollection, List[str]]:
    """
    Given a reference to a fragment, return the represented collection
    of fields as well as a list of nested fragment names referenced via
    fragment spreads.
    :param context: context forwarded to the validation rule
    :param cached_fields_and_fragment_names: store fields and fragment names
    :param fragment: a FragmentDefinitionNode instance
    :type context: ASTValidationContext
    :type cached_fields_and_fragment_names: Dict[
        int, Tuple[NodeAndDefCollection, List[str]]
    ]
    :type fragment: FragmentDefinitionNode
    :return: the represented collection of fields as well as a list of nested
    fragment names referenced via fragment spreads
    :rtype: Tuple[NodeAndDefCollection, List[str]]
    """
    cached = cached_fields_and_fragment_names.get(id(fragment.selection_set))
    if cached:
        return cached

    return _get_fields_and_fragment_names(
        context,
        cached_fields_and_fragment_names,
        schema_type_from_ast(context.schema, fragment.type_condition),
        fragment.selection_set,
    )


def _collect_fields_and_fragment_names(
    context: "ASTValidationContext",
    parent_type: Optional["GraphQLCompositeType"],
    selection_set: "SelectionSetNode",
    node_and_defs: NodeAndDefCollection,
    fragment_names: Set[str],
) -> None:
    """
    Collect fields and fragment names from a selection set.
    :param context: context forwarded to the validation rule
    :param parent_type: the GraphQLType instance of the parent type
    :param selection_set: the SelectionSetNode instance to parse
    :param node_and_defs: collection of node a definitions
    :param fragment_names: list of visited fragment names
    :type context: ASTValidationContext
    :type parent_type: Optional[GraphQLCompositeType]
    :type selection_set: SelectionSetNode,
    :type node_and_defs: NodeAndDefCollection
    :type fragment_names: Set[str]
    """
    for selection in selection_set.selections:
        if isinstance(selection, FieldNode):
            field_name = selection.name.value
            field_def = (
                parent_type.find_field(field_name)
                if (
                    is_object_type(parent_type)
                    or is_interface_type(parent_type)
                )
                and parent_type.has_field(field_name)
                else None
            )
            node_and_defs.setdefault(
                get_field_entry_key(selection), []
            ).append((parent_type, selection, field_def))
        elif isinstance(selection, FragmentSpreadNode):
            fragment_names.add(selection.name.value)
        elif isinstance(selection, InlineFragmentNode):
            type_condition = selection.type_condition
            inline_fragment_type = (
                schema_type_from_ast(context.schema, type_condition)
                if type_condition
                else parent_type
            )
            _collect_fields_and_fragment_names(
                context,
                inline_fragment_type,
                selection.selection_set,
                node_and_defs,
                fragment_names,
            )


def _subfield_conflicts(
    conflicts: List[Conflict],
    response_name: str,
    node_1: "FieldNode",
    node_2: "FieldNode",
) -> Optional[Conflict]:
    """
    Given a series of Conflicts which occurred between two sub-fields,
    generate a single Conflict.
    :param conflicts: conflicts found
    :param response_name: field query response name
    :param node_1: first field node to check
    :param node_2: second field node to check
    :type conflicts: List[Conflict]
    :type response_name: str
    :type node_1: FieldNode
    :type node_2: FieldNode
    :return: a conflict if found
    :rtype: Optional[Conflict]
    """
    if conflicts:
        response_names = [response_name, []]
        nodes_1 = [node_1]
        nodes_2 = [node_2]
        for conflict in conflicts:
            response_names[1].append(conflict[0])
            nodes_1.extend(conflict[1])
            nodes_2.extend(conflict[2])
        return (response_names, nodes_1, nodes_2)
    return None


class PairSet:
    """
    A way to keep track of pairs of things when the ordering of the pair
    does not matter. We do this by maintaining a sort of double
    adjacency sets.
    """

    __slots__ = ("_data",)

    def __init__(self) -> None:
        self._data = {}

    def has(
        self, name_1: str, name_2: str, are_mutually_exclusive: bool
    ) -> bool:
        """
        Determine whether or not those fragments has been compared
        :param name_1: first fragment name
        :param name_2: second fragment name
        :param are_mutually_exclusive: whether or not they are mutually exclusive
        :type name_1: str
        :type name_2: str
        :type are_mutually_exclusive: bool
        :return: whether or not those fragments has been compared
        :rtype: bool
        """
        first = self._data.get(name_1)
        result = first and first.get(name_2)
        if result is None:
            return False

        if not are_mutually_exclusive:
            return not result
        return True

    def _pair_set_add(
        self, name_1: str, name_2: str, are_mutually_exclusive: bool
    ) -> None:
        """
        Add a new entry to mark those fragments has already compared.
        :param name_1: first fragment name
        :param name_2: second fragment name
        :param are_mutually_exclusive: whether or not they are mutually exclusive
        :type name_1: str
        :type name_2: str
        :type are_mutually_exclusive: bool
        """
        a_map = self._data.get(name_1)
        if not a_map:
            self._data[name_1] = a_map = {}
        a_map[name_2] = are_mutually_exclusive

    def add(
        self, name_1: str, name_2: str, are_mutually_exclusive: bool
    ) -> None:
        """
        Add an entry for each fragment to mark those has compared.
        :param name_1: first fragment name
        :param name_2: second fragment name
        :param are_mutually_exclusive: whether or not they are mutually exclusive
        :type name_1: str
        :type name_2: str
        :type are_mutually_exclusive: bool
        """
        self._pair_set_add(name_1, name_2, are_mutually_exclusive)
        self._pair_set_add(  # pylint: disable=arguments-out-of-order
            name_2, name_1, are_mutually_exclusive
        )
