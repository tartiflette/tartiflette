from unittest.mock import Mock

import pytest

from lark import Tree
from lark.lexer import Token

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
from tartiflette.language.parsers.lark.transformers.converters import (
    UnexpectedASTNode,
    _extract_node_info,
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
    lark_to_location_node,
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
from tartiflette.language.parsers.lark.transformers.node_transformer import (
    SchemaNode,
)

_DEFAULT_TREE_META_MOCK = Mock(line=1, column=2, end_line=3, end_column=4)
_EXPECTED_TREE_LOCATION = Location(line=1, column=2, line_end=3, column_end=4)


@pytest.mark.parametrize(
    "children,options,expected",
    [
        (
            [SchemaNode(type="name", value="aName"), Token("value", "aValue")],
            {"types_to_value": ["name", "value"]},
            {"name": "aName", "value": "aValue"},
        ),
        (
            [
                SchemaNode(type="definition", value="firstDefinition"),
                Token("definition", "secondDefinition"),
            ],
            {"types_to_list": {"definition": "definitions"}},
            {
                "definitions": [
                    SchemaNode(type="definition", value="firstDefinition"),
                    Token("definition", "secondDefinition"),
                ]
            },
        ),
        (
            [SchemaNode(type="to_ignore", value=None)],
            {"types_to_ignore": "to_ignore"},
            {},
        ),
        (
            [
                SchemaNode(type="definition", value="firstDefinition"),
                Token("value", "aValue"),
                SchemaNode(type="to_ignore", value=None),
                Token("definition", "secondDefinition"),
                SchemaNode(type="name", value="aName"),
            ],
            {
                "types_to_value": ["name", "value"],
                "types_to_list": {"definition": "definitions"},
                "types_to_ignore": "to_ignore",
            },
            {
                "name": "aName",
                "value": "aValue",
                "definitions": [
                    SchemaNode(type="definition", value="firstDefinition"),
                    Token("definition", "secondDefinition"),
                ],
            },
        ),
    ],
)
def test_extract_node_info(children, options, expected):
    assert _extract_node_info(children, **options) == expected


def test_extract_node_info_unexpected_ast_node():
    with pytest.raises(UnexpectedASTNode):
        _extract_node_info([SchemaNode(type="unexpected", value=None)])


@pytest.mark.parametrize(
    "line,column,end_line,end_column,expected",
    [
        (1, 2, 2, 1, Location(line=1, column=2, line_end=2, column_end=1)),
        (1, 2, 3, 4, Location(line=1, column=2, line_end=3, column_end=4)),
    ],
)
def test_lark_to_location_node(line, column, end_line, end_column, expected):
    node = Mock(
        line=line, column=column, end_line=end_line, end_column=end_column
    )
    assert lark_to_location_node(node) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="int_value",
                children=[Token("INT_VALUE", 10)],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            IntValueNode(value="10", location=_EXPECTED_TREE_LOCATION),
        )
    ],
)
def test_lark_to_int_value_node(tree, expected):
    assert lark_to_int_value_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="float_value",
                children=[Token("FLOAT_VALUE", 10.2)],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            FloatValueNode(value="10.2", location=_EXPECTED_TREE_LOCATION),
        )
    ],
)
def test_lark_to_float_value_node(tree, expected):
    assert lark_to_float_value_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="string_value",
                children=[Token("STRING_VALUE", "aValue")],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            StringValueNode(value="aValue", location=_EXPECTED_TREE_LOCATION),
        )
    ],
)
def test_lark_to_string_value_node(tree, expected):
    assert lark_to_string_value_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="boolean_value",
                children=[Token("BOOLEAN_VALUE", True)],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            BooleanValueNode(value="True", location=_EXPECTED_TREE_LOCATION),
        )
    ],
)
def test_lark_to_boolean_value_node(tree, expected):
    assert lark_to_boolean_value_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="null_value",
                children=[Token("NULL_VALUE", None)],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            NullValueNode(location=_EXPECTED_TREE_LOCATION),
        )
    ],
)
def test_lark_to_null_value_node(tree, expected):
    assert lark_to_null_value_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="enum_value",
                children=[Token("ENUM", "ENUM_VALUE")],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            EnumValueNode(
                value="ENUM_VALUE", location=_EXPECTED_TREE_LOCATION
            ),
        )
    ],
)
def test_lark_to_enum_value_node(tree, expected):
    assert lark_to_enum_value_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="list_value",
                children=[
                    SchemaNode(
                        type="value",
                        value=BooleanValueNode(
                            value=True, location=_EXPECTED_TREE_LOCATION
                        ),
                    )
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            ListValueNode(
                values=[
                    BooleanValueNode(
                        value=True, location=_EXPECTED_TREE_LOCATION
                    )
                ],
                location=_EXPECTED_TREE_LOCATION,
            ),
        )
    ],
)
def test_lark_to_list_value_node(tree, expected):
    assert lark_to_list_value_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="object_field",
                children=[
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="fieldName", location=_EXPECTED_TREE_LOCATION
                        ),
                    ),
                    SchemaNode(
                        type="value",
                        value=BooleanValueNode(
                            value=True, location=_EXPECTED_TREE_LOCATION
                        ),
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            ObjectFieldNode(
                name=NameNode(
                    value="fieldName", location=_EXPECTED_TREE_LOCATION
                ),
                value=BooleanValueNode(
                    value=True, location=_EXPECTED_TREE_LOCATION
                ),
                location=_EXPECTED_TREE_LOCATION,
            ),
        )
    ],
)
def test_lark_to_object_field_node(tree, expected):
    assert lark_to_object_field_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="object_value",
                children=[
                    SchemaNode(
                        type="object_field",
                        value=ObjectFieldNode(
                            name=NameNode(
                                value="fieldName",
                                location=_EXPECTED_TREE_LOCATION,
                            ),
                            value=BooleanValueNode(
                                value=True, location=_EXPECTED_TREE_LOCATION
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    )
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            ObjectValueNode(
                fields=[
                    ObjectFieldNode(
                        name=NameNode(
                            value="fieldName", location=_EXPECTED_TREE_LOCATION
                        ),
                        value=BooleanValueNode(
                            value=True, location=_EXPECTED_TREE_LOCATION
                        ),
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                location=_EXPECTED_TREE_LOCATION,
            ),
        )
    ],
)
def test_lark_to_object_value_node(tree, expected):
    assert lark_to_object_value_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="name",
                children=[Token("NAME", "aName")],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            NameNode(value="aName", location=_EXPECTED_TREE_LOCATION),
        )
    ],
)
def test_lark_to_name_node(tree, expected):
    assert lark_to_name_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="description",
                children=[Token("DESCRIPTION", "aDescription")],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            DescriptionNode(
                value="aDescription", location=_EXPECTED_TREE_LOCATION
            ),
        )
    ],
)
def test_lark_to_description_node(tree, expected):
    assert lark_to_description_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="named_type",
                children=[
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="aName", location=_EXPECTED_TREE_LOCATION
                        ),
                    )
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            NamedTypeNode(
                name=NameNode(value="aName", location=_EXPECTED_TREE_LOCATION),
                location=_EXPECTED_TREE_LOCATION,
            ),
        )
    ],
)
def test_lark_to_named_type_node(tree, expected):
    assert lark_to_named_type_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="argument",
                children=[
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="argumentName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="value",
                        value=BooleanValueNode(
                            value=True, location=_EXPECTED_TREE_LOCATION
                        ),
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            ArgumentNode(
                name=NameNode(
                    value="argumentName", location=_EXPECTED_TREE_LOCATION
                ),
                value=BooleanValueNode(
                    value=True, location=_EXPECTED_TREE_LOCATION
                ),
                location=_EXPECTED_TREE_LOCATION,
            ),
        )
    ],
)
def test_lark_to_argument_node(tree, expected):
    assert lark_to_argument_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="directive",
                children=[
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="directiveName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="arguments",
                        value=[
                            ArgumentNode(
                                name=NameNode(
                                    value="argumentName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                value=BooleanValueNode(
                                    value=True,
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            DirectiveNode(
                name=NameNode(
                    value="directiveName", location=_EXPECTED_TREE_LOCATION
                ),
                arguments=[
                    ArgumentNode(
                        name=NameNode(
                            value="argumentName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        value=BooleanValueNode(
                            value=True, location=_EXPECTED_TREE_LOCATION
                        ),
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
        (
            Tree(
                data="directive",
                children=[
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="directiveName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    )
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            DirectiveNode(
                name=NameNode(
                    value="directiveName", location=_EXPECTED_TREE_LOCATION
                ),
                arguments=[],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
    ],
)
def test_lark_to_directive_node(tree, expected):
    assert lark_to_directive_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="operation_type_definition",
                children=[
                    SchemaNode(type="operation_type", value="query"),
                    SchemaNode(
                        type="named_type",
                        value=NamedTypeNode(
                            name=NameNode(
                                value="aName", location=_EXPECTED_TREE_LOCATION
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            OperationTypeDefinitionNode(
                operation_type="query",
                type=NamedTypeNode(
                    name=NameNode(
                        value="aName", location=_EXPECTED_TREE_LOCATION
                    ),
                    location=_EXPECTED_TREE_LOCATION,
                ),
                location=_EXPECTED_TREE_LOCATION,
            ),
        )
    ],
)
def test_lark_to_operation_type_definition_node(tree, expected):
    assert lark_to_operation_type_definition_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="schema_definition",
                children=[
                    SchemaNode(type="SCHEMA", value=None),
                    SchemaNode(
                        type="operation_type_definition",
                        value=OperationTypeDefinitionNode(
                            operation_type="query",
                            type=NamedTypeNode(
                                name=NameNode(
                                    value="firstOperation",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                location=_EXPECTED_TREE_LOCATION,
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="operation_type_definition",
                        value=OperationTypeDefinitionNode(
                            operation_type="mutation",
                            type=NamedTypeNode(
                                name=NameNode(
                                    value="secondOperation",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                location=_EXPECTED_TREE_LOCATION,
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="directives",
                        value=[
                            DirectiveNode(
                                name=NameNode(
                                    value="directiveName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                arguments=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            SchemaDefinitionNode(
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="directiveName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                operation_type_definitions=[
                    OperationTypeDefinitionNode(
                        operation_type="query",
                        type=NamedTypeNode(
                            name=NameNode(
                                value="firstOperation",
                                location=_EXPECTED_TREE_LOCATION,
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        location=_EXPECTED_TREE_LOCATION,
                    ),
                    OperationTypeDefinitionNode(
                        operation_type="mutation",
                        type=NamedTypeNode(
                            name=NameNode(
                                value="secondOperation",
                                location=_EXPECTED_TREE_LOCATION,
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        location=_EXPECTED_TREE_LOCATION,
                    ),
                ],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
        (
            Tree(
                data="schema_definition",
                children=[SchemaNode(type="SCHEMA", value=None)],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            SchemaDefinitionNode(
                directives=[],
                operation_type_definitions=[],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
    ],
)
def test_lark_to_schema_definition_node(tree, expected):
    assert lark_to_schema_definition_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="scalar_type_definition",
                children=[
                    SchemaNode(type="SCALAR", value=None),
                    SchemaNode(
                        type="description",
                        value=DescriptionNode(
                            value="aDescription",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="aScalarName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="directives",
                        value=[
                            DirectiveNode(
                                name=NameNode(
                                    value="directiveName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                arguments=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            ScalarTypeDefinitionNode(
                description=DescriptionNode(
                    value="aDescription", location=_EXPECTED_TREE_LOCATION
                ),
                name=NameNode(
                    value="aScalarName", location=_EXPECTED_TREE_LOCATION
                ),
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="directiveName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
        (
            Tree(
                data="scalar_type_definition",
                children=[
                    SchemaNode(type="SCALAR", value=None),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="aScalarName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            ScalarTypeDefinitionNode(
                description=None,
                name=NameNode(
                    value="aScalarName", location=_EXPECTED_TREE_LOCATION
                ),
                directives=[],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
    ],
)
def test_lark_to_scalar_type_definition_node(tree, expected):
    assert lark_to_scalar_type_definition_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="list_type",
                children=[
                    SchemaNode(
                        type="named_type",
                        value=NamedTypeNode(
                            name=NameNode(
                                value="aName", location=_EXPECTED_TREE_LOCATION
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    )
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            ListTypeNode(
                type=NamedTypeNode(
                    name=NameNode(
                        value="aName", location=_EXPECTED_TREE_LOCATION
                    ),
                    location=_EXPECTED_TREE_LOCATION,
                ),
                location=_EXPECTED_TREE_LOCATION,
            ),
        )
    ],
)
def test_lark_to_list_type_node(tree, expected):
    assert lark_to_list_type_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="non_null_type",
                children=[
                    SchemaNode(
                        type="named_type",
                        value=NamedTypeNode(
                            name=NameNode(
                                value="aName", location=_EXPECTED_TREE_LOCATION
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    )
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            NonNullTypeNode(
                type=NamedTypeNode(
                    name=NameNode(
                        value="aName", location=_EXPECTED_TREE_LOCATION
                    ),
                    location=_EXPECTED_TREE_LOCATION,
                ),
                location=_EXPECTED_TREE_LOCATION,
            ),
        )
    ],
)
def test_lark_to_non_null_type_node(tree, expected):
    assert lark_to_non_null_type_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="scalar_type_definition",
                children=[
                    SchemaNode(
                        type="description",
                        value=DescriptionNode(
                            value="aDescription",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="anInputValueDefinitionName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="type",
                        value=NamedTypeNode(
                            name=NameNode(
                                value="aName", location=_EXPECTED_TREE_LOCATION
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="default_value",
                        value=BooleanValueNode(
                            value=True, location=_EXPECTED_TREE_LOCATION
                        ),
                    ),
                    SchemaNode(
                        type="directives",
                        value=[
                            DirectiveNode(
                                name=NameNode(
                                    value="directiveName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                arguments=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            InputValueDefinitionNode(
                description=DescriptionNode(
                    value="aDescription", location=_EXPECTED_TREE_LOCATION
                ),
                name=NameNode(
                    value="anInputValueDefinitionName",
                    location=_EXPECTED_TREE_LOCATION,
                ),
                type=NamedTypeNode(
                    name=NameNode(
                        value="aName", location=_EXPECTED_TREE_LOCATION
                    ),
                    location=_EXPECTED_TREE_LOCATION,
                ),
                default_value=BooleanValueNode(
                    value=True, location=_EXPECTED_TREE_LOCATION
                ),
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="directiveName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
        (
            Tree(
                data="scalar_type_definition",
                children=[
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="anInputValueDefinitionName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="type",
                        value=NamedTypeNode(
                            name=NameNode(
                                value="aName", location=_EXPECTED_TREE_LOCATION
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            InputValueDefinitionNode(
                description=None,
                name=NameNode(
                    value="anInputValueDefinitionName",
                    location=_EXPECTED_TREE_LOCATION,
                ),
                type=NamedTypeNode(
                    name=NameNode(
                        value="aName", location=_EXPECTED_TREE_LOCATION
                    ),
                    location=_EXPECTED_TREE_LOCATION,
                ),
                default_value=None,
                directives=[],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
    ],
)
def test_lark_to_input_value_definition_node(tree, expected):
    assert lark_to_input_value_definition_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="directive_definition",
                children=[
                    SchemaNode(type="DIRECTIVE", value=None),
                    SchemaNode(type="ON", value=None),
                    SchemaNode(
                        type="description",
                        value=DescriptionNode(
                            value="aDescription",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="aDirectiveDefinitionName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="arguments_definition",
                        value=[
                            InputValueDefinitionNode(
                                description=None,
                                name=NameNode(
                                    value="anInputValueDefinitionName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                type=NamedTypeNode(
                                    name=NameNode(
                                        value="aName",
                                        location=_EXPECTED_TREE_LOCATION,
                                    ),
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                default_value=None,
                                directives=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                    SchemaNode(
                        type="directive_locations",
                        value=[
                            NameNode(
                                value="DIRECTIVE_LOCATION",
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            DirectiveDefinitionNode(
                description=DescriptionNode(
                    value="aDescription", location=_EXPECTED_TREE_LOCATION
                ),
                name=NameNode(
                    value="aDirectiveDefinitionName",
                    location=_EXPECTED_TREE_LOCATION,
                ),
                arguments=[
                    InputValueDefinitionNode(
                        description=None,
                        name=NameNode(
                            value="anInputValueDefinitionName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        type=NamedTypeNode(
                            name=NameNode(
                                value="aName", location=_EXPECTED_TREE_LOCATION
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        default_value=None,
                        directives=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                locations=[
                    NameNode(
                        value="DIRECTIVE_LOCATION",
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
        (
            Tree(
                data="directive_definition",
                children=[
                    SchemaNode(type="DIRECTIVE", value=None),
                    SchemaNode(type="ON", value=None),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="aDirectiveDefinitionName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            DirectiveDefinitionNode(
                description=None,
                name=NameNode(
                    value="aDirectiveDefinitionName",
                    location=_EXPECTED_TREE_LOCATION,
                ),
                arguments=[],
                locations=[],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
    ],
)
def test_lark_to_directive_definition_node(tree, expected):
    assert lark_to_directive_definition_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="implements_interfaces",
                children=[
                    SchemaNode(type="IMPLEMENTS", value=None),
                    SchemaNode(
                        type="named_type",
                        value=NamedTypeNode(
                            name=NameNode(
                                value="firstName",
                                location=_EXPECTED_TREE_LOCATION,
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="named_type",
                        value=NamedTypeNode(
                            name=NameNode(
                                value="secondName",
                                location=_EXPECTED_TREE_LOCATION,
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            [
                NamedTypeNode(
                    name=NameNode(
                        value="firstName", location=_EXPECTED_TREE_LOCATION
                    ),
                    location=_EXPECTED_TREE_LOCATION,
                ),
                NamedTypeNode(
                    name=NameNode(
                        value="secondName", location=_EXPECTED_TREE_LOCATION
                    ),
                    location=_EXPECTED_TREE_LOCATION,
                ),
            ],
        ),
        (
            Tree(
                data="implements_interfaces",
                children=[],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            [],
        ),
    ],
)
def test_lark_to_implements_interfaces_node(tree, expected):
    assert lark_to_implements_interfaces_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="field_definition",
                children=[
                    SchemaNode(
                        type="description",
                        value=DescriptionNode(
                            value="aDescription",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="aFieldDefinitionName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="arguments_definition",
                        value=[
                            InputValueDefinitionNode(
                                description=None,
                                name=NameNode(
                                    value="anInputValueDefinitionName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                type=NamedTypeNode(
                                    name=NameNode(
                                        value="aName",
                                        location=_EXPECTED_TREE_LOCATION,
                                    ),
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                default_value=None,
                                directives=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                    SchemaNode(
                        type="type",
                        value=NamedTypeNode(
                            name=NameNode(
                                value="aName", location=_EXPECTED_TREE_LOCATION
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="directives",
                        value=[
                            DirectiveNode(
                                name=NameNode(
                                    value="directiveName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                arguments=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            FieldDefinitionNode(
                description=DescriptionNode(
                    value="aDescription", location=_EXPECTED_TREE_LOCATION
                ),
                name=NameNode(
                    value="aFieldDefinitionName",
                    location=_EXPECTED_TREE_LOCATION,
                ),
                arguments=[
                    InputValueDefinitionNode(
                        description=None,
                        name=NameNode(
                            value="anInputValueDefinitionName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        type=NamedTypeNode(
                            name=NameNode(
                                value="aName", location=_EXPECTED_TREE_LOCATION
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        default_value=None,
                        directives=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                type=NamedTypeNode(
                    name=NameNode(
                        value="aName", location=_EXPECTED_TREE_LOCATION
                    ),
                    location=_EXPECTED_TREE_LOCATION,
                ),
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="directiveName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
        (
            Tree(
                data="field_definition",
                children=[
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="aFieldDefinitionName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="type",
                        value=NamedTypeNode(
                            name=NameNode(
                                value="aName", location=_EXPECTED_TREE_LOCATION
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            FieldDefinitionNode(
                description=None,
                name=NameNode(
                    value="aFieldDefinitionName",
                    location=_EXPECTED_TREE_LOCATION,
                ),
                arguments=[],
                type=NamedTypeNode(
                    name=NameNode(
                        value="aName", location=_EXPECTED_TREE_LOCATION
                    ),
                    location=_EXPECTED_TREE_LOCATION,
                ),
                directives=[],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
    ],
)
def test_lark_to_field_definition_node(tree, expected):
    assert lark_to_field_definition_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="object_type_definition",
                children=[
                    SchemaNode(type="TYPE", value=None),
                    SchemaNode(
                        type="description",
                        value=DescriptionNode(
                            value="aDescription",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="anObjectTypeDefinition",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="implements_interfaces",
                        value=[
                            NamedTypeNode(
                                name=NameNode(
                                    value="firstName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                    SchemaNode(
                        type="directives",
                        value=[
                            DirectiveNode(
                                name=NameNode(
                                    value="directiveName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                arguments=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                    SchemaNode(
                        type="fields_definition",
                        value=[
                            FieldDefinitionNode(
                                description=None,
                                name=NameNode(
                                    value="aFieldDefinitionName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                arguments=[],
                                type=NamedTypeNode(
                                    name=NameNode(
                                        value="aName",
                                        location=_EXPECTED_TREE_LOCATION,
                                    ),
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                directives=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            ObjectTypeDefinitionNode(
                description=DescriptionNode(
                    value="aDescription", location=_EXPECTED_TREE_LOCATION
                ),
                name=NameNode(
                    value="anObjectTypeDefinition",
                    location=_EXPECTED_TREE_LOCATION,
                ),
                interfaces=[
                    NamedTypeNode(
                        name=NameNode(
                            value="firstName", location=_EXPECTED_TREE_LOCATION
                        ),
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="directiveName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                fields=[
                    FieldDefinitionNode(
                        description=None,
                        name=NameNode(
                            value="aFieldDefinitionName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        arguments=[],
                        type=NamedTypeNode(
                            name=NameNode(
                                value="aName", location=_EXPECTED_TREE_LOCATION
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        directives=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
        (
            Tree(
                data="object_type_definition",
                children=[
                    SchemaNode(type="TYPE", value=None),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="anObjectTypeDefinition",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            ObjectTypeDefinitionNode(
                description=None,
                name=NameNode(
                    value="anObjectTypeDefinition",
                    location=_EXPECTED_TREE_LOCATION,
                ),
                interfaces=[],
                directives=[],
                fields=[],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
    ],
)
def test_lark_to_object_type_definition_node(tree, expected):
    assert lark_to_object_type_definition_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="interface_type_definition",
                children=[
                    SchemaNode(type="INTERFACE", value=None),
                    SchemaNode(
                        type="description",
                        value=DescriptionNode(
                            value="aDescription",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="anInterfaceTypeDefinition",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="directives",
                        value=[
                            DirectiveNode(
                                name=NameNode(
                                    value="directiveName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                arguments=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                    SchemaNode(
                        type="fields_definition",
                        value=[
                            FieldDefinitionNode(
                                description=None,
                                name=NameNode(
                                    value="aFieldDefinitionName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                arguments=[],
                                type=NamedTypeNode(
                                    name=NameNode(
                                        value="aName",
                                        location=_EXPECTED_TREE_LOCATION,
                                    ),
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                directives=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            InterfaceTypeDefinitionNode(
                description=DescriptionNode(
                    value="aDescription", location=_EXPECTED_TREE_LOCATION
                ),
                name=NameNode(
                    value="anInterfaceTypeDefinition",
                    location=_EXPECTED_TREE_LOCATION,
                ),
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="directiveName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                fields=[
                    FieldDefinitionNode(
                        description=None,
                        name=NameNode(
                            value="aFieldDefinitionName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        arguments=[],
                        type=NamedTypeNode(
                            name=NameNode(
                                value="aName", location=_EXPECTED_TREE_LOCATION
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        directives=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
        (
            Tree(
                data="interface_type_definition",
                children=[
                    SchemaNode(type="INTERFACE", value=None),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="anInterfaceTypeDefinition",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            InterfaceTypeDefinitionNode(
                description=None,
                name=NameNode(
                    value="anInterfaceTypeDefinition",
                    location=_EXPECTED_TREE_LOCATION,
                ),
                directives=[],
                fields=[],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
    ],
)
def test_lark_to_interface_type_definition_node(tree, expected):
    assert lark_to_interface_type_definition_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="union_type_definition",
                children=[
                    SchemaNode(type="UNION", value=None),
                    SchemaNode(
                        type="description",
                        value=DescriptionNode(
                            value="aDescription",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="anUnionTypeDefinition",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="directives",
                        value=[
                            DirectiveNode(
                                name=NameNode(
                                    value="directiveName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                arguments=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                    SchemaNode(
                        type="union_member_types",
                        value=[
                            NamedTypeNode(
                                name=NameNode(
                                    value="firstName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            UnionTypeDefinitionNode(
                description=DescriptionNode(
                    value="aDescription", location=_EXPECTED_TREE_LOCATION
                ),
                name=NameNode(
                    value="anUnionTypeDefinition",
                    location=_EXPECTED_TREE_LOCATION,
                ),
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="directiveName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                types=[
                    NamedTypeNode(
                        name=NameNode(
                            value="firstName", location=_EXPECTED_TREE_LOCATION
                        ),
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
        (
            Tree(
                data="union_type_definition",
                children=[
                    SchemaNode(type="UNION", value=None),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="anUnionTypeDefinition",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            UnionTypeDefinitionNode(
                description=None,
                name=NameNode(
                    value="anUnionTypeDefinition",
                    location=_EXPECTED_TREE_LOCATION,
                ),
                directives=[],
                types=[],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
    ],
)
def test_lark_to_union_type_definition_node(tree, expected):
    assert lark_to_union_type_definition_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="enum_value_definition",
                children=[
                    SchemaNode(
                        type="description",
                        value=DescriptionNode(
                            value="aDescription",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="enum_value",
                        value=NameNode(
                            value="anEnumValueName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="directives",
                        value=[
                            DirectiveNode(
                                name=NameNode(
                                    value="directiveName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                arguments=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            EnumValueDefinitionNode(
                description=DescriptionNode(
                    value="aDescription", location=_EXPECTED_TREE_LOCATION
                ),
                name=NameNode(
                    value="anEnumValueName", location=_EXPECTED_TREE_LOCATION
                ),
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="directiveName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
        (
            Tree(
                data="enum_value_definition",
                children=[
                    SchemaNode(
                        type="enum_value",
                        value=NameNode(
                            value="anEnumValueName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    )
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            EnumValueDefinitionNode(
                description=None,
                name=NameNode(
                    value="anEnumValueName", location=_EXPECTED_TREE_LOCATION
                ),
                directives=[],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
    ],
)
def test_lark_to_enum_value_definition_node(tree, expected):
    assert lark_to_enum_value_definition_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="enum_type_definition",
                children=[
                    SchemaNode(type="ENUM", value=None),
                    SchemaNode(
                        type="description",
                        value=DescriptionNode(
                            value="aDescription",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="anEnumTypeName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="directives",
                        value=[
                            DirectiveNode(
                                name=NameNode(
                                    value="directiveName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                arguments=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                    SchemaNode(
                        type="enum_values_definition",
                        value=[
                            EnumValueDefinitionNode(
                                description=None,
                                name=NameNode(
                                    value="anEnumValueName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                directives=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            EnumTypeDefinitionNode(
                description=DescriptionNode(
                    value="aDescription", location=_EXPECTED_TREE_LOCATION
                ),
                name=NameNode(
                    value="anEnumTypeName", location=_EXPECTED_TREE_LOCATION
                ),
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="directiveName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                values=[
                    EnumValueDefinitionNode(
                        description=None,
                        name=NameNode(
                            value="anEnumValueName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        directives=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
        (
            Tree(
                data="enum_type_definition",
                children=[
                    SchemaNode(type="ENUM", value=None),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="anEnumTypeName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            EnumTypeDefinitionNode(
                description=None,
                name=NameNode(
                    value="anEnumTypeName", location=_EXPECTED_TREE_LOCATION
                ),
                directives=[],
                values=[],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
    ],
)
def test_lark_to_enum_type_definition_node(tree, expected):
    assert lark_to_enum_type_definition_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="input_object_type_definition",
                children=[
                    SchemaNode(type="INPUT", value=None),
                    SchemaNode(
                        type="description",
                        value=DescriptionNode(
                            value="aDescription",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="anInputObjectTypeName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="directives",
                        value=[
                            DirectiveNode(
                                name=NameNode(
                                    value="directiveName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                arguments=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                    SchemaNode(
                        type="input_fields_definition",
                        value=[
                            InputValueDefinitionNode(
                                description=None,
                                name=NameNode(
                                    value="anInputValueDefinitionName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                type=NamedTypeNode(
                                    name=NameNode(
                                        value="aName",
                                        location=_EXPECTED_TREE_LOCATION,
                                    ),
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                default_value=None,
                                directives=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            InputObjectTypeDefinitionNode(
                description=DescriptionNode(
                    value="aDescription", location=_EXPECTED_TREE_LOCATION
                ),
                name=NameNode(
                    value="anInputObjectTypeName",
                    location=_EXPECTED_TREE_LOCATION,
                ),
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="directiveName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                fields=[
                    InputValueDefinitionNode(
                        description=None,
                        name=NameNode(
                            value="anInputValueDefinitionName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        type=NamedTypeNode(
                            name=NameNode(
                                value="aName", location=_EXPECTED_TREE_LOCATION
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        default_value=None,
                        directives=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
        (
            Tree(
                data="input_object_type_definition",
                children=[
                    SchemaNode(type="INPUT", value=None),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="anInputObjectTypeName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            InputObjectTypeDefinitionNode(
                description=None,
                name=NameNode(
                    value="anInputObjectTypeName",
                    location=_EXPECTED_TREE_LOCATION,
                ),
                directives=[],
                fields=[],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
    ],
)
def test_lark_to_input_object_type_definition_node(tree, expected):
    assert lark_to_input_object_type_definition_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="schema_extension",
                children=[
                    SchemaNode(type="EXTEND", value=None),
                    SchemaNode(type="SCHEMA", value=None),
                    SchemaNode(
                        type="operation_type_definition",
                        value=OperationTypeDefinitionNode(
                            operation_type="query",
                            type=NamedTypeNode(
                                name=NameNode(
                                    value="firstOperation",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                location=_EXPECTED_TREE_LOCATION,
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="operation_type_definition",
                        value=OperationTypeDefinitionNode(
                            operation_type="mutation",
                            type=NamedTypeNode(
                                name=NameNode(
                                    value="secondOperation",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                location=_EXPECTED_TREE_LOCATION,
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="directives",
                        value=[
                            DirectiveNode(
                                name=NameNode(
                                    value="directiveName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                arguments=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            SchemaExtensionNode(
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="directiveName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                operation_type_definitions=[
                    OperationTypeDefinitionNode(
                        operation_type="query",
                        type=NamedTypeNode(
                            name=NameNode(
                                value="firstOperation",
                                location=_EXPECTED_TREE_LOCATION,
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        location=_EXPECTED_TREE_LOCATION,
                    ),
                    OperationTypeDefinitionNode(
                        operation_type="mutation",
                        type=NamedTypeNode(
                            name=NameNode(
                                value="secondOperation",
                                location=_EXPECTED_TREE_LOCATION,
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        location=_EXPECTED_TREE_LOCATION,
                    ),
                ],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
        (
            Tree(
                data="schema_extension",
                children=[
                    SchemaNode(type="EXTEND", value=None),
                    SchemaNode(type="SCHEMA", value=None),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            SchemaExtensionNode(
                directives=[],
                operation_type_definitions=[],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
    ],
)
def test_lark_to_schema_extension_node(tree, expected):
    assert lark_to_schema_extension_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="scalar_type_extension",
                children=[
                    SchemaNode(type="EXTEND", value=None),
                    SchemaNode(type="SCALAR", value=None),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="aScalarName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="directives",
                        value=[
                            DirectiveNode(
                                name=NameNode(
                                    value="directiveName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                arguments=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            ScalarTypeExtensionNode(
                name=NameNode(
                    value="aScalarName", location=_EXPECTED_TREE_LOCATION
                ),
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="directiveName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
        (
            Tree(
                data="scalar_type_extension",
                children=[
                    SchemaNode(type="EXTEND", value=None),
                    SchemaNode(type="SCALAR", value=None),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="aScalarName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            ScalarTypeExtensionNode(
                name=NameNode(
                    value="aScalarName", location=_EXPECTED_TREE_LOCATION
                ),
                directives=[],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
    ],
)
def test_lark_to_scalar_type_extension_node(tree, expected):
    assert lark_to_scalar_type_extension_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="object_type_extension",
                children=[
                    SchemaNode(type="EXTEND", value=None),
                    SchemaNode(type="TYPE", value=None),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="anObjectTypeDefinition",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="implements_interfaces",
                        value=[
                            NamedTypeNode(
                                name=NameNode(
                                    value="firstName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                    SchemaNode(
                        type="directives",
                        value=[
                            DirectiveNode(
                                name=NameNode(
                                    value="directiveName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                arguments=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                    SchemaNode(
                        type="fields_definition",
                        value=[
                            FieldDefinitionNode(
                                description=None,
                                name=NameNode(
                                    value="aFieldDefinitionName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                arguments=[],
                                type=NamedTypeNode(
                                    name=NameNode(
                                        value="aName",
                                        location=_EXPECTED_TREE_LOCATION,
                                    ),
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                directives=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            ObjectTypeExtensionNode(
                name=NameNode(
                    value="anObjectTypeDefinition",
                    location=_EXPECTED_TREE_LOCATION,
                ),
                interfaces=[
                    NamedTypeNode(
                        name=NameNode(
                            value="firstName", location=_EXPECTED_TREE_LOCATION
                        ),
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="directiveName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                fields=[
                    FieldDefinitionNode(
                        description=None,
                        name=NameNode(
                            value="aFieldDefinitionName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        arguments=[],
                        type=NamedTypeNode(
                            name=NameNode(
                                value="aName", location=_EXPECTED_TREE_LOCATION
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        directives=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
        (
            Tree(
                data="object_type_extension",
                children=[
                    SchemaNode(type="EXTEND", value=None),
                    SchemaNode(type="TYPE", value=None),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="anObjectTypeDefinition",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            ObjectTypeExtensionNode(
                name=NameNode(
                    value="anObjectTypeDefinition",
                    location=_EXPECTED_TREE_LOCATION,
                ),
                interfaces=[],
                directives=[],
                fields=[],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
    ],
)
def test_lark_to_object_type_extension_node(tree, expected):
    assert lark_to_object_type_extension_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="interface_type_extension",
                children=[
                    SchemaNode(type="EXTEND", value=None),
                    SchemaNode(type="INTERFACE", value=None),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="anInterfaceTypeDefinition",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="directives",
                        value=[
                            DirectiveNode(
                                name=NameNode(
                                    value="directiveName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                arguments=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                    SchemaNode(
                        type="fields_definition",
                        value=[
                            FieldDefinitionNode(
                                description=None,
                                name=NameNode(
                                    value="aFieldDefinitionName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                arguments=[],
                                type=NamedTypeNode(
                                    name=NameNode(
                                        value="aName",
                                        location=_EXPECTED_TREE_LOCATION,
                                    ),
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                directives=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            InterfaceTypeExtensionNode(
                name=NameNode(
                    value="anInterfaceTypeDefinition",
                    location=_EXPECTED_TREE_LOCATION,
                ),
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="directiveName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                fields=[
                    FieldDefinitionNode(
                        description=None,
                        name=NameNode(
                            value="aFieldDefinitionName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        arguments=[],
                        type=NamedTypeNode(
                            name=NameNode(
                                value="aName", location=_EXPECTED_TREE_LOCATION
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        directives=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
        (
            Tree(
                data="interface_type_extension",
                children=[
                    SchemaNode(type="EXTEND", value=None),
                    SchemaNode(type="INTERFACE", value=None),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="anInterfaceTypeDefinition",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            InterfaceTypeExtensionNode(
                name=NameNode(
                    value="anInterfaceTypeDefinition",
                    location=_EXPECTED_TREE_LOCATION,
                ),
                directives=[],
                fields=[],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
    ],
)
def test_lark_to_interface_type_extension_node(tree, expected):
    assert lark_to_interface_type_extension_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="union_type_extension",
                children=[
                    SchemaNode(type="EXTEND", value=None),
                    SchemaNode(type="UNION", value=None),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="anUnionTypeDefinition",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="directives",
                        value=[
                            DirectiveNode(
                                name=NameNode(
                                    value="directiveName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                arguments=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                    SchemaNode(
                        type="union_member_types",
                        value=[
                            NamedTypeNode(
                                name=NameNode(
                                    value="firstName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            UnionTypeExtensionNode(
                name=NameNode(
                    value="anUnionTypeDefinition",
                    location=_EXPECTED_TREE_LOCATION,
                ),
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="directiveName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                types=[
                    NamedTypeNode(
                        name=NameNode(
                            value="firstName", location=_EXPECTED_TREE_LOCATION
                        ),
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
        (
            Tree(
                data="union_type_extension",
                children=[
                    SchemaNode(type="EXTEND", value=None),
                    SchemaNode(type="UNION", value=None),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="anUnionTypeDefinition",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            UnionTypeExtensionNode(
                name=NameNode(
                    value="anUnionTypeDefinition",
                    location=_EXPECTED_TREE_LOCATION,
                ),
                directives=[],
                types=[],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
    ],
)
def test_lark_to_union_type_extension_node(tree, expected):
    assert lark_to_union_type_extension_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="enum_type_extension",
                children=[
                    SchemaNode(type="EXTEND", value=None),
                    SchemaNode(type="ENUM", value=None),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="anEnumTypeName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="directives",
                        value=[
                            DirectiveNode(
                                name=NameNode(
                                    value="directiveName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                arguments=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                    SchemaNode(
                        type="enum_values_definition",
                        value=[
                            EnumValueDefinitionNode(
                                description=None,
                                name=NameNode(
                                    value="anEnumValueName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                directives=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            EnumTypeExtensionNode(
                name=NameNode(
                    value="anEnumTypeName", location=_EXPECTED_TREE_LOCATION
                ),
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="directiveName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                values=[
                    EnumValueDefinitionNode(
                        description=None,
                        name=NameNode(
                            value="anEnumValueName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        directives=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
        (
            Tree(
                data="enum_type_extension",
                children=[
                    SchemaNode(type="EXTEND", value=None),
                    SchemaNode(type="ENUM", value=None),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="anEnumTypeName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            EnumTypeExtensionNode(
                name=NameNode(
                    value="anEnumTypeName", location=_EXPECTED_TREE_LOCATION
                ),
                directives=[],
                values=[],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
    ],
)
def test_lark_to_enum_type_extension_node(tree, expected):
    assert lark_to_enum_type_extension_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="input_object_type_extension",
                children=[
                    SchemaNode(type="EXTEND", value=None),
                    SchemaNode(type="INPUT", value=None),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="anInputObjectTypeName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                    SchemaNode(
                        type="directives",
                        value=[
                            DirectiveNode(
                                name=NameNode(
                                    value="directiveName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                arguments=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                    SchemaNode(
                        type="input_fields_definition",
                        value=[
                            InputValueDefinitionNode(
                                description=None,
                                name=NameNode(
                                    value="anInputValueDefinitionName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                type=NamedTypeNode(
                                    name=NameNode(
                                        value="aName",
                                        location=_EXPECTED_TREE_LOCATION,
                                    ),
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                default_value=None,
                                directives=[],
                                location=_EXPECTED_TREE_LOCATION,
                            )
                        ],
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            InputObjectTypeExtension(
                name=NameNode(
                    value="anInputObjectTypeName",
                    location=_EXPECTED_TREE_LOCATION,
                ),
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="directiveName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                fields=[
                    InputValueDefinitionNode(
                        description=None,
                        name=NameNode(
                            value="anInputValueDefinitionName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        type=NamedTypeNode(
                            name=NameNode(
                                value="aName", location=_EXPECTED_TREE_LOCATION
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        default_value=None,
                        directives=[],
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
        (
            Tree(
                data="input_object_type_extension",
                children=[
                    SchemaNode(type="EXTEND", value=None),
                    SchemaNode(type="INPUT", value=None),
                    SchemaNode(
                        type="name",
                        value=NameNode(
                            value="anInputObjectTypeName",
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    ),
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            InputObjectTypeExtension(
                name=NameNode(
                    value="anInputObjectTypeName",
                    location=_EXPECTED_TREE_LOCATION,
                ),
                directives=[],
                fields=[],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
    ],
)
def test_lark_to_input_object_type_extension_node(tree, expected):
    assert lark_to_input_object_type_extension_node(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="document",
                children=[
                    SchemaNode(
                        type="operation_type_definition",
                        value=OperationTypeDefinitionNode(
                            operation_type="query",
                            type=NamedTypeNode(
                                name=NameNode(
                                    value="aName",
                                    location=_EXPECTED_TREE_LOCATION,
                                ),
                                location=_EXPECTED_TREE_LOCATION,
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                    )
                ],
                meta=_DEFAULT_TREE_META_MOCK,
            ),
            DocumentNode(
                definitions=[
                    OperationTypeDefinitionNode(
                        operation_type="query",
                        type=NamedTypeNode(
                            name=NameNode(
                                value="aName", location=_EXPECTED_TREE_LOCATION
                            ),
                            location=_EXPECTED_TREE_LOCATION,
                        ),
                        location=_EXPECTED_TREE_LOCATION,
                    )
                ],
                location=_EXPECTED_TREE_LOCATION,
            ),
        ),
        (
            Tree(data="document", children=[], meta=_DEFAULT_TREE_META_MOCK),
            DocumentNode(definitions=[], location=_EXPECTED_TREE_LOCATION),
        ),
    ],
)
def test_lark_to_document_node(tree, expected):
    assert lark_to_document_node(tree) == expected
