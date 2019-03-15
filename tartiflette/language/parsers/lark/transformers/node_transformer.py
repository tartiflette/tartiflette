from typing import List, Optional, Union

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
    TODO:
    """

    __slots__ = ("type", "value")

    def __init__(self, type: str, value: Union["Node", List["Node"]]) -> None:
        """
        TODO:
        :param type: TODO:
        :param value: TODO:
        :type type: str
        :type value: Union[Node, List[Node]]
        """
        # pylint: disable=redefined-builtin
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: str
        """
        return "SchemaNode(type=%r, value=%r)" % (self.type, self.value)


@v_args(tree=True)
class NodeTransformer(Transformer_InPlace):
    """
    TODO:
    """

    # pylint: disable=too-many-public-methods

    def __init__(self):
        """
        TODO:
        """
        super().__init__()
        self.document_node: Optional["DocumentNode"] = None

    def int_value(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(type="int_value", value=lark_to_int_value_node(tree))

    def float_value(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="float_value", value=lark_to_float_value_node(tree)
        )

    def string_value(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="string_value", value=lark_to_string_value_node(tree)
        )

    def boolean_value(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="boolean_value", value=lark_to_boolean_value_node(tree)
        )

    def null_value(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="null_value", value=lark_to_null_value_node(tree)
        )

    def enum_value(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="enum_value", value=lark_to_enum_value_node(tree)
        )

    def list_value(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="list_value", value=lark_to_list_value_node(tree)
        )

    def object_field(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="object_field", value=lark_to_object_field_node(tree)
        )

    def object_value(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="object_value", value=lark_to_object_value_node(tree)
        )

    def value(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(type="value", value=tree.children[0].value)

    def name(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(type="name", value=lark_to_name_node(tree))

    def description(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="description", value=lark_to_description_node(tree)
        )

    def named_type(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="named_type", value=lark_to_named_type_node(tree)
        )

    def argument(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(type="argument", value=lark_to_argument_node(tree))

    def arguments(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="arguments", value=[token.value for token in tree.children]
        )

    def directive(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(type="directive", value=lark_to_directive_node(tree))

    def directives(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="directives", value=[child.value for child in tree.children]
        )

    def operation_type(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(type="operation_type", value=tree.children[0].value)

    def operation_type_definition(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="operation_type_definition",
            value=lark_to_operation_type_definition_node(tree),
        )

    def schema_definition(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="schema_definition",
            value=lark_to_schema_definition_node(tree),
        )

    def scalar_type_definition(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="scalar_type_definition",
            value=lark_to_scalar_type_definition_node(tree),
        )

    def list_type(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(type="list_type", value=lark_to_list_type_node(tree))

    def non_null_type(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="non_null_type", value=lark_to_non_null_type_node(tree)
        )

    def type(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(type="type", value=tree.children[0].value)

    def default_value(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(type="default_value", value=tree.children[0].value)

    def input_value_definition(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="input_value_definition",
            value=lark_to_input_value_definition_node(tree),
        )

    def arguments_definition(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="arguments_definition",
            value=[child.value for child in tree.children],
        )

    def directive_location(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="directive_location", value=lark_to_name_node(tree)
        )

    def directive_locations(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :return: TODO:
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="directive_locations",
            value=[child.value for child in tree.children],
        )

    def directive_definition(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="directive_definition",
            value=lark_to_directive_definition_node(tree),
        )

    def implements_interfaces(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="implements_interfaces",
            value=lark_to_implements_interfaces_node(tree),
        )

    def field_definition(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="field_definition", value=lark_to_field_definition_node(tree)
        )

    def fields_definition(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="fields_definition",
            value=[child.value for child in tree.children],
        )

    def object_type_definition(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="object_type_definition",
            value=lark_to_object_type_definition_node(tree),
        )

    def interface_type_definition(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="interface_type_definition",
            value=lark_to_interface_type_definition_node(tree),
        )

    def union_member_types(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="union_member_types",
            value=[child.value for child in tree.children],
        )

    def union_type_definition(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="union_type_definition",
            value=lark_to_union_type_definition_node(tree),
        )

    def enum_value_definition(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="enum_value_definition",
            value=lark_to_enum_value_definition_node(tree),
        )

    def enum_values_definition(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="enum_values_definition",
            value=[child.value for child in tree.children],
        )

    def enum_type_definition(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="enum_type_definition",
            value=lark_to_enum_type_definition_node(tree),
        )

    def input_fields_definition(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="input_fields_definition",
            value=[child.value for child in tree.children],
        )

    def input_object_type_definition(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="input_object_type_definition",
            value=lark_to_input_object_type_definition_node(tree),
        )

    def schema_extension(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="schema_extension", value=lark_to_schema_extension_node(tree)
        )

    def scalar_type_extension(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="scalar_type_extension",
            value=lark_to_scalar_type_extension_node(tree),
        )

    def object_type_extension(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="object_type_extension",
            value=lark_to_object_type_extension_node(tree),
        )

    def interface_type_extension(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="interface_type_extension",
            value=lark_to_interface_type_extension_node(tree),
        )

    def union_type_extension(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="union_type_extension",
            value=lark_to_union_type_extension_node(tree),
        )

    def enum_type_extension(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="enum_type_extension",
            value=lark_to_enum_type_extension_node(tree),
        )

    def input_object_type_extension(self, tree: "Tree") -> "SchemaNode":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: SchemaNode
        """
        # pylint: disable=no-self-use
        return SchemaNode(
            type="input_object_type_extension",
            value=lark_to_input_object_type_extension_node(tree),
        )

    def document(self, tree: "Tree") -> "Tree":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
        :rtype: Tree
        """
        self.document_node = lark_to_document_node(tree)
        return tree
