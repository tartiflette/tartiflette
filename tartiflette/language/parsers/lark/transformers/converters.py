from typing import List, Union

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
    Location,
    NamedTypeNode,
    NameNode,
    NonNullTypeNode,
    NullValueNode,
    ObjectTypeDefinitionNode,
    ObjectTypeExtensionNode,
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
    TODO:
    """


def _extract_node_info(
    children, types_to_value=None, types_to_list=None, types_to_ignore=None
):
    """
    TODO:
    :param children: TODO:
    :param types_to_value: TODO:
    :param types_to_list: TODO:
    :param types_to_ignore: TODO:
    :type children: TODO:
    :type types_to_value: TODO:
    :type types_to_list: TODO:
    :type types_to_ignore: TODO:
    :return: TODO:
    :rtype: TODO:
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


def lark_to_location_node(
    token_or_tree_meta: Union["Tree", "Token"]
) -> "Location":
    """
    TODO:
    :param token_or_tree_meta: TODO:
    :type token_or_tree_meta: Union[Tree, Token]
    :return: TODO:
    :rtype: Location
    """
    return Location(
        line=token_or_tree_meta.line,
        column=token_or_tree_meta.column,
        line_end=token_or_tree_meta.end_line,
        column_end=token_or_tree_meta.end_column,
    )


def lark_to_int_value_node(tree: "Tree") -> "IntValueNode":
    """
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
    :rtype: IntValueNode
    """
    token = tree.children[0]
    return IntValueNode(
        value=token.value, location=lark_to_location_node(token)
    )


def lark_to_float_value_node(tree: "Tree") -> "FloatValueNode":
    """
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
    :rtype: FloatValueNode
    """
    token = tree.children[0]
    return FloatValueNode(
        value=token.value, location=lark_to_location_node(token)
    )


def lark_to_string_value_node(tree: "Tree") -> "StringValueNode":
    """
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
    :rtype: StringValueNode
    """
    token = tree.children[0]
    return StringValueNode(
        value=token.value, location=lark_to_location_node(token)
    )


def lark_to_boolean_value_node(tree: "Tree") -> "BooleanValueNode":
    """
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
    :rtype: BooleanValueNode
    """
    token = tree.children[0]
    return BooleanValueNode(
        value=token.value, location=lark_to_location_node(token)
    )


def lark_to_null_value_node(tree: "Tree") -> "NullValueNode":
    """
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
    :rtype: NullValueNode
    """
    return NullValueNode(location=lark_to_location_node(tree.children[0]))


def lark_to_enum_value_node(tree: "Tree") -> "EnumValueNode":
    """
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
    :rtype: EnumValueNode
    """
    token = tree.children[0]
    return EnumValueNode(
        value=token.value, location=lark_to_location_node(token)
    )


def lark_to_description_node(tree: "Tree") -> "DescriptionNode":
    """
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
    :rtype: DescriptionNode
    """
    token = tree.children[0]
    return DescriptionNode(
        value=token.value, location=lark_to_location_node(token)
    )


def lark_to_name_node(tree: "Tree") -> "NameNode":
    """
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
    :rtype: NameNode
    """
    token = tree.children[0]
    return NameNode(value=token.value, location=lark_to_location_node(token))


def lark_to_named_type_node(tree: "Tree") -> "NamedTypeNode":
    """
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
    :rtype: NamedTypeNode
    """
    token = tree.children[0].value
    return NamedTypeNode(
        name=token.value, location=lark_to_location_node(tree.meta)
    )


def lark_to_argument_node(tree: "Tree") -> "ArgumentNode":
    """
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
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
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
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


# def lark_to_operation_type_node(tree: "Tree") -> "OperationTypeNode":
#     """
#     TODO:
#     :param tree: TODO:
#     :type tree: Tree
#     :return: TODO:
#     :rtype: OperationTypeNode
#     """
#     token = tree.children[0]
#     return OperationTypeNode(
#         value=token.value, location=lark_to_location_node(token)
#     )


def lark_to_operation_type_definition_node(
    tree: "Tree"
) -> "OperationTypeDefinitionNode":
    """
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
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
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
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
        directives=node_info.get("directives"),
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
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
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
        directives=node_info.get("directives"),
        location=lark_to_location_node(tree.meta),
    )


def lark_to_list_type_node(tree: "Tree") -> "ListTypeNode":
    """
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
    :rtype: ListTypeNode
    """
    token = tree.children[0]
    return ListTypeNode(
        type=token.value, location=lark_to_location_node(tree.meta)
    )


def lark_to_non_null_type_node(tree: "Tree") -> "NonNullTypeNode":
    """
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
    :rtype: NonNullTypeNode
    """
    token = tree.children[0]
    return NonNullTypeNode(
        type=token.value, location=lark_to_location_node(tree.meta)
    )


# def lark_to_default_value_node(tree: "Tree") -> "DefaultValueNode":
#     """
#     TODO:
#     :param tree: TODO:
#     :type tree: Tree
#     :return: TODO:
#     :rtype: DefaultValueNode
#     """
#     value_node = tree.children[0].value
#     return DefaultValueNode(
#         value=value_node.value, location=value_node.location
#     )


def lark_to_input_value_definition_node(
    tree: "Tree"
) -> "InputValueDefinitionNode":
    """
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
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


# def lark_to_directive_location_node(tree: "Tree") -> "DirectiveLocationNode":
#     """
#     TODO:
#     :param tree: TODO:
#     :type tree: Tree
#     :return: TODO:
#     :rtype: DirectiveLocationNode
#     """
#     token = tree.children[0]
#     return DirectiveLocationNode(
#         value=token.value, location=lark_to_location_node(token)
#     )


def lark_to_directive_definition_node(
    tree: "Tree"
) -> "DirectiveDefinitionNode":
    """
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
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
        arguments=node_info.get("arguments_definition") or None,
        locations=node_info.get("directive_locations") or None,
        location=lark_to_location_node(tree.meta),
    )


def lark_to_implements_interfaces_node(tree: "Tree") -> List["NamedTypeNode"]:
    """
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
    :rtype: List[NamedTypeNode]
    """
    node_info = _extract_node_info(
        tree.children,
        types_to_list={"named_type": "named_types"},
        types_to_ignore=["IMPLEMENTS"],
    )

    return [
        NamedTypeNode(
            name=named_type.value, location=named_type.value.location
        )
        for named_type in node_info.get("named_types") or []
    ]


def lark_to_field_definition_node(tree: "Tree") -> "FieldDefinitionNode":
    """
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
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
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
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
        interfaces=node_info.get("implements_interfaces"),
        directives=node_info.get("directives") or [],
        fields=node_info.get("fields_definition") or [],
        location=lark_to_location_node(tree.meta),
    )


def lark_to_interface_type_definition_node(
    tree: "Tree"
) -> "InterfaceTypeDefinitionNode":
    """
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
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
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
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
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
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
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
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
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
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
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
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
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
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
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
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
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
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
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
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
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
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
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
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
    TODO:
    :param tree: TODO:
    :type tree: Tree
    :return: TODO:
    :rtype: DocumentNode
    """
    return DocumentNode(
        definitions=[child.value for child in tree.children],
        location=lark_to_location_node(tree.meta),
    )
