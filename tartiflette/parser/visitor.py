from functools import lru_cache, partial
from typing import Any, Dict

from tartiflette.parser.cffi import (
    Visitor,
    _VisitorElement,
    _VisitorElementOperationDefinition,
)
from tartiflette.schema import GraphQLSchema
from tartiflette.types.exceptions.tartiflette import (
    TartifletteException,
    UnknownSchemaFieldResolver,
    UnknownVariableException,
)
from tartiflette.types.helpers import reduce_type

from .nodes.field import NodeField
from .nodes.fragment_definition import NodeFragmentDefinition
from .nodes.variable_definition import NodeVariableDefinition


class TartifletteVisitor(Visitor):
    # pylint: disable=too-many-instance-attributes

    #  TODO is usefull only for debug, will
    # be removed when everythings works
    #  Same as path information
    @staticmethod
    @lru_cache(maxsize=10)
    def create_node_name(gql_type, name=None):
        node_name = gql_type
        if name:
            node_name = node_name + "(%s)" % name
        return node_name

    def __init__(
        self, schema: GraphQLSchema, variables: Dict[str, Any] = None
    ):
        super().__init__()
        self.path = ""
        self.field_path = []
        self._events = [
            {
                "default": self._in,
                "Argument": self._on_argument_in,
                "Field": self._on_field_in,
                "Variable": self._on_variable_in,
                "IntValue": self._on_value_in,
                "StringValue": self._on_value_in,
                "BooleanValue": self._on_value_in,
                "FloatValue": self._on_value_in,
                "NamedType": self._on_named_type_in,
                "ListType": self._on_list_type_in,
                "NonNullType": self._on_non_null_type_in,
                "VariableDefinition": self._on_variable_definition_in,
                "FragmentDefinition": self._on_fragment_definition_in,
                "OperationDefinition": self._on_operation_definition_in,
                "InlineFragment": self._on_inline_fragment_in,
            },
            {
                "default": self._out,
                "Argument": self._on_argument_out,
                "Field": self._on_field_out,
                "VariableDefinition": self._on_variable_definition_out,
                "FragmentDefinition": self._on_fragment_definition_out,
                "FragmentSpread": self._on_fragment_spread_out,
                "OperationDefinition": self._on_operation_definition_out,
                "InlineFragment": self._on_inline_fragment_out,
            },
        ]
        self._depth = 0
        self._operation_type = None
        self.root_nodes = []
        self._vars = variables if variables else {}
        self._current_node = None
        self._current_argument_name = None
        self._current_type_condition = None
        self._current_fragment_definition = None
        self._fragments = {}
        self.schema: GraphQLSchema = schema
        self.exception: Exception = None
        self._inline_fragment_type = None

    def _on_argument_in(self, element: _VisitorElement):
        self._current_argument_name = element.name

    def _on_argument_out(self, _):
        self._current_argument_name = None

    def _on_value_in(self, element: _VisitorElement):
        if hasattr(self._current_node, "default_value"):
            self._current_node.default_value = element.get_value()
            return

        self._current_node.arguments.update(
            {self._current_argument_name: element.get_value()}
        )

    def _on_variable_in(self, element: _VisitorElement):
        if hasattr(self._current_node, "var_name"):
            self._current_node.var_name = element.name
            return

        try:
            var_name = element.name
            self._current_node.arguments.update(
                {self._current_argument_name: self._vars[var_name]}
            )
        except KeyError:
            self.continue_child = 0
            self.exception = UnknownVariableException(var_name)

    def _on_field_in(self, element: _VisitorElement):
        self.field_path.append(element.name)
        self._depth = self._depth + 1

        try:
            parent_type = reduce_type(
                self._current_node.field_executor.schema_field.gql_type
            )
        except (AttributeError, TypeError):
            parent_type = self.schema.find_type(
                self.schema.get_operation_type(self._operation_type)
            )

        try:
            field = self.schema.get_field_by_name(
                str(parent_type) + "." + element.name
            )
        except UnknownSchemaFieldResolver as e:
            try:
                field = self.schema.get_field_by_name(
                    self._inline_fragment_type + "." + element.name
                )
            except UnknownSchemaFieldResolver as e:
                self.continue_child = 0
                self.exception = e
                return

        node = NodeField(
            element.name,
            self.schema,
            field.resolver,
            element.get_location(),
            self.field_path[:],
            self._current_type_condition,
            element.get_alias(),
        )

        node.set_parent(self._current_node)
        if self._current_node:
            self._current_node.add_child(node)

        self._current_node = node

        if self._depth == 1:
            self.root_nodes.append(node)

    def _on_field_out(self, _):
        self._depth = self._depth - 1
        self.field_path.pop()
        self._current_node = self._current_node.parent

    def _on_variable_definition_in(self, element: _VisitorElement):
        node = NodeVariableDefinition(
            self.path, element.get_location(), element.name
        )
        node.set_parent(self._current_node)
        self._current_node = node

    def _validate_type(self, varname, a_value, a_type):
        try:
            if not isinstance(a_value, a_type):
                self.continue_child = 0
                self.exception = TypeError(
                    "Given value for < %s > is not type < %s >"
                    % (varname, a_type)
                )
        except TypeError:
            # TODO remove this, and handle the case it's an InputValue
            # (look at registered input values and compare fields)
            pass

    def _validates_vars(self):
        # validate given var are okay
        name = self._current_node.var_name
        if name not in self._vars:
            dfv = self._current_node.default_value
            if not dfv and not self._current_node.is_nullable:
                self.continue_child = 0
                self.exception = UnknownVariableException(name)
                return None

            self._vars[name] = dfv
            return None

        a_type = self._current_node.var_type
        a_value = self._vars[name]

        if self._current_node.is_list:
            if not isinstance(a_value, list):
                self.continue_child = 0
                self.exception = TypeError(
                    "Expecting List for < %s > values" % name
                )
                return None

            for val in a_value:
                self._validate_type(name, val, a_type)
            return None

        self._validate_type(name, a_value, a_type)
        return None

    def _on_variable_definition_out(self, _):
        self._validates_vars()
        # now the VariableDefinition Node is useless so kill it
        self._current_node = self._current_node.parent

    def _on_named_type_in(self, element: _VisitorElement):
        try:
            self._current_node.var_type = element.name
        except AttributeError:
            pass

    def _on_list_type_in(self, _):
        try:
            self._current_node.is_list = True
        except AttributeError:
            pass

    def _on_non_null_type_in(self, _):
        self._current_node.is_nullable = False

    def _on_fragment_definition_in(self, element: _VisitorElement):
        if element.name in self._fragments:
            self.continue_child = 0
            self.exception = TartifletteException(
                "Fragment < %s > already defined" % element.name
            )
            return

        nfd = NodeFragmentDefinition(
            self.path,
            element.get_location(),
            element.name,
            type_condition=element.get_type_condition(),
        )

        self._current_fragment_definition = nfd
        self._fragments[element.name] = nfd

    def _on_fragment_definition_out(self, _):
        self._current_fragment_definition = None

    def _on_fragment_spread_out(self, element: _VisitorElement):
        cfd = self._fragments[element.name]
        self._current_type_condition = cfd.type_condition
        for saved_callback in cfd.callbacks:
            saved_callback()  # Simulate calling a the right place.
        self._current_type_condition = None

    def _on_operation_definition_in(
        self, element: _VisitorElementOperationDefinition
    ):
        self._operation_type = element.get_operation()

    def _on_operation_definition_out(self, _):
        self._operation_type = None

    def _on_inline_fragment_in(self, element):
        self._inline_fragment_type = element.get_named_type()
        self._current_type_condition = self._inline_fragment_type

    def _on_inline_fragment_out(self, _):
        self._inline_fragment_type = None
        self._current_type_condition = None

    def _in(self, element: _VisitorElement):
        self.path = self.path + "/%s" % TartifletteVisitor.create_node_name(
            element.libgraphql_type, element.name
        )

        try:
            self._events[self.IN][element.libgraphql_type](element)
        except KeyError:
            pass

    def _out(self, element: _VisitorElement):
        self.path = "/".join(self.path.split("/")[:-1])

        try:
            self._events[self.OUT][element.libgraphql_type](element)
        except KeyError:
            pass

    def update(self, event, element: _VisitorElement):
        self.continue_child = 1
        self.event = event

        if element.libgraphql_type in ["SelectionSet"]:
            return  # because we don't care.

        if (
            not self._current_fragment_definition
            or element.libgraphql_type == "FragmentDefinition"
        ):
            # Always execute FragmentDefinitions Handlers,
            # never exec if in fragment.
            self._events[self.event]["default"](element)
        else:
            self._current_fragment_definition.callbacks.append(
                partial(self._events[self.event]["default"], element)
            )
