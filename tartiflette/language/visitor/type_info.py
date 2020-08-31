from typing import Any, Callable, List, Optional, Union

from tartiflette.language.ast.base import Node
from tartiflette.language.visitor.constants import OK
from tartiflette.language.visitor.utils import get_visit_function
from tartiflette.language.visitor.visitor import Visitor
from tartiflette.types.helpers.definition import (
    get_wrapped_type,
    is_composite_type,
    is_enum_type,
    is_input_object_type,
    is_input_type,
    is_interface_type,
    is_list_type,
    is_non_null_type,
    is_object_type,
    is_output_type,
)
from tartiflette.utils.type_from_ast import schema_type_from_ast

__all__ = (
    "get_nullable_type",
    "TypeInfo",
    "WithTypeInfoVisitor",
)


def get_nullable_type(gql_type: "GraphQLType") -> "GraphQLType":
    """
    Return the wrapped type from a non-nullable type.
    :param gql_type: the GraphQLType to unwrap
    :type gql_type: GraphQLType
    :return: the wrapped type from a non-nullable type
    :rtype: GraphQLType
    """
    return gql_type.wrapped_type if is_non_null_type(gql_type) else gql_type


def _get_field_def(
    schema: "GraphQLSchema",
    parent_type: "GraphQLType",
    field_node: "FieldNode",
) -> Optional["GraphQLField"]:
    """
    Fetch the appropriate GraphQLField definition.
    :param schema: the related GraphQLSchema instance
    :param parent_type: the parent type of the field node
    :param field_node: the field node instance
    :type schema: GraphQLSchema
    :type parent_type: GraphQLType
    :type field_node: FieldNode
    :return: the GraphQLField definition for parent_type/field_node
    :rtype: Optional[GraphQLField]
    """
    field_name = field_node.name.value
    if field_name == "__schema" and schema.queryType is parent_type:
        return schema.queryType.find_field("__schema")
    if field_name == "__type" and schema.queryType is parent_type:
        return schema.queryType.find_field("__type")
    if field_name == "__typename" and is_composite_type(parent_type):
        return parent_type.find_field("__typename")
    if (
        is_object_type(parent_type) or is_interface_type(parent_type)
    ) and parent_type.has_field(field_name):
        return parent_type.find_field(field_name)
    return None


