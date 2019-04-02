from typing import Any, List, Optional, Union

from lark import v_args
from lark.visitors import Transformer_InPlace

from tartiflette.language.parsers.lark.transformers.converters import (
    lark_to_argument_node,
    lark_to_boolean_value_node,
    lark_to_description_node,
    lark_to_directive_definition_node,
    lark_to_directive_node,
    lark_to_document_node,
    lark_to_enum_type_definition_node,
    lark_to_enum_type_extension_node,
    lark_to_enum_value_definition_node,
    lark_to_enum_value_node,
    lark_to_field_definition_node,
    lark_to_float_value_node,
    lark_to_implements_interfaces_node,
    lark_to_input_object_type_definition_node,
    lark_to_input_object_type_extension_node,
    lark_to_input_value_definition_node,
    lark_to_int_value_node,
    lark_to_interface_type_definition_node,
    lark_to_interface_type_extension_node,
    lark_to_list_type_node,
    lark_to_list_value_node,
    lark_to_name_node,
    lark_to_named_type_node,
    lark_to_non_null_type_node,
    lark_to_null_value_node,
    lark_to_object_field_node,
    lark_to_object_type_definition_node,
    lark_to_object_type_extension_node,
    lark_to_object_value_node,
    lark_to_operation_type_definition_node,
    lark_to_scalar_type_definition_node,
    lark_to_scalar_type_extension_node,
    lark_to_schema_definition_node,
    lark_to_schema_extension_node,
    lark_to_string_value_node,
    lark_to_union_type_definition_node,
    lark_to_union_type_extension_node,
)


class SchemaNode:
    """
    A class which fit the lark.Token API to be able to use instances from these
    classes the same way.
    """

    __slots__ = ("type", "value")

    def __init__(self, type: str, value: Union["Node", List["Node"]]) -> None:
        """
        :param type: type of the schema node
        :param value: value of the schema node
        :type type: str
        :type value: Union[Node, List[Node]]
        """
        # pylint: disable=redefined-builtin
        self.type = type
        self.value = value

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, SchemaNode)
            and (self.type == other.type and self.value == other.value)
        )

    def __repr__(self) -> str:
        """
        Returns the representation of an SchemaNode instance.
        :return: the representation of an SchemaNode instance
        :rtype: str
        """
        return "SchemaNode(type=%r, value=%r)" % (self.type, self.value)


