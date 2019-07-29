from functools import lru_cache
from typing import Dict, List, Optional, Set, Tuple, Union

from tartiflette.execution.nodes.variable_definition import (
    variable_definition_node_to_executable,
)
from tartiflette.language.ast import (
    FieldNode,
    FragmentSpreadNode,
    InlineFragmentNode,
)
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.types.exceptions.tartiflette import (
    SkipCollection,
    TartifletteError,
)
from tartiflette.types.helpers.get_directive_instances import (
    compute_directive_nodes,
)
from tartiflette.utils.directives import wraps_with_directives
from tartiflette.utils.errors import to_graphql_error
from tartiflette.utils.type_from_ast import schema_type_from_ast

__all__ = (
    "parse_and_validate_query",
    "collect_executable_variable_definitions",
    "collect_fields",
    "collect_subfields",
)


@lru_cache(maxsize=512)
def parse_and_validate_query(
    query: Union[str, bytes]
) -> Tuple[Optional["DocumentNode"], Optional[List["TartifletteError"]]]:
    """
    Analyzes & validates a query by converting it to a DocumentNode.
    :param query: the GraphQL request / query as UTF8-encoded string
    :type query: Union[str, bytes]
    :return: a DocumentNode representing the query
    :rtype: Tuple[Optional[DocumentNode], Optional[List[TartifletteError]]]
    """
    try:
        document: "DocumentNode" = parse_to_document(query)
    except TartifletteError as e:
        return None, [e]
    except Exception as e:  # pylint: disable=broad-except
        return (
            None,
            [to_graphql_error(e, message="Server encountered an error.")],
        )
    # TODO: implements the `validate_document` function
    # errors = validate_document(document)
    # if errors:
    #     return None, errors
    return document, None


@lru_cache(maxsize=512)
def collect_executable_variable_definitions(
    schema: "GraphQLSchema",
    document: "DocumentNode",
    operation: "OperationDefinitionNode",
) -> List["ExecutableVariableDefinition"]:
    """
    Go recursively through all variable definition AST nodes to convert them as
    executable variable definition.
    :param schema: the GraphQLSchema instance linked to the engine
    :param document: the DocumentNode instance linked to the GraphQL request
    :param operation: the AST operation definition node to execute
    :type schema: GraphQLSchema
    :type document: DocumentNode
    :type operation: OperationDefinitionNode
    :return: a list of executable variable definition
    :rtype: List[ExecutableVariableDefinition]
    """
    # pylint: disable=unused-argument
    if not operation.variable_definitions:
        return []

    return [
        variable_definition_node_to_executable(
            schema, variable_definition_node
        )
        for variable_definition_node in operation.variable_definitions
    ]


async def should_include_node(
    execution_context: "ExecutionContext",
    node: Union["FragmentSpreadNode", "FieldNode", "InlineFragmentNode"],
) -> bool:
    """
    Determines if a field should be included based on the @include and @skip
    directives, where @skip has higher precedence than @include.
    :param execution_context: instance of the query execution context
    :param node: the selection node to collect or skip
    :type execution_context: ExecutionContext
    :type node: Union[FragmentSpreadNode, FieldNode, InlineFragmentNode]
    :return: whether or not the node should be collected or skipped
    :rtype: bool
    """
    if not node.directives:
        return True

    hook_name = (
        "on_field_collection"
        if isinstance(node, FieldNode)
        else (
            "on_fragment_spread_collection"
            if isinstance(node, FragmentSpreadNode)
            else "on_inline_fragment_collection"
        )
    )

    try:
        await wraps_with_directives(
            directives_definition=compute_directive_nodes(
                execution_context.schema,
                node.directives,
                execution_context.variable_values,
            ),
            directive_hook=hook_name,
            with_default=True,
        )(
            node,
            execution_context.context,
            context_coercer=execution_context.context,
        )
    except SkipCollection:
        return False
    except Exception:  # pylint: disable=broad-except
        # TODO: we should store unexpected exception in order to treat them as
        # field result on execution to handle them the same way as resolved
        # value and having the bubble up error and so on.
        return False
    return True


def get_field_entry_key(node: "FieldNode") -> str:
    """
    Implements the logic to compute the key of a given field's entry.
    :param node: field node from which to extract the entry key
    :type node: FieldNode
    :return: the field entry key
    :rtype: str
    """
    return node.alias.value if node.alias else node.name.value