class TypeInfo(Visitor):
    """
    Utility class which keep track of some information while visiting.
    """

    def __init__(
        self,
        schema: "GraphQLSchema",
        get_field_def_fn: Optional[Callable] = None,
        initial_type: Optional["GraphQLType"] = None,
    ) -> None:
        """
        :param schema: the related GraphQLSchema instance
        :param get_field_def_fn: callable to use to fetch field definition
        :param initial_type: ease visits beginning elsewhere than DocumentNode
        :type schema: GraphQLSchema
        :type get_field_def_fn: Optional[Callable]
        :type initial_type: Optional[GraphQLType]
        """
        self._schema = schema
        self._get_field_def = get_field_def_fn or _get_field_def

        self._type_stack: List["GraphQLOutputType"] = []
        self._parent_type_stack: List["GraphQLCompositeType"] = []
        self._input_type_stack: List["GraphQLInputType"] = []
        self._field_def_stack: List["GraphQLField"] = []
        self._default_value_stack: List[Any] = []
        self._directive: Optional["GraphQLDirective"] = None
        self._argument: Optional["GraphQLArgument"] = None
        self._enum_value: Optional["GraphQLEnumValue"] = None

        if initial_type:
            if is_input_type(initial_type):
                self._input_type_stack.append(initial_type)
            if is_composite_type(initial_type):
                self._parent_type_stack.append(initial_type)
            if is_output_type(initial_type):
                self._type_stack.append(initial_type)

    def get_type(self) -> Optional["GraphQLOutputType"]:
        """
        Return the current GraphQLOutputType if one.
        :return: the current GraphQLOutputType if one
        :rtype: Optional[GraphQLOutputType]
        """
        return self._type_stack[-1] if self._type_stack else None

    def get_parent_type(self) -> Optional["GraphQLCompositeType"]:
        """
        Return the GraphQLCompositeType parent type if one.
        :return: the GraphQLCompositeType parent type if one
        :rtype: Optional[GraphQLCompositeType]
        """
        return self._parent_type_stack[-1] if self._parent_type_stack else None

    def get_input_type(self) -> Optional["GraphQLInputType"]:
        """
        Return the current GraphQLInputType if one.
        :return: the current GraphQLInputType if one
        :rtype: Optional[GraphQLInputType]
        """
        return self._input_type_stack[-1] if self._input_type_stack else None

    def get_parent_input_type(self) -> Optional["GraphQLInputType"]:
        """
        Return the parent GraphQLInputType if one.
        :return: the parent GraphQLInputType if one
        :rtype: Optional[GraphQLInputType]
        """
        return (
            self._input_type_stack[-2]
            if len(self._input_type_stack) > 1
            else None
        )

    def get_field_def(self) -> Optional["GraphQLField"]:
        """
        Return the current GraphQLField if one.
        :return: the current GraphQLField if one
        :rtype: Optional[GraphQLField]
        """
        return self._field_def_stack[-1] if self._field_def_stack else None

    def get_default_value(self) -> Optional[Any]:
        """
        Return the current default value if one.
        :return: the current default value if one
        :rtype: Optional[Any]
        """
        return (
            self._default_value_stack[-1]
            if self._default_value_stack
            else None
        )

    def get_directive(self) -> Optional["GraphQLDirective"]:
        """
        Return the current GraphQLDirective if one.
        :return: the current GraphQLDirective if one
        :rtype: Optional[GraphQLDirective]
        """
        return self._directive

    def get_argument(self) -> Optional["GraphQLArgument"]:
        """
        Return the current GraphQLArgument if one.
        :return: the current GraphQLArgument if one
        :rtype: Optional[GraphQLArgument]
        """
        return self._argument

    def get_enum_value(self) -> Optional["GraphQLEnumValue"]:
        """
        Return the current GraphQLEnumValue if one.
        :return: the current GraphQLEnumValue if one
        :rtype: Optional[GraphQLEnumValue]
        """
        return self._enum_value

    def enter(self, node: "Node") -> Optional[Any]:
        """
        Visit the go in node to trigger the appropriate enter method.
        :return: Node
        :rtype: the result of the enter method or None
        """
        fn = getattr(self, "enter_" + node.__class__.__name__[:-4], None)
        return fn(node) if fn else None

    def enter_SelectionSet(  # pylint: disable=invalid-name
        self, node: "SelectionSetNode"
    ) -> None:
        """
        Visit a SelectionSetNode to update stack attributes.
        :param node: the current node being visiting
        :type node: SelectionSetNode
        """
        # pylint: disable=unused-argument
        named_type = get_wrapped_type(self.get_type())
        self._parent_type_stack.append(
            named_type if is_composite_type(named_type) else None
        )

    def enter_Field(  # pylint: disable=invalid-name
        self, node: "FieldNode"
    ) -> None:
        """
        Visit a FieldNode to update stack attributes.
        :param node: the current node being visiting
        :type node: FieldNode
        """
        parent_type = self.get_parent_type()
        if parent_type:
            field_def = self._get_field_def(self._schema, parent_type, node)
            field_type = field_def.graphql_type if field_def else None
        else:
            field_def = field_type = None

        self._field_def_stack.append(field_def)
        self._type_stack.append(
            field_type if is_output_type(field_type) else None
        )

    def enter_Directive(  # pylint: disable=invalid-name
        self, node: "DirectiveNode"
    ) -> None:
        """
        Visit a DirectiveNode to update stack attributes.
        :param node: the current node being visiting
        :type node: DirectiveNode
        """
        directive_name = node.name.value
        self._directive = (
            self._schema.find_directive(directive_name)
            if self._schema.has_directive(directive_name)
            else None
        )

    def enter_OperationDefinition(  # pylint: disable=invalid-name
        self, node: "OperationDefinitionNode"
    ) -> None:
        """
        Visit a OperationDefinitionNode to update stack attributes.
        :param node: the current node being visiting
        :type node: OperationDefinitionNode
        """
        operation_type = getattr(
            self._schema, f"{node.operation_type}Type", None
        )
        self._type_stack.append(
            operation_type if is_object_type(operation_type) else None
        )

    def _enter_inline_or_definition_fragment(
        self, node: Union["InlineFragmentNode", "FragmentDefinitionNode"]
    ) -> None:
        """
        Visit a InlineFragmentNode or FragmentDefinitionNode to update
        stack attributes.
        :param node: the current node being visiting
        :type node: Union[InlineFragmentNode, FragmentDefinitionNode]
        """
        type_condition_node = node.type_condition
        output_type = (
            schema_type_from_ast(self._schema, type_condition_node)
            if type_condition_node
            else get_wrapped_type(self.get_type())
        )
        self._type_stack.append(
            output_type if is_output_type(output_type) else None
        )

    enter_InlineFragment = _enter_inline_or_definition_fragment
    enter_FragmentDefinition = _enter_inline_or_definition_fragment

    def enter_VariableDefinition(  # pylint: disable=invalid-name
        self, node: "VariableDefinitionNode"
    ) -> None:
        """
        Visit a VariableDefinitionNode to update stack attributes.
        :param node: the current node being visiting
        :type node: VariableDefinitionNode
        """
        input_type = schema_type_from_ast(self._schema, node.type)
        self._input_type_stack.append(
            input_type if is_input_type(input_type) else None
        )

    def enter_Argument(  # pylint: disable=invalid-name
        self, node: "ArgumentNode"
    ) -> None:
        """
        Visit a ArgumentNode to update stack attributes.
        :param node: the current node being visiting
        :type node: ArgumentNode
        """
        directive_or_field = self.get_directive() or self.get_field_def()
        if directive_or_field:
            arg_def = directive_or_field.arguments.get(node.name.value)
            arg_type = arg_def.graphql_type if arg_def else None
        else:
            arg_def = arg_type = None

        self._argument = arg_def
        self._default_value_stack.append(
            arg_def.default_value if arg_def else None
        )
        self._input_type_stack.append(
            arg_type if is_input_type(arg_type) else None
        )

    def enter_ListValue(  # pylint: disable=invalid-name
        self, node: "ListValueNode"
    ) -> None:
        """
        Visit a ListValueNode to update stack attributes.
        :param node: the current node being visiting
        :type node: ListValueNode
        """
        # pylint: disable=unused-argument
        list_type = get_nullable_type(self.get_input_type())
        item_type = (
            list_type.wrapped_type if is_list_type(list_type) else list_type
        )
        self._default_value_stack.append(None)
        self._input_type_stack.append(
            item_type if is_input_type(item_type) else None
        )

    def enter_ObjectField(  # pylint: disable=invalid-name
        self, node: "ObjectFieldNode"
    ) -> None:
        """
        Visit a ObjectFieldNode to update stack attributes.
        :param node: the current node being visiting
        :type node: ObjectFieldNode
        """
        object_type = get_wrapped_type(self.get_input_type())
        if is_input_object_type(object_type):
            input_field = object_type.input_fields.get(node.name.value)
            input_field_type = (
                input_field.graphql_type if input_field else None
            )
        else:
            input_field = input_field_type = None
        self._default_value_stack.append(
            input_field.default_value if input_field else None
        )
        self._input_type_stack.append(
            input_field_type if is_input_type(input_field_type) else None
        )

    def enter_EnumValue(  # pylint: disable=invalid-name
        self, node: "EnumValueNode"
    ) -> None:
        """
        Visit a EnumValueNode to update stack attributes.
        :param node: the current node being visiting
        :type node: EnumValueNode
        """
        enum_type = get_wrapped_type(self.get_input_type())
        value = node.value
        self._enum_value = (
            enum_type.get_value(value)
            if is_enum_type(enum_type) and enum_type.has_value(value)
            else None
        )

    def leave(self, node: "Node") -> Optional[Any]:
        """
        Visit the go out node to trigger the appropriate leave method.
        :return: the result of the leave method or None
        :rtype: Node
        """
        fn = getattr(self, "leave_" + node.__class__.__name__[:-4], None)
        return fn() if fn else None

    def leave_SelectionSet(self) -> None:  # pylint: disable=invalid-name
        """
        Visit a SelectionSet to update stack attributes.
        """
        self._parent_type_stack.pop()

    def leave_Field(self) -> None:  # pylint: disable=invalid-name
        """
        Visit a FieldNode to update stack attributes.
        """
        self._field_def_stack.pop()
        self._type_stack.pop()

    def leave_Directive(self) -> None:  # pylint: disable=invalid-name
        """
        Visit a DirectiveNode to update stack attributes.
        """
        self._directive = None

    def _leave_and_pop_type_stack(self) -> None:
        """
        Visit a OperationDefinitionNode, InlineFragmentNode or
        FragmentDefinitionNode to update stack attributes.
        """
        self._type_stack.pop()

    leave_OperationDefinition = _leave_and_pop_type_stack
    leave_InlineFragment = _leave_and_pop_type_stack
    leave_FragmentDefinition = _leave_and_pop_type_stack

    def leave_VariableDefinition(self) -> None:  # pylint: disable=invalid-name
        """
        Visit a VariableDefinitionNode to update stack attributes.
        """
        self._input_type_stack.pop()

    def leave_Argument(self) -> None:  # pylint: disable=invalid-name
        """
        Visit a ArgumentNode to update stack attributes.
        """
        self._argument = None
        self._default_value_stack.pop()
        self._input_type_stack.pop()

    def _leave_object_field_or_list_value(self) -> None:
        """
        Visit a ObjectFieldNode or ListValueNode to update stack
        attributes.
        """
        self._default_value_stack.pop()
        self._input_type_stack.pop()

    leave_ObjectField = _leave_object_field_or_list_value
    leave_ListValue = _leave_object_field_or_list_value

    def leave_EnumValue(self) -> None:  # pylint: disable=invalid-name
        """
        Visit a EnumValueNode to update stack attributes.
        """
        self._enum_value = None


