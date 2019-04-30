from functools import partial
from typing import Any, Dict, List, Optional, Union

from tartiflette.parser.cffi import (
    Visitor,
    _VisitorElement,
    _VisitorElementBooleanValue,
    _VisitorElementEnumValue,
    _VisitorElementField,
    _VisitorElementFloatValue,
    _VisitorElementFragmentDefinition,
    _VisitorElementInlineFragment,
    _VisitorElementIntValue,
    _VisitorElementNullValue,
    _VisitorElementOperationDefinition,
    _VisitorElementSelectionSet,
    _VisitorElementStringValue,
)
from tartiflette.parser.nodes.argument import NodeArgument
from tartiflette.parser.nodes.directive import NodeDirective
from tartiflette.parser.nodes.field import NodeField
from tartiflette.parser.nodes.fragment_definition import NodeFragmentDefinition
from tartiflette.parser.nodes.operation_definition import (
    NodeOperationDefinition,
)
from tartiflette.parser.nodes.variable_definition import NodeVariableDefinition
from tartiflette.parser.visitor.list_value import ListValue
from tartiflette.parser.visitor.object_value import ObjectValue
from tartiflette.parser.visitor.visitor_context import InternalVisitorContext
from tartiflette.schema import GraphQLSchema
from tartiflette.types.exceptions.tartiflette import (
    AlreadyDefined,
    InvalidType,
    MissingRequiredArgument,
    MultipleRootNodeOnSubscriptionOperation,
    NotALeafType,
    NotAnObjectType,
    NotLoneAnonymousOperation,
    NotUniqueOperationName,
    UndefinedDirectiveArgument,
    UndefinedFieldArgument,
    UndefinedFragment,
    UniqueArgumentNames,
    UnknownSchemaFieldResolver,
    UnknownTypeDefinition,
    UnknownVariableException,
    UnusedFragment,
)
from tartiflette.types.helpers import reduce_type, transform_directive
from tartiflette.utils.arguments import UNDEFINED_VALUE


class FragmentData:
    def __init__(self, atype: str, depth: int) -> None:
        self.type = atype
        self.depth = depth
        self.directives = []

    def add_directive(self, directive):
        self.directives.append(directive)


