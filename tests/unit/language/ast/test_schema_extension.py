import pytest

from tartiflette.language.ast import SchemaExtensionNode


def test_schemaextensionnode__init__():
    schema_extension_node = SchemaExtensionNode(
        directives="schemaExtensionDirectives",
        operation_type_definitions="schemaExtensionOperationTypeDefinitions",
        location="schemaExtensionLocation",
    )
    assert schema_extension_node.directives == "schemaExtensionDirectives"
    assert (
        schema_extension_node.operation_type_definitions
        == "schemaExtensionOperationTypeDefinitions"
    )
    assert schema_extension_node.location == "schemaExtensionLocation"


@pytest.mark.parametrize(
    "schema_extension_node,other,expected",
    [
        (
            SchemaExtensionNode(
                directives="schemaExtensionDirectives",
                operation_type_definitions="schemaExtensionOperationTypeDefinitions",
                location="schemaExtensionLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            SchemaExtensionNode(
                directives="schemaExtensionDirectives",
                operation_type_definitions="schemaExtensionOperationTypeDefinitions",
                location="schemaExtensionLocation",
            ),
            SchemaExtensionNode(
                directives="schemaExtensionDirectivesBis",
                operation_type_definitions="schemaExtensionOperationTypeDefinitions",
                location="schemaExtensionLocation",
            ),
            False,
        ),
        (
            SchemaExtensionNode(
                directives="schemaExtensionDirectives",
                operation_type_definitions="schemaExtensionOperationTypeDefinitions",
                location="schemaExtensionLocation",
            ),
            SchemaExtensionNode(
                directives="schemaExtensionDirectives",
                operation_type_definitions="schemaExtensionOperationTypeDefinitionsBis",
                location="schemaExtensionLocation",
            ),
            False,
        ),
        (
            SchemaExtensionNode(
                directives="schemaExtensionDirectives",
                operation_type_definitions="schemaExtensionOperationTypeDefinitions",
                location="schemaExtensionLocation",
            ),
            SchemaExtensionNode(
                directives="schemaExtensionDirectives",
                operation_type_definitions="schemaExtensionOperationTypeDefinitions",
                location="schemaExtensionLocationBis",
            ),
            False,
        ),
        (
            SchemaExtensionNode(
                directives="schemaExtensionDirectives",
                operation_type_definitions="schemaExtensionOperationTypeDefinitions",
                location="schemaExtensionLocation",
            ),
            SchemaExtensionNode(
                directives="schemaExtensionDirectives",
                operation_type_definitions="schemaExtensionOperationTypeDefinitions",
                location="schemaExtensionLocation",
            ),
            True,
        ),
    ],
)
def test_schemaextensionnode__eq__(schema_extension_node, other, expected):
    assert (schema_extension_node == other) is expected


@pytest.mark.parametrize(
    "schema_extension_node,expected",
    [
        (
            SchemaExtensionNode(
                directives="schemaExtensionDirectives",
                operation_type_definitions="schemaExtensionOperationTypeDefinitions",
                location="schemaExtensionLocation",
            ),
            "SchemaExtensionNode("
            "directives='schemaExtensionDirectives', "
            "operation_type_definitions='schemaExtensionOperationTypeDefinitions', "
            "location='schemaExtensionLocation')",
        )
    ],
)
def test_schemaextensionnode__repr__(schema_extension_node, expected):
    assert schema_extension_node.__repr__() == expected