class WithTypeInfoVisitor(Visitor):
    """
    Visitor which maintains a provided TypeInfo instance along with
    visiting visitor.
    """

    def __init__(self, type_info: "TypeInfo", visitor: "Visitor") -> None:
        """
        :param type_info: the TypeInfo instance to maintain
        :param visitor: the Visitor instance to visit
        :type type_info: TypeInfo
        :type visitor: Visitor
        """
        self._type_info = type_info
        self._visitor = visitor

    def enter(
        self,
        node: "Node",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> Optional[Any]:
        """
        Visit the go in node to trigger the appropriate enter method.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: Node
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        :return: the result of the enter method or None
        :rtype: Optional[Any]
        """
        self._type_info.enter(node)
        fn = get_visit_function(self._visitor, node)
        if fn:
            result = fn(node, key, parent, path, ancestors)
            if result is not OK:
                self._type_info.leave(node)
                if isinstance(result, Node):
                    self._type_info.enter(result)
            return result
        return None

    def leave(
        self,
        node: "Node",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> Optional[Any]:
        """
        Visit the go out node to trigger the appropriate leave method.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: Node
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        :return: the result of the leave method or None
        :rtype: Optional[Any]
        """
        fn = get_visit_function(self._visitor, node, is_leaving=True)
        result = fn(node, key, parent, path, ancestors) if fn else None
        self._type_info.leave(node)
        return result