@v_args(tree=True)
class NodeTransformer(Transformer_InPlace):
    """
    Parses a Tree previously cleaned with TokenTransformer and builds a
    DocumentNode instance.
    """

    # pylint: disable=too-many-public-methods

    def __init__(self):
        super().__init__()
        self.document_node: Optional["DocumentNode"] = None

    def int_value(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "int_value" with a
        IntValueNode instance as value (extracted from the parsing of the tree
        instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "int_value" with an IntValueNode
        instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(type="int_value", value=lark_to_int_value_node(tree))

    def float_value(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "float_value" with a
        FloatValueNode instance as value (extracted from the parsing of the
        tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "float_value" with a
        FloatValueNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="float_value", value=lark_to_float_value_node(tree)
        )

    def string_value(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "string_value" with a
        StringValueNode instance as value (extracted from the parsing of the
        tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "string_value" with a
        StringValueNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="string_value", value=lark_to_string_value_node(tree)
        )

    def boolean_value(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "boolean_value" with
        a BooleanValueNode instance as value (extracted from the parsing of the
        tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "boolean_value" with a
        BooleanValueNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="boolean_value", value=lark_to_boolean_value_node(tree)
        )

    def null_value(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "null_value" with a
        NullValueNode instance as value (extracted from the parsing of the tree
        instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "null_value" with a
        NullValueNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="null_value", value=lark_to_null_value_node(tree)
        )

    def enum_value(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "enum_value" with an
        EnumValueNode instance as value (extracted from the parsing of the tree
        instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "enum_value" with an
        EnumValueNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="enum_value", value=lark_to_enum_value_node(tree)
        )

    def list_value(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "list_value" with a
        ListValueNode instance as value (extracted from the parsing of the tree
        instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "list_value" with a
        ListValueNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="list_value", value=lark_to_list_value_node(tree)
        )

    def object_field(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "object_field" with
        an ObjectFieldNode instance as value (extracted from the parsing of the
        tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "object_field" with an
        ObjectFieldNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="object_field", value=lark_to_object_field_node(tree)
        )

    def object_value(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "object_value" with
        an ObjectValueNode instance as value (extracted from the parsing of the
        tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "object_value" with an
        ObjectValueNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="object_value", value=lark_to_object_value_node(tree)
        )

    def value(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "value" with a
        ValueNode instance as value (extracted from the parsing of the tree
        instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "value" with a ValueNode
        instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(type="value", value=tree.children[0].value)

    def name(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "name" with a
        NameNode instance as value (extracted from the parsing of the tree
        instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "name" with a NameNode instance
        as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(type="name", value=lark_to_name_node(tree))

    def description(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "description" with a
        DescriptionNode instance as value (extracted from the parsing of the
        tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "description" with a
        DescriptionNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="description", value=lark_to_description_node(tree)
        )

    def named_type(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "named_type" with a
        NamedTypeNode instance as value (extracted from the parsing of the tree
        instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "named_type" with a
        NamedTypeNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="named_type", value=lark_to_named_type_node(tree)
        )

    def argument(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "argument" with a
        ArgumentNode instance as value (extracted from the parsing of the tree
        instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "argument" with an ArgumentNode
        instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(type="argument", value=lark_to_argument_node(tree))

    def arguments(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "arguments" with a
        list of ArgumentNode instance as value (extracted from the parsing of
        the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "arguments" with a list of
        ArgumentNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="arguments", value=[token.value for token in tree.children]
        )

    def directive(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "directive" with a
        DirectiveNode instance as value (extracted from the parsing of the tree
        instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "directive" with a DirectiveNode
        instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(type="directive", value=lark_to_directive_node(tree))

    def directives(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "directives" with a
        list of DirectiveNode instance as value (extracted from the parsing of
        the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "directives" with a list of
        DirectiveNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="directives", value=[child.value for child in tree.children]
        )

    def operation_type(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "operation_type" with
        a string as value (extracted from the parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "operation_type" with a string
        as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(type="operation_type", value=tree.children[0].value)

    def operation_type_definition(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type
        "operation_type_definition" with an OperationTypeDefinitionNode
        instance as value (extracted from the parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "operation_type_definition" with
        an OperationTypeDefinitionNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="operation_type_definition",
            value=lark_to_operation_type_definition_node(tree),
        )

    def schema_definition(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "schema_definition"
        with a SchemaDefinitionNode instance as value (extracted from the
        parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "schema_definition" with a
        SchemaDefinitionNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="schema_definition",
            value=lark_to_schema_definition_node(tree),
        )

    def scalar_type_definition(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type
        "scalar_type_definition" with a ScalarTypeDefinitionNode instance as
        value (extracted from the parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "scalar_type_definition" with a
        ScalarTypeDefinitionNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="scalar_type_definition",
            value=lark_to_scalar_type_definition_node(tree),
        )

    def list_type(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "list_type" with a
        ListTypeNode instance as value (extracted from the parsing of the tree
        instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "list_type" with a ListTypeNode
        instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(type="list_type", value=lark_to_list_type_node(tree))

    def non_null_type(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "non_null_type" with
        a NonNullTypeNode instance as value (extracted from the parsing of the
        tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "non_null_type" with a
        NonNullTypeNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="non_null_type", value=lark_to_non_null_type_node(tree)
        )

    def type(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "type" with a
        TypeNode instance as value (extracted from the parsing of the tree
        instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "type" with a TypeNode instance
        as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(type="type", value=tree.children[0].value)

    def default_value(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "default_value" with
        a ValueNode instance as value (extracted from the parsing of the tree
        instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "default_value" with a ValueNode
        instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(type="default_value", value=tree.children[0].value)

    def input_value_definition(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type
        "input_value_definition" with an InputValueDefinitionNode instance
        as value (extracted from the parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "input_value_definition" with an
        InputValueDefinitionNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="input_value_definition",
            value=lark_to_input_value_definition_node(tree),
        )

    def arguments_definition(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type
        "arguments_definition" with a list of InputValueDefinitionNode instance
        as value (extracted from the parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "arguments_definition" with a
        list of InputValueDefinitionNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="arguments_definition",
            value=[child.value for child in tree.children],
        )

    def directive_location(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "directive_location"
        with a NameNode instance as value (extracted from the parsing of the
        tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "directive_location" with a
        NameNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="directive_location", value=lark_to_name_node(tree)
        )

    def directive_locations(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "directive_locations"
        with a list of NameNode instance as value (extracted from the parsing
        of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :return: a SchemaNode instance of type "directive_locations" with a
        list of NameNode instance as value
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="directive_locations",
            value=[child.value for child in tree.children],
        )

    def directive_definition(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type
        "directive_definition" with a DirectiveDefinitionNode instance as value
        (extracted from the parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "directive_definition" with a
        DirectiveDefinitionNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="directive_definition",
            value=lark_to_directive_definition_node(tree),
        )

    def implements_interfaces(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type
        "implements_interfaces" with a list of NamedTypeNode instance as value
        (extracted from the parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "implements_interfaces" with a
        list of NamedTypeNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="implements_interfaces",
            value=lark_to_implements_interfaces_node(tree),
        )

    def field_definition(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "field_definition"
        with a FieldDefinitionNode instance as value (extracted from the
        parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "field_definition" with a
        FieldDefinitionNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="field_definition", value=lark_to_field_definition_node(tree)
        )

    def fields_definition(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "fields_definition"
        with a list of FieldDefinitionNode instance as value (extracted from
        the parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "fields_definition" with a list
        of FieldDefinitionNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="fields_definition",
            value=[child.value for child in tree.children],
        )

    def object_type_definition(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type
        "object_type_definition" with an ObjectTypeDefinitionNode instance as
        value (extracted from the parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "object_type_definition" with an
        ObjectTypeDefinitionNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="object_type_definition",
            value=lark_to_object_type_definition_node(tree),
        )

    def interface_type_definition(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type
        "interface_type_definition" with an InterfaceTypeDefinitionNode
        instance as value (extracted from the parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "interface_type_definition" with
        an InterfaceTypeDefinitionNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="interface_type_definition",
            value=lark_to_interface_type_definition_node(tree),
        )

    def union_member_types(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "union_member_types"
        with a list of NamedTypeNode instance as value (extracted from the
        parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "union_member_types" with a list
        of NamedTypeNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="union_member_types",
            value=[child.value for child in tree.children],
        )

    def union_type_definition(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type
        "union_type_definition" with an UnionTypeDefinitionNode instance as
        value (extracted from the parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "union_type_definition" with an
        UnionTypeDefinitionNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="union_type_definition",
            value=lark_to_union_type_definition_node(tree),
        )

    def enum_value_definition(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type
        "enum_value_definition" with an EnumValueDefinitionNode instance as
        value (extracted from the parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "enum_value_definition" with an
        EnumValueDefinitionNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="enum_value_definition",
            value=lark_to_enum_value_definition_node(tree),
        )

    def enum_values_definition(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type
        "enum_values_definition" with a list of EnumValueDefinitionNode
        instance as value (extracted from the parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "enum_values_definition" with a
        list of EnumValueDefinitionNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="enum_values_definition",
            value=[child.value for child in tree.children],
        )

    def enum_type_definition(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type
        "enum_type_definition" with an EnumTypeDefinitionNode instance as value
        (extracted from the parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "enum_type_definition" with an
        EnumTypeDefinitionNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="enum_type_definition",
            value=lark_to_enum_type_definition_node(tree),
        )

    def input_fields_definition(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type
        "input_fields_definition" with a list of InputValueDefinitionNode
        instance as value (extracted from the parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "input_fields_definition" with a
        list of InputValueDefinitionNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="input_fields_definition",
            value=[child.value for child in tree.children],
        )

    def input_object_type_definition(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type
        "input_object_type_definition" with an InputObjectTypeDefinitionNode
        instance as value (extracted from the parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "input_object_type_definition"
        with an InputObjectTypeDefinitionNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="input_object_type_definition",
            value=lark_to_input_object_type_definition_node(tree),
        )

    def schema_extension(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "schema_extension"
        with a SchemaExtensionNode instance as value (extracted from the
        parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "schema_extension" with a
        SchemaExtensionNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="schema_extension", value=lark_to_schema_extension_node(tree)
        )

    def scalar_type_extension(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type
        "scalar_type_extension" with a ScalarTypeExtensionNode instance as
        value (extracted from the parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "scalar_type_extension" with a
        ScalarTypeExtensionNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="scalar_type_extension",
            value=lark_to_scalar_type_extension_node(tree),
        )

    def object_type_extension(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type
        "object_type_extension" with an ObjectTypeExtensionNode instance as
        value (extracted from the parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "object_type_extension" with an
        ObjectTypeExtensionNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="object_type_extension",
            value=lark_to_object_type_extension_node(tree),
        )

    def interface_type_extension(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type
        "interface_type_extension" with an InterfaceTypeExtensionNode instance
        as value (extracted from the parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "interface_type_extension" with
        an InterfaceTypeExtensionNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="interface_type_extension",
            value=lark_to_interface_type_extension_node(tree),
        )

    def union_type_extension(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type
        "union_type_extension" with an UnionTypeExtensionNode instance as value
        (extracted from the parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "union_type_extension" with an
        UnionTypeExtensionNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="union_type_extension",
            value=lark_to_union_type_extension_node(tree),
        )

    def enum_type_extension(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type "enum_type_extension"
        with an EnumTypeExtensionNode instance as value (extracted from the
        parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "enum_type_extension" with an
        EnumTypeExtensionNode instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="enum_type_extension",
            value=lark_to_enum_type_extension_node(tree),
        )

    def input_object_type_extension(self, tree: "Tree") -> "SchemaNode":
        """
        Creates and returns a SchemaNode instance of type
        "input_object_type_extension" with an InputObjectTypeExtension instance
        as value (extracted from the parsing of the tree instance).
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: a SchemaNode instance of type "input_object_type_extension"
        with an InputObjectTypeExtension instance as value
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="input_object_type_extension",
            value=lark_to_input_object_type_extension_node(tree),
        )

    def document(self, tree: "Tree") -> "Tree":
        """
        Extracts the DocumentNode from the parsing of the tree instance and set
        it to the document node attribute instance.
        :param tree: the Tree to parse in order to extract the proper node
        :type tree: Tree
        :return: the tree instance
        :rtype: Tree
        """
        self.document_node = lark_to_document_node(tree)
        return tree
