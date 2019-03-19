from typing import Any, Dict, List, Optional, Union

from tartiflette.language.ast import (
    ArgumentNode,
    BooleanValueNode,
    DescriptionNode,
    DirectiveDefinitionNode,
    DirectiveNode,
    DocumentNode,
    EnumTypeDefinitionNode,
    EnumTypeExtensionNode,
    EnumValueDefinitionNode,
    EnumValueNode,
    FieldDefinitionNode,
    FloatValueNode,
    InputObjectTypeDefinitionNode,
    InputObjectTypeExtension,
    InputValueDefinitionNode,
    InterfaceTypeDefinitionNode,
    InterfaceTypeExtensionNode,
    IntValueNode,
    ListTypeNode,
    ListValueNode,
    Location,
    NamedTypeNode,
    NameNode,
    NonNullTypeNode,
    NullValueNode,
    ObjectFieldNode,
    ObjectTypeDefinitionNode,
    ObjectTypeExtensionNode,
    ObjectValueNode,
    OperationTypeDefinitionNode,
    ScalarTypeDefinitionNode,
    ScalarTypeExtensionNode,
    SchemaDefinitionNode,
    SchemaExtensionNode,
    StringValueNode,
    UnionTypeDefinitionNode,
    UnionTypeExtensionNode,
)


class UnexpectedASTNode(Exception):
    """
    Raised when an unexpected node type is encoutered.
    """