class TartifletteVisitor(Visitor):
    # pylint: disable=too-many-instance-attributes

    def __init__(
        self, schema: GraphQLSchema, variables: Optional[Dict[str, Any]] = None
    ):
        super().__init__()
        self._events = [
            {
                "default": self._in,
                "Argument": self._on_argument_in,
                "Directive": self._on_directive_in,
                "Field": self._on_field_in,
                "Variable": self._on_variable_in,
                "IntValue": self._on_value_in,
                "StringValue": self._on_value_in,
                "BooleanValue": self._on_value_in,
                "FloatValue": self._on_value_in,
                "NullValue": self._on_value_in,
                "EnumValue": self._on_value_in,
                "NamedType": self._on_named_type_in,
                "ListType": self._on_list_type_in,
                "NonNullType": self._on_non_null_type_in,
                "VariableDefinition": self._on_variable_definition_in,
                "FragmentDefinition": self._on_fragment_definition_in,
                "OperationDefinition": self._on_operation_definition_in,
                "InlineFragment": self._on_inline_fragment_in,
                "SelectionSet": self._on_selection_set_in,
                "ObjectValue": self._on_object_value_in,
                "ObjectField": self._on_object_field_in,
                "FragmentSpread": self._on_fragment_spread_in,
                "ListValue": self._on_list_value_in,
            },
            {
                "default": self._out,
                "Document": self._on_document_out,
                "Argument": self._on_argument_out,
                "Directive": self._on_directive_out,
                "Field": self._on_field_out,
                "VariableDefinition": self._on_variable_definition_out,
                "FragmentDefinition": self._on_fragment_definition_out,
                "FragmentSpread": self._on_fragment_spread_out,
                "OperationDefinition": self._on_operation_definition_out,
                "InlineFragment": self._on_inline_fragment_out,
                "ObjectValue": self._on_object_or_list_value_out,
                "ListValue": self._on_object_or_list_value_out,
            },
        ]

        self.operations = {}
        self._named_operations = {}
        self._anonymous_operations = []
        self._vars = variables or {}
        self._fragments = {}
        self._used_fragments = set()
        self.schema: GraphQLSchema = schema
        self.exceptions: List[Exception] = []
        self._to_call_later = []
        self._internal_ctx = InternalVisitorContext()
        self._in_fragment_spread_context = False
        self._error_path = None

    def _add_exception(self, exception: Exception) -> None:
        self.continue_child = 0
        self._error_path = self._internal_ctx.path
        self.exceptions.append(exception)

    def _reset_error_path_and_continue_child(self) -> None:
        self.continue_child = 1
        self._error_path = None

    def _get_parent_type(self, node: NodeField) -> Union[str, "GraphQLType"]:
        try:
            return reduce_type(node.field_executor.schema_field.gql_type)
        except (AttributeError, TypeError):
            pass
        return self.schema.find_type(
            self.schema.get_operation_type(self._internal_ctx.operation.type)
        )

    def _on_argument_in(
        self, element: _VisitorElement, *_args, **_kwargs
    ) -> None:
        if not self._internal_ctx.directive:
            parent_type = self._get_parent_type(self._internal_ctx.node.parent)

            if element.name not in self._internal_ctx.current_field.arguments:
                self._add_exception(
                    UndefinedFieldArgument(
                        "Undefined argument < %s > on field < %s > of type < "
                        "%s >."
                        % (
                            element.name,
                            self._internal_ctx.node.name,
                            parent_type,
                        ),
                        locations=[element.get_location()],
                    )
                )
                return

            if element.name in self._internal_ctx.node.arguments:
                self._add_exception(
                    UniqueArgumentNames(
                        "There can be only one argument named < %s >."
                        % element.name,
                        locations=[
                            self._internal_ctx.node.arguments[
                                element.name
                            ].location,
                            element.get_location(),
                        ],
                    )
                )
                return
        else:
            try:
                directive = self.schema.find_directive(
                    self._internal_ctx.directive.name
                )
            except KeyError:
                return

            if element.name not in directive.arguments:
                self._add_exception(
                    UndefinedDirectiveArgument(
                        "Undefined argument < %s > on directive < @%s >."
                        % (element.name, directive.name),
                        locations=[element.get_location()],
                    )
                )
                return

            if element.name in self._internal_ctx.directive.arguments:
                self._add_exception(
                    UniqueArgumentNames(
                        "There can be only one argument named < %s >."
                        % element.name,
                        locations=[
                            self._internal_ctx.directive.arguments[
                                element.name
                            ].location,
                            element.get_location(),
                        ],
                    )
                )
                return

        self._internal_ctx.argument = NodeArgument(
            self._internal_ctx.path, element.get_location(), element.name
        )

    def _on_argument_out(self, *_args, **_kwargs) -> None:
        self._internal_ctx.argument = None

    def _on_directive_in(
        self, element: _VisitorElement, *_args, **_kwargs
    ) -> None:
        self._internal_ctx.directive = NodeDirective(
            self._internal_ctx.path, element.get_location(), element.name
        )

    def _on_directive_out(
        self, element: _VisitorElement, *_args, **_kwargs
    ) -> None:
        try:
            directive = self.schema.find_directive(
                self._internal_ctx.directive.name
            )
        except KeyError:
            self._internal_ctx.directive = None
            return

        for argument in directive.arguments.values():
            if not argument.is_required:
                continue

            value = self._internal_ctx.directive.arguments.get(argument.name)
            if value is None:
                self._add_exception(
                    MissingRequiredArgument(
                        "Missing required < %s > argument on < @%s > directive."
                        % (argument.name, directive.name),
                        locations=[element.get_location()],
                    )
                )

        destination = (
            self._internal_ctx.inline_fragment_info
            or self._internal_ctx.fragment_spread
            or self._internal_ctx.node
        )
        if destination:
            destination.add_directive(
                transform_directive(
                    directive,
                    args={
                        x.name: x.value
                        for x in self._internal_ctx.directive.arguments.values()
                    },
                )
            )
        self._internal_ctx.directive = None

    def _add_argument_to_parent(self):
        if self._internal_ctx.argument.value is UNDEFINED_VALUE:
            return

        if not self._internal_ctx.directive:
            self._internal_ctx.node.arguments[
                self._internal_ctx.argument.name
            ] = self._internal_ctx.argument
            return

        self._internal_ctx.directive.arguments[
            self._internal_ctx.argument.name
        ] = self._internal_ctx.argument

    def _on_value_in(
        self,
        element: Union[
            _VisitorElementIntValue,
            _VisitorElementStringValue,
            _VisitorElementFloatValue,
            _VisitorElementBooleanValue,
            _VisitorElementEnumValue,
            _VisitorElementNullValue,
        ],
        *_args,
        **_kwargs,
    ) -> None:
        if self._internal_ctx.current_object_value is not None:
            self._internal_ctx.current_object_value.set_value(
                element.get_value()
            )
            return

        if hasattr(self._internal_ctx.node, "default_value"):
            self._internal_ctx.node.default_value = element.get_value()
            return

        self._internal_ctx.argument.value = element.get_value()
        self._add_argument_to_parent()

    def _objlist_value_in(self, node):
        if (
            self._internal_ctx.argument
            and self._internal_ctx.argument.value is None
        ):
            self._internal_ctx.argument.value = node

        if self._internal_ctx.current_object_value is not None:
            self._internal_ctx.current_object_value.set_value(node)

        node.parent = self._internal_ctx.current_object_value
        self._internal_ctx.current_object_value = node

    def _on_object_value_in(self, _: _VisitorElement, *_args, **_kwargs):
        self._objlist_value_in(ObjectValue())

    def _on_object_field_in(self, element: _VisitorElement, *_args, **_kwargs):
        self._internal_ctx.current_object_value.set_key(element.name)

    def _on_object_or_list_value_out(
        self, _: _VisitorElement, *_args, **_kwargs
    ):
        self._internal_ctx.current_object_value = (
            self._internal_ctx.current_object_value.parent
        )

        if self._internal_ctx.current_object_value is None:
            self._add_argument_to_parent()

    def _on_list_value_in(self, _: _VisitorElement, *_args, **_kwargs):
        self._objlist_value_in(ListValue())

    def _on_variable_in(
        self, element: _VisitorElement, *_args, **_kwargs
    ) -> None:
        if hasattr(self._internal_ctx.node, "var_name"):
            self._internal_ctx.node.var_name = element.name
            return

        var_name = element.name
        try:
            if self._internal_ctx.current_object_value is not None:
                self._internal_ctx.current_object_value.set_value(
                    self._vars[var_name]
                )
                return

            self._internal_ctx.argument.value = self._vars[var_name]
            self._add_argument_to_parent()

        except KeyError:
            self._add_exception(UnknownVariableException(var_name))

    def _on_field_in(
        self,
        element: _VisitorElementField,
        *_args,
        type_cond_depth: int = -1,
        directives: List[Dict[str, Any]] = None,
        **_kwargs,
    ) -> None:
        # pylint: disable=too-many-locals
        type_cond = self._internal_ctx.compute_type_cond(type_cond_depth)
        parent_type = self._get_parent_type(self._internal_ctx.node)

        try:
            field = self.schema.get_field_by_name(
                str(parent_type) + "." + element.name
            )
        except UnknownSchemaFieldResolver as e:
            try:
                if type_cond is None:
                    raise
                field = self.schema.get_field_by_name(
                    str(type_cond) + "." + element.name
                )
            except UnknownSchemaFieldResolver as e:
                e.path = self._internal_ctx.field_path[:] + [element.name]
                e.locations = [element.get_location()]
                self._add_exception(e)
                return

        if field.is_leaf and element.get_selection_set_size() > 0:
            self._add_exception(
                NotAnObjectType(
                    message=f"field < {field.name} > is a leaf and thus can't have a selection set",
                    path=self._internal_ctx.field_path[:] + [element.name],
                    locations=[element.get_location()],
                )
            )
            return

        if not field.is_leaf and element.get_selection_set_size() < 1:
            self._add_exception(
                NotALeafType(
                    message=f"field < {field.name} > is not a leaf and thus must have a selection set",
                    path=self._internal_ctx.field_path[:] + [element.name],
                    locations=[element.get_location()],
                )
            )
            return

        self._internal_ctx.move_in_field(element, field)

        node = NodeField(
            element.name,
            self.schema,
            field.resolver,
            element.get_location(),
            self._internal_ctx.field_path[:],
            type_cond,
            element.get_alias(),
            subscribe=field.subscribe,
        )

        if self._internal_ctx.inline_fragment_info:
            for (
                directive
            ) in self._internal_ctx.inline_fragment_info.directives:
                node.add_directive(directive)

        if directives:
            for directive in directives:
                node.add_directive(directive)

        node.set_parent(self._internal_ctx.node)
        if self._internal_ctx.node:
            self._internal_ctx.node.add_child(node)

        self._internal_ctx.node = node

        if self._internal_ctx.depth == 1:
            self.operations[self._internal_ctx.operation.name].children.append(
                node
            )

    def _on_field_out(self, *_args, **_kwargs) -> None:
        for argument in self._internal_ctx.current_field.arguments.values():
            if not argument.is_required:
                continue

            value = self._internal_ctx.node.arguments.get(argument.name)
            if value is None:
                self._add_exception(
                    MissingRequiredArgument(
                        "Missing required < %s > argument on < %s > field."
                        % (argument.name, self._internal_ctx.node.name),
                        locations=[self._internal_ctx.node.location],
                    )
                )
        self._internal_ctx.move_out_field()

    def _on_variable_definition_in(
        self, element: _VisitorElement, *_args, **_kwargs
    ) -> None:
        node = NodeVariableDefinition(
            self._internal_ctx.path, element.get_location(), element.name
        )
        node.set_parent(self._internal_ctx.node)
        self._internal_ctx.node = node

    def _validate_type(
        self, varname: str, a_value: Any, a_type: Any, is_nullable: bool
    ) -> None:
        if is_nullable and a_value is None:
            return

        try:
            if not isinstance(a_value, a_type):
                self._add_exception(
                    InvalidType(
                        "Given value for < %s > is not type < %s >"
                        % (varname, a_type),
                        path=self._internal_ctx.field_path[:],
                        locations=[self._internal_ctx.node.location],
                    )
                )
        except TypeError:
            # TODO remove this, and handle the case it's an InputValue
            # (look at registered input values and compare fields)
            pass

    def _validates_vars(self) -> None:
        # validate given var are okay
        name = self._internal_ctx.node.var_name
        if name not in self._vars:
            default_values = self._internal_ctx.node.default_value
            if (
                default_values is None or default_values is UNDEFINED_VALUE
            ) and not self._internal_ctx.node.is_nullable:
                self._add_exception(UnknownVariableException(name))
                return

            self._vars[name] = default_values
            return

        a_type = self._internal_ctx.node.var_type
        is_nullable = self._internal_ctx.node.is_nullable
        a_value = self._vars[name]

        if self._internal_ctx.node.is_list:
            if not isinstance(a_value, list):
                self._add_exception(
                    InvalidType(
                        "Expecting List for < %s > values" % name,
                        path=self._internal_ctx.field_path[:],
                        locations=[self._internal_ctx.node.location],
                    )
                )
                return

            for val in a_value:
                self._validate_type(name, val, a_type, is_nullable)
            return

        self._validate_type(name, a_value, a_type, is_nullable)
        return

    def _on_variable_definition_out(self, *_args, **_kwargs) -> None:
        self._validates_vars()
        # now the VariableDefinition Node is useless so kill it
        self._internal_ctx.node = self._internal_ctx.node.parent

    def _on_named_type_in(
        self, element: _VisitorElement, *_args, **_kwargs
    ) -> None:
        try:
            self._internal_ctx.node.var_type = element.name
        except AttributeError:
            pass

    def _on_list_type_in(self, *_args, **_kwargs) -> None:
        try:
            self._internal_ctx.node.is_list = True
        except AttributeError:
            pass

    def _on_non_null_type_in(self, *_args, **_kwargs) -> None:
        self._internal_ctx.node.is_nullable = False

    def _on_fragment_definition_in(
        self, element: _VisitorElementFragmentDefinition, *_args, **_kwargs
    ) -> None:
        if element.name in self._fragments:
            self._add_exception(
                AlreadyDefined(
                    "Fragment < %s > already defined" % element.name,
                    path=self._internal_ctx.field_path[:],
                    locations=[element.get_location()],
                )
            )
            return

        type_condition = element.get_type_condition()
        if not self.schema.has_type(type_condition):
            self._add_exception(
                UnknownTypeDefinition(
                    "Unknown type < %s >." % type_condition,
                    locations=[element.get_location()],
                )
            )
            return

        nfd = NodeFragmentDefinition(
            self._internal_ctx.path,
            element.get_location(),
            element.name,
            type_condition=type_condition,
        )

        self._internal_ctx.fragment_definition = nfd
        self._fragments[element.name] = nfd

    def _on_fragment_definition_out(self, *_args, **_kwargs) -> None:
        self._internal_ctx.fragment_definition = None

    def _fragment_spread(
        self,
        ctx: InternalVisitorContext,
        element: _VisitorElement,
        directives: [Dict[str, Any]],
    ) -> None:
        _ctx = self._internal_ctx
        self._internal_ctx = ctx

        self._used_fragments.add(element.name)
        try:
            cfd = self._fragments[element.name]
        except KeyError:
            self._add_exception(
                UndefinedFragment(
                    "Undefined fragment < %s >." % element.name,
                    locations=[element.get_location()],
                )
            )
            return

        depth = self._internal_ctx.depth
        self._internal_ctx.type_condition = cfd.type_condition

        self._in_fragment_spread_context = True
        kwargs = {"type_cond_depth": depth}
        for saved_callback in cfd.callbacks:
            kwargs["directives"] = None
            if depth == self._internal_ctx.depth:
                kwargs["directives"] = directives

            saved_callback(**kwargs)  # Simulate calling a the right place.

        self._in_fragment_spread_context = False

        self._internal_ctx.type_condition = None
        self._internal_ctx = _ctx

    def _on_fragment_spread_in(self, _: _VisitorElement, *_args, **_kwargs):
        self._internal_ctx.fragment_spread = FragmentData(None, None)

    def _on_fragment_spread_out(
        self, element: _VisitorElement, *_args, **_kwargs
    ) -> None:
        self._to_call_later.append(
            partial(
                self._fragment_spread,
                self._internal_ctx.clone(),
                element,
                self._internal_ctx.fragment_spread.directives,
            )
        )
        self._internal_ctx.fragment_spread = None

    def _on_operation_definition_in(
        self, element: _VisitorElementOperationDefinition, *_args, **_kwargs
    ) -> None:
        try:
            operation_node = self._named_operations[element.name]
        except KeyError:
            operation_node = NodeOperationDefinition(
                self._internal_ctx.path,
                element.get_location(),
                element.name,
                element.get_operation(),
            )
            if element.name is not None:
                self._named_operations[element.name] = operation_node
            else:
                self._anonymous_operations.append(operation_node)
        else:
            self._add_exception(
                NotUniqueOperationName(
                    "Operation name < %s > should be unique." % element.name,
                    locations=[
                        operation_node.location,
                        element.get_location(),
                    ],
                )
            )
            return

        self.operations[element.name] = operation_node

        self._internal_ctx.operation = operation_node

    def _on_operation_definition_out(self, *_args, **_kwargs) -> None:
        self._internal_ctx.operation = None

    def _on_inline_fragment_in(
        self, element: _VisitorElementInlineFragment, *_args, **_kwargs
    ) -> None:
        a_type = element.get_named_type()
        self._internal_ctx.inline_fragment_info = FragmentData(
            a_type, self._internal_ctx.depth
        )
        self._internal_ctx.type_condition = a_type

    def _on_inline_fragment_out(self, *_args, **_kwargs) -> None:
        self._internal_ctx.inline_fragment_info = None
        self._internal_ctx.type_condition = None

    def _on_document_out(self, *_args, **_kwargs) -> None:
        for saved_callback in self._to_call_later:
            saved_callback()

        unused_fragments = set(self._fragments) - self._used_fragments
        for unused_fragment in unused_fragments:
            self._add_exception(
                UnusedFragment(
                    "Fragment < %s > is never used." % unused_fragment,
                    locations=[self._fragments[unused_fragment].location],
                )
            )

        if self._anonymous_operations and (
            len(self._anonymous_operations) > 1 or self._named_operations
        ):
            for operation in self._anonymous_operations:
                self._add_exception(
                    NotLoneAnonymousOperation(
                        "Anonymous operation must be the only defined operation.",
                        locations=[operation.location],
                    )
                )

    def _on_selection_set_in(
        self, element: _VisitorElementSelectionSet, *_args, **_kwargs
    ) -> None:
        if (
            self._internal_ctx.operation.type == "Subscription"
            and self._internal_ctx.depth == 0
            and element.get_selections_size() > 1
        ):
            self._add_exception(
                MultipleRootNodeOnSubscriptionOperation(
                    "Subscription operations must have exactly one root field.",
                    locations=[self._internal_ctx.operation.location],
                )
            )

    def _in(self, element: _VisitorElement, *args, **kwargs) -> None:
        # While spreading out a fragment we execute all callbacks whether they
        # results on a continue_child=0 or not. The goal here is to not process
        # children of a node which result to a continue_child=0 while still
        # processing its siblings.

        if (
            self._in_fragment_spread_context
            and not self.continue_child
            and self._error_path
        ):
            if self._internal_ctx.path.startswith(self._error_path):
                self._internal_ctx.move_in(element)
                return
            self._reset_error_path_and_continue_child()

        self._internal_ctx.move_in(element)
        try:
            self._events[self.IN][element.libgraphql_type](
                element, *args, **kwargs
            )
        except KeyError:
            pass

    def _out(self, element: _VisitorElement, *args, **kwargs) -> None:
        # While spreading out a fragment we execute all callbacks whether they
        # results on a continue_child=0 or not. The goal here is to not process
        # children of a node which result to a continue_child=0 while still
        # processing its siblings.

        if (
            self._in_fragment_spread_context
            and not self.continue_child
            and self._error_path
        ):
            if self._internal_ctx.path.startswith(self._error_path):
                self._internal_ctx.move_out()
                return
            self._reset_error_path_and_continue_child()

        try:
            self._events[self.OUT][element.libgraphql_type](
                element, *args, **kwargs
            )
        except KeyError:
            pass
        finally:
            self._internal_ctx.move_out()

    def update(self, event: int, element: _VisitorElement) -> None:
        self.continue_child = 1
        self.event = event

        if (
            not self._internal_ctx.fragment_definition
            or element.libgraphql_type == "FragmentDefinition"
        ):
            # Always execute FragmentDefinitions Handlers,
            # never exec if in fragment.
            self._events[self.event]["default"](element)
        else:
            self._internal_ctx.fragment_definition.callbacks.append(
                partial(self._events[self.event]["default"], element)
            )