def does_fragment_condition_match(
    execution_context: "ExecutionContext",
    fragment_node: Union["FragmentDefinitionNode", "InlineFragmentNode"],
    graphql_object_type: "GraphQLObjectType",
) -> bool:
    """
    Determines if a fragment is applicable to the given type.
    :param execution_context: instance of the query execution context
    :param fragment_node: fragment node to check
    :param graphql_object_type: GraphQLObjectType to check against with
    :type execution_context: ExecutionContext
    :type fragment_node: Union[FragmentDefinitionNode, InlineFragmentNode]
    :type graphql_object_type: GraphQLObjectType
    :return: whether or not the fragment is applicable to the given type
    :rtype: bool
    """
    type_condition_node = fragment_node.type_condition
    if not type_condition_node:
        return True

    conditional_type = schema_type_from_ast(
        execution_context.schema, type_condition_node
    )
    if conditional_type is graphql_object_type:
        return True

    return (
        conditional_type.is_abstract_type
        and conditional_type.is_possible_type(graphql_object_type)
    )


async def collect_fields(
    execution_context: "ExecutionContext",
    runtime_type: "GraphQLObjectType",
    selection_set: "SelectionSetNode",
    fields: Optional[Dict[str, List["FieldNode"]]] = None,
    visited_fragment_names: Optional[Set[str]] = None,
) -> Dict[str, List["FieldNode"]]:
    """
    Given a SelectionSet, adds all of the fields in that selection to
    the passed in map of fields, and returns it at the end.

    CollectFields requires the "runtime type" of an object. For a field which
    returns an Interface or Union type, the "runtime type" will be the actual
    Object type returned by that field.
    :param execution_context: instance of the query execution context
    :param runtime_type: current runtime type of the selection set
    :param selection_set: selection set node to parse
    :param fields: dictionary of collected fields
    :param visited_fragment_names: the set of fragment names already visited
    :type execution_context: ExecutionContext
    :type runtime_type: GraphQLObjectType
    :type selection_set: SelectionSetNode
    :type fields: Optional[Dict[str, List[FieldNode]]]
    :type visited_fragment_names: Optional[Set[str]]
    :return: the dictionary of collected fields
    :rtype: Dict[str, List[FieldNode]]
    """
    if fields is None:
        fields: Dict[str, "FieldNode"] = {}

    if visited_fragment_names is None:
        visited_fragment_names: Set[str] = set()

    for selection in selection_set.selections:
        if isinstance(selection, FieldNode):
            if not await should_include_node(execution_context, selection):
                continue
            fields.setdefault(get_field_entry_key(selection), []).append(
                selection
            )
        elif isinstance(selection, InlineFragmentNode):
            if not await should_include_node(
                execution_context, selection
            ) or not does_fragment_condition_match(
                execution_context, selection, runtime_type
            ):
                continue

            await collect_fields(
                execution_context,
                runtime_type,
                selection.selection_set,
                fields,
                visited_fragment_names,
            )
        elif isinstance(selection, FragmentSpreadNode):
            fragment_name = selection.name.value
            if (
                fragment_name in visited_fragment_names
                or not await should_include_node(execution_context, selection)
            ):
                continue

            visited_fragment_names.add(fragment_name)

            fragment_definition = execution_context.fragments[fragment_name]
            if not fragment_definition or not does_fragment_condition_match(
                execution_context, fragment_definition, runtime_type
            ):
                continue

            await collect_fields(
                execution_context,
                runtime_type,
                fragment_definition.selection_set,
                fields,
                visited_fragment_names,
            )
    return fields


async def collect_subfields(
    execution_context: "ExecutionContext",
    return_type: "GraphQLOutputType",
    field_nodes: List["FieldNode"],
) -> Dict[str, List["FieldNode"]]:
    """
    Collects the fields of each field nodes.
    :param execution_context: instance of the query execution context
    :param return_type: GraphQLOutputType of the parent field
    :param field_nodes: AST nodes related to the parent field
    :type execution_context: ExecutionContext
    :type return_type: GraphQLOutputType
    :type field_nodes: List[FieldNode]
    :return: the dictionary of collected fields
    :rtype: Dict[str, List[FieldNode]]
    """
    subfield_nodes: Dict[str, List["FieldNode"]] = {}
    visited_fragment_names: Set[str] = set()
    for field_node in field_nodes:
        selection_set = field_node.selection_set
        if selection_set:
            subfield_nodes = await collect_fields(
                execution_context,
                return_type,
                selection_set,
                subfield_nodes,
                visited_fragment_names,
            )
    return subfield_nodes