def _extract_node_info(
    children: List[Union["Token", "SchemaNode"]],
    types_to_value: Optional[List[str]] = None,
    types_to_list: Optional[Dict[str, str]] = None,
    types_to_ignore: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Extracts information from a node's children depending on the parameters
    options.
    :param children: list of child to parse and from which we should extract
    information
    :param types_to_value: list of child types for which we should add the
    value to the returned information
    :param types_to_list: mapping of child type to returned information key.
    The key must be the type of children and the value the key where all
    matched children will be stored in the returned information
    :param types_to_ignore: list of node type we should ignore
    :type children: List[Union[Token, SchemaNode]]
    :type types_to_value: Optional[List[str]]
    :type types_to_list: Optional[Dict[str, str]]
    :type types_to_ignore: Optional[List[str]]
    :return: a dictionary containing data extracted from children
    :rtype: Dict[str, Any]
    :raises UnexpectedASTNode: raised when an unexpected type is encountered
    """
    types_to_value = types_to_value or []
    types_to_list = types_to_list or {}
    types_to_ignore = types_to_ignore or []

    info = {type_to_list: [] for type_to_list in types_to_list.values()}
    for child in children:
        if child.type in types_to_value:
            info[child.type] = child.value
        elif child.type in types_to_list:
            info[types_to_list[child.type]].append(child)
        elif child.type in types_to_ignore:
            pass
        else:
            raise UnexpectedASTNode(
                "Unexpected AST node `{}`, type `{}`".format(
                    child, child.__class__.__name__
                )
            )
    return info


def lark_to_location_node(tree_meta: "Meta") -> "Location":
    """
    Creates and returns a Location instance from a Tree Meta instance.
    :param tree_meta: Tree Meta Lark instance containing metadata
    :type tree_meta: Meta
    :return: a Location instance
    :rtype: Location
    """
    return Location(
        line=tree_meta.line,
        column=tree_meta.column,
        line_end=tree_meta.end_line,
        column_end=tree_meta.end_column,
    )


def lark_to_int_value_node(tree: "Tree") -> "IntValueNode":
    """
    Creates and returns an IntValueNode instance extracted from the parsing of
    the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: an IntValueNode instance extracted from the parsing of the tree
    :rtype: IntValueNode
    """
    return IntValueNode(
        value=tree.children[0].value, location=lark_to_location_node(tree.meta)
    )


def lark_to_float_value_node(tree: "Tree") -> "FloatValueNode":
    """
    Creates and returns a FloatValueNode instance extracted from the parsing of
    the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: a FloatValueNode instance extracted from the parsing of the tree
    :rtype: FloatValueNode
    """
    return FloatValueNode(
        value=tree.children[0].value, location=lark_to_location_node(tree.meta)
    )


def lark_to_string_value_node(tree: "Tree") -> "StringValueNode":
    """
    Creates and returns a StringValueNode instance extracted from the parsing
    of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: a StringValueNode instance extracted from the parsing of the tree
    :rtype: StringValueNode
    """
    return StringValueNode(
        value=tree.children[0].value, location=lark_to_location_node(tree.meta)
    )


def lark_to_boolean_value_node(tree: "Tree") -> "BooleanValueNode":
    """
    Creates and returns a BooleanValueNode instance extracted from the parsing
    of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: a BooleanValueNode instance extracted from the parsing of the tree
    :rtype: BooleanValueNode
    """
    return BooleanValueNode(
        value=tree.children[0].value, location=lark_to_location_node(tree.meta)
    )


def lark_to_null_value_node(tree: "Tree") -> "NullValueNode":
    """
    Creates and returns a NullValueNode instance extracted from the parsing of
    the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: a NullValueNode instance extracted from the parsing of the tree
    :rtype: NullValueNode
    """
    return NullValueNode(location=lark_to_location_node(tree.meta))


def lark_to_enum_value_node(tree: "Tree") -> "EnumValueNode":
    """
    Creates and returns an EnumValueNode instance extracted from the parsing of
    the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: an EnumValueNode instance extracted from the parsing of the tree
    :rtype: EnumValueNode
    """
    return EnumValueNode(
        value=tree.children[0].value, location=lark_to_location_node(tree.meta)
    )


def lark_to_list_value_node(tree: "Tree") -> "ListValueNode":
    """
    Creates and returns a ListValueNode instance extracted from the parsing of
    the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: a ListValueNode instance extracted from the parsing of the tree
    :rtype: ListValueNode
    """
    return ListValueNode(
        values=[child.value for child in tree.children],
        location=lark_to_location_node(tree.meta),
    )


def lark_to_object_field_node(tree: "Tree") -> "ObjectFieldNode":
    """
    Creates and returns an ObjectFieldNode instance extracted from the parsing
    of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: an ObjectFieldNode instance extracted from the parsing of the tree
    :rtype: ObjectFieldNode
    """
    node_info = _extract_node_info(
        tree.children, types_to_value=["name", "value"]
    )

    return ObjectFieldNode(
        name=node_info["name"],
        value=node_info["value"],
        location=lark_to_location_node(tree.meta),
    )


def lark_to_object_value_node(tree: "Tree") -> "ObjectValueNode":
    """
    Creates and returns an ObjectValueNode instance extracted from the parsing
    of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: an ObjectValueNode instance extracted from the parsing of the tree
    :rtype: ObjectValueNode
    """
    return ObjectValueNode(
        fields=[child.value for child in tree.children],
        location=lark_to_location_node(tree.meta),
    )


def lark_to_name_node(tree: "Tree") -> "NameNode":
    """
    Creates and returns a NameNode instance extracted from the parsing of the
    tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: a NameNode instance extracted from the parsing of the tree
    :rtype: NameNode
    """
    return NameNode(
        value=tree.children[0].value, location=lark_to_location_node(tree.meta)
    )


def lark_to_description_node(tree: "Tree") -> "DescriptionNode":
    """
    Creates and returns a DescriptionNode instance extracted from the parsing
    of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: a DescriptionNode instance extracted from the parsing of the tree
    :rtype: DescriptionNode
    """
    return DescriptionNode(
        value=tree.children[0].value, location=lark_to_location_node(tree.meta)
    )


def lark_to_named_type_node(tree: "Tree") -> "NamedTypeNode":
    """
    Creates and returns a NamedTypeNode instance extracted from the parsing of
    the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: a NamedTypeNode instance extracted from the parsing of the tree
    :rtype: NamedTypeNode
    """
    return NamedTypeNode(
        name=tree.children[0].value, location=lark_to_location_node(tree.meta)
    )


def lark_to_argument_node(tree: "Tree") -> "ArgumentNode":
    """
    Creates and returns an ArgumentNode instance extracted from the parsing of
    the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: an ArgumentNode instance extracted from the parsing of the tree
    :rtype: ArgumentNode
    """
    node_info = _extract_node_info(
        tree.children, types_to_value=["name", "value"]
    )

    return ArgumentNode(
        name=node_info["name"],
        value=node_info["value"],
        location=lark_to_location_node(tree.meta),
    )


def lark_to_directive_node(tree: "Tree") -> "DirectiveNode":
    """
    Creates and returns a DirectiveNode instance extracted from the parsing of
    the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: a DirectiveNode instance extracted from the parsing of the tree
    :rtype: DirectiveNode
    """
    node_info = _extract_node_info(
        tree.children, types_to_value=["name", "arguments"]
    )

    return DirectiveNode(
        name=node_info["name"],
        arguments=node_info.get("arguments") or [],
        location=lark_to_location_node(tree.meta),
    )


def lark_to_operation_type_definition_node(
    tree: "Tree"
) -> "OperationTypeDefinitionNode":
    """
    Creates and returns an OperationTypeDefinitionNode instance extracted from
    the parsing of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: an OperationTypeDefinitionNode instance extracted from the parsing
    of the tree
    :rtype: OperationTypeDefinitionNode
    """
    node_info = _extract_node_info(
        tree.children, types_to_value=["operation_type", "named_type"]
    )

    return OperationTypeDefinitionNode(
        operation_type=node_info["operation_type"],
        type=node_info["named_type"],
        location=lark_to_location_node(tree.meta),
    )


def lark_to_schema_definition_node(tree: "Tree") -> "SchemaDefinitionNode":
    """
    Creates and returns a SchemaDefinitionNode instance extracted from the
    parsing of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: a SchemaDefinitionNode instance extracted from the parsing of the
    tree
    :rtype: SchemaDefinitionNode
    """
    node_info = _extract_node_info(
        tree.children,
        types_to_value=["directives"],
        types_to_list={
            "operation_type_definition": "operation_type_definitions"
        },
        types_to_ignore=["SCHEMA"],
    )

    return SchemaDefinitionNode(
        directives=node_info.get("directives") or [],
        operation_type_definitions=[
            operation_type_definition.value
            for operation_type_definition in node_info.get(
                "operation_type_definitions"
            )
            or []
        ],
        location=lark_to_location_node(tree.meta),
    )


def lark_to_scalar_type_definition_node(
    tree: "Tree"
) -> "ScalarTypeDefinitionNode":
    """
    Creates and returns a ScalarTypeDefinitionNode instance extracted from the
    parsing of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: a ScalarTypeDefinitionNode instance extracted from the parsing of
    the tree
    :rtype: ScalarTypeDefinitionNode
    """
    node_info = _extract_node_info(
        tree.children,
        types_to_value=["description", "name", "directives"],
        types_to_ignore=["SCALAR"],
    )

    return ScalarTypeDefinitionNode(
        description=node_info.get("description"),
        name=node_info["name"],
        directives=node_info.get("directives") or [],
        location=lark_to_location_node(tree.meta),
    )


def lark_to_list_type_node(tree: "Tree") -> "ListTypeNode":
    """
    Creates and returns a ListTypeNode instance extracted from the parsing of
    the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: a ListTypeNode instance extracted from the parsing of the tree
    :rtype: ListTypeNode
    """
    return ListTypeNode(
        type=tree.children[0].value, location=lark_to_location_node(tree.meta)
    )


def lark_to_non_null_type_node(tree: "Tree") -> "NonNullTypeNode":
    """
    Creates and returns a NonNullTypeNode instance extracted from the parsing
    of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: a NonNullTypeNode instance extracted from the parsing of the tree
    :rtype: NonNullTypeNode
    """
    return NonNullTypeNode(
        type=tree.children[0].value, location=lark_to_location_node(tree.meta)
    )


def lark_to_input_value_definition_node(
    tree: "Tree"
) -> "InputValueDefinitionNode":
    """
    Creates and returns an InputValueDefinitionNode instance extracted from the
    parsing of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: an InputValueDefinitionNode instance extracted from the parsing of
    the tree
    :rtype: InputValueDefinitionNode
    """
    node_info = _extract_node_info(
        tree.children,
        types_to_value=[
            "description",
            "name",
            "type",
            "default_value",
            "directives",
        ],
    )

    return InputValueDefinitionNode(
        description=node_info.get("description"),
        name=node_info["name"],
        type=node_info["type"],
        default_value=node_info.get("default_value"),
        directives=node_info.get("directives") or [],
        location=lark_to_location_node(tree.meta),
    )


def lark_to_directive_definition_node(
    tree: "Tree"
) -> "DirectiveDefinitionNode":
    """
    Creates and returns a DirectiveDefinitionNode instance extracted from the
    parsing of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: a DirectiveDefinitionNode instance extracted from the parsing of
    the tree
    :rtype: DirectiveDefinitionNode
    """
    node_info = _extract_node_info(
        tree.children,
        types_to_value=[
            "description",
            "name",
            "arguments_definition",
            "directive_locations",
        ],
        types_to_ignore=["DIRECTIVE", "ON"],
    )

    return DirectiveDefinitionNode(
        description=node_info.get("description"),
        name=node_info["name"],
        arguments=node_info.get("arguments_definition") or [],
        locations=node_info.get("directive_locations") or [],
        location=lark_to_location_node(tree.meta),
    )


def lark_to_implements_interfaces_node(tree: "Tree") -> List["NamedTypeNode"]:
    """
    Creates and returns a list of NamedTypeNode instance extracted from the
    parsing of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: a list of NamedTypeNode instance extracted from the parsing of the
    tree
    :rtype: List[NamedTypeNode]
    """
    node_info = _extract_node_info(
        tree.children,
        types_to_list={"named_type": "named_types"},
        types_to_ignore=["IMPLEMENTS"],
    )

    return [
        named_type.value for named_type in node_info.get("named_types") or []
    ]


def lark_to_field_definition_node(tree: "Tree") -> "FieldDefinitionNode":
    """
    Creates and returns a FieldDefinitionNode instance extracted from the
    parsing of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: a FieldDefinitionNode instance extracted from the parsing of the
    tree
    :rtype: FieldDefinitionNode
    """
    node_info = _extract_node_info(
        tree.children,
        types_to_value=[
            "description",
            "name",
            "arguments_definition",
            "type",
            "directives",
        ],
    )

    return FieldDefinitionNode(
        description=node_info.get("description"),
        name=node_info["name"],
        arguments=node_info.get("arguments_definition") or [],
        type=node_info["type"],
        directives=node_info.get("directives") or [],
        location=lark_to_location_node(tree.meta),
    )


def lark_to_object_type_definition_node(
    tree: "Tree"
) -> "ObjectTypeDefinitionNode":
    """
    Creates and returns an ObjectTypeDefinitionNode instance extracted from the
    parsing of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: an ObjectTypeDefinitionNode instance extracted from the parsing of
    the tree
    :rtype: ObjectTypeDefinitionNode
    """
    node_info = _extract_node_info(
        tree.children,
        types_to_value=[
            "description",
            "name",
            "implements_interfaces",
            "directives",
            "fields_definition",
        ],
        types_to_ignore=["TYPE"],
    )

    return ObjectTypeDefinitionNode(
        description=node_info.get("description"),
        name=node_info["name"],
        interfaces=node_info.get("implements_interfaces") or [],
        directives=node_info.get("directives") or [],
        fields=node_info.get("fields_definition") or [],
        location=lark_to_location_node(tree.meta),
    )


def lark_to_interface_type_definition_node(
    tree: "Tree"
) -> "InterfaceTypeDefinitionNode":
    """
    Creates and returns an InterfaceTypeDefinitionNode instance extracted from
    the parsing of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: an InterfaceTypeDefinitionNode instance extracted from the parsing
    of the tree
    :rtype: InterfaceTypeDefinitionNode
    """
    node_info = _extract_node_info(
        tree.children,
        types_to_value=[
            "description",
            "name",
            "directives",
            "fields_definition",
        ],
        types_to_ignore=["INTERFACE"],
    )

    return InterfaceTypeDefinitionNode(
        description=node_info.get("description"),
        name=node_info["name"],
        directives=node_info.get("directives") or [],
        fields=node_info.get("fields_definition") or [],
        location=lark_to_location_node(tree.meta),
    )


def lark_to_union_type_definition_node(
    tree: "Tree"
) -> "UnionTypeDefinitionNode":
    """
    Creates and returns an UnionTypeDefinitionNode instance extracted from the
    parsing of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: an UnionTypeDefinitionNode instance extracted from the parsing of
    the tree
    :rtype: UnionTypeDefinitionNode
    """
    node_info = _extract_node_info(
        tree.children,
        types_to_value=[
            "description",
            "name",
            "directives",
            "union_member_types",
        ],
        types_to_ignore=["UNION"],
    )

    return UnionTypeDefinitionNode(
        description=node_info.get("description"),
        name=node_info["name"],
        directives=node_info.get("directives") or [],
        types=node_info.get("union_member_types") or [],
        location=lark_to_location_node(tree.meta),
    )


def lark_to_enum_value_definition_node(
    tree: "Tree"
) -> "EnumValueDefinitionNode":
    """
    Creates and returns an EnumValueDefinitionNode instance extracted from the
    parsing of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: an EnumValueDefinitionNode instance extracted from the parsing of
    the tree
    :rtype: EnumValueDefinitionNode
    """
    node_info = _extract_node_info(
        tree.children,
        types_to_value=["description", "enum_value", "directives"],
    )

    return EnumValueDefinitionNode(
        description=node_info.get("description"),
        name=node_info["enum_value"],
        directives=node_info.get("directives") or [],
        location=lark_to_location_node(tree.meta),
    )


def lark_to_enum_type_definition_node(
    tree: "Tree"
) -> "EnumTypeDefinitionNode":
    """
    Creates and returns an EnumTypeDefinitionNode instance extracted from the
    parsing of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: an EnumTypeDefinitionNode instance extracted from the parsing of
    the tree
    :rtype: EnumTypeDefinitionNode
    """
    node_info = _extract_node_info(
        tree.children,
        types_to_value=[
            "description",
            "name",
            "directives",
            "enum_values_definition",
        ],
        types_to_ignore=["ENUM"],
    )

    return EnumTypeDefinitionNode(
        description=node_info.get("description"),
        name=node_info["name"],
        directives=node_info.get("directives") or [],
        values=node_info.get("enum_values_definition") or [],
        location=lark_to_location_node(tree.meta),
    )


def lark_to_input_object_type_definition_node(
    tree: "Tree"
) -> "InputObjectTypeDefinitionNode":
    """
    Creates and returns an InputObjectTypeDefinitionNode instance extracted
    from the parsing of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: an InputObjectTypeDefinitionNode instance extracted from the
    parsing of the tree
    :rtype: InputObjectTypeDefinitionNode
    """
    node_info = _extract_node_info(
        tree.children,
        types_to_value=[
            "description",
            "name",
            "directives",
            "input_fields_definition",
        ],
        types_to_ignore=["INPUT"],
    )

    return InputObjectTypeDefinitionNode(
        description=node_info.get("description"),
        name=node_info["name"],
        directives=node_info.get("directives") or [],
        fields=node_info.get("input_fields_definition") or [],
        location=lark_to_location_node(tree.meta),
    )


def lark_to_schema_extension_node(tree: "Tree") -> "SchemaExtensionNode":
    """
    Creates and returns a SchemaExtensionNode instance extracted from the
    parsing of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: a SchemaExtensionNode instance extracted from the parsing of the
    tree
    :rtype: SchemaExtensionNode
    """
    node_info = _extract_node_info(
        tree.children,
        types_to_value=["directives"],
        types_to_list={
            "operation_type_definition": "operation_type_definitions"
        },
        types_to_ignore=["EXTEND", "SCHEMA"],
    )

    return SchemaExtensionNode(
        directives=node_info.get("directives") or [],
        operation_type_definitions=[
            operation_type_definition.value
            for operation_type_definition in node_info.get(
                "operation_type_definitions"
            )
            or []
        ],
        location=lark_to_location_node(tree.meta),
    )


def lark_to_scalar_type_extension_node(
    tree: "Tree"
) -> "ScalarTypeExtensionNode":
    """
    Creates and returns a ScalarTypeExtensionNode instance extracted from the
    parsing of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: a ScalarTypeExtensionNode instance extracted from the parsing of
    the tree
    :rtype: ScalarTypeExtensionNode
    """
    node_info = _extract_node_info(
        tree.children,
        types_to_value=["name", "directives"],
        types_to_ignore=["EXTEND", "SCALAR"],
    )

    return ScalarTypeExtensionNode(
        name=node_info["name"],
        directives=node_info.get("directives") or [],
        location=lark_to_location_node(tree.meta),
    )


def lark_to_object_type_extension_node(
    tree: "Tree"
) -> "ObjectTypeExtensionNode":
    """
    Creates and returns an ObjectTypeExtensionNode instance extracted from the
    parsing of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: an ObjectTypeExtensionNode instance extracted from the parsing of
    the tree
    :rtype: ObjectTypeExtensionNode
    """
    node_info = _extract_node_info(
        tree.children,
        types_to_value=[
            "name",
            "implements_interfaces",
            "directives",
            "fields_definition",
        ],
        types_to_ignore=["EXTEND", "TYPE"],
    )

    return ObjectTypeExtensionNode(
        name=node_info["name"],
        interfaces=node_info.get("implements_interfaces") or [],
        directives=node_info.get("directives") or [],
        fields=node_info.get("fields_definition") or [],
        location=lark_to_location_node(tree.meta),
    )


def lark_to_interface_type_extension_node(
    tree: "Tree"
) -> "InterfaceTypeExtensionNode":
    """
    Creates and returns an InterfaceTypeExtensionNode instance extracted from
    the parsing of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: an InterfaceTypeExtensionNode instance extracted from the parsing
    of the tree
    :rtype: InterfaceTypeExtensionNode
    """
    node_info = _extract_node_info(
        tree.children,
        types_to_value=["name", "directives", "fields_definition"],
        types_to_ignore=["EXTEND", "INTERFACE"],
    )

    return InterfaceTypeExtensionNode(
        name=node_info["name"],
        directives=node_info.get("directives") or [],
        fields=node_info.get("fields_definition") or [],
        location=lark_to_location_node(tree.meta),
    )


def lark_to_union_type_extension_node(
    tree: "Tree"
) -> "UnionTypeExtensionNode":
    """
    Creates and returns an UnionTypeExtensionNode instance extracted from the
    parsing of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: an UnionTypeExtensionNode instance extracted from the parsing of
    the tree
    :rtype: UnionTypeExtensionNode
    """
    node_info = _extract_node_info(
        tree.children,
        types_to_value=["name", "directives", "union_member_types"],
        types_to_ignore=["EXTEND", "UNION"],
    )

    return UnionTypeExtensionNode(
        name=node_info["name"],
        directives=node_info.get("directives") or [],
        types=node_info.get("union_member_types") or [],
        location=lark_to_location_node(tree.meta),
    )


def lark_to_enum_type_extension_node(tree: "Tree") -> "EnumTypeExtensionNode":
    """
    Creates and returns an EnumTypeExtensionNode instance extracted from the
    parsing of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: an EnumTypeExtensionNode instance extracted from the parsing of
    the tree
    :rtype: EnumTypeExtensionNode
    """
    node_info = _extract_node_info(
        tree.children,
        types_to_value=["name", "directives", "enum_values_definition"],
        types_to_ignore=["EXTEND", "ENUM"],
    )

    return EnumTypeExtensionNode(
        name=node_info["name"],
        directives=node_info.get("directives") or [],
        values=node_info.get("enum_values_definition") or [],
        location=lark_to_location_node(tree.meta),
    )


def lark_to_input_object_type_extension_node(
    tree: "Tree"
) -> "InputObjectTypeExtension":
    """
    Creates and returns an InputObjectTypeExtension instance extracted from the
    parsing of the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: an InputObjectTypeExtension instance extracted from the parsing of
    the tree
    :rtype: InputObjectTypeExtension
    """
    node_info = _extract_node_info(
        tree.children,
        types_to_value=["name", "directives", "input_fields_definition"],
        types_to_ignore=["EXTEND", "INPUT"],
    )

    return InputObjectTypeExtension(
        name=node_info["name"],
        directives=node_info.get("directives") or [],
        fields=node_info.get("input_fields_definition") or [],
        location=lark_to_location_node(tree.meta),
    )


def lark_to_document_node(tree: "Tree") -> "DocumentNode":
    """
    Creates and returns a DocumentNode instance extracted from the parsing of
    the tree instance.
    :param tree: the Tree to parse in order to extract the proper node
    :type tree: Tree
    :return: a DocumentNode instance extracted from the parsing of the tree
    :rtype: DocumentNode
    """
    return DocumentNode(
        definitions=[child.value for child in tree.children],
        location=lark_to_location_node(tree.meta),
    )
