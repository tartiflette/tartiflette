import pytest

from tartiflette.language.ast import SchemaDefinitionNode


def test_schemadefinitionnode__init__():
    schema_definition_node = SchemaDefinitionNode(
        operation_type_definitions="schemaDefinitionOperationTypeDefinitions",
        directives="schemaDefinitionDirectives",
        location="schemaDefinitionLocation",
    )
    assert (
        schema_definition_node.operation_type_definitions
        == "schemaDefinitionOperationTypeDefinitions"
    )
    assert schema_definition_node.directives == "schemaDefinitionDirectives"
    assert schema_definition_node.location == "schemaDefinitionLocation"


@pytest.mark.parametrize(
    "schema_definition_node,other,expected",
    [
        (
            SchemaDefinitionNode(
                operation_type_definitions="schemaDefinitionOperationTypeDefinitions",
                directives="schemaDefinitionDirectives",
                location="schemaDefinitionLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            SchemaDefinitionNode(
                operation_type_definitions="schemaDefinitionOperationTypeDefinitions",
                directives="schemaDefinitionDirectives",
                location="schemaDefinitionLocation",
            ),
            SchemaDefinitionNode(
                operation_type_definitions="schemaDefinitionOperationTypeDefinitionsBis",
                directives="schemaDefinitionDirectives",
                location="schemaDefinitionLocation",
            ),
            False,
        ),
        (
            SchemaDefinitionNode(
                operation_type_definitions="schemaDefinitionOperationTypeDefinitions",
                directives="schemaDefinitionDirectives",
                location="schemaDefinitionLocation",
            ),
            SchemaDefinitionNode(
                operation_type_definitions="schemaDefinitionOperationTypeDefinitions",
                directives="schemaDefinitionDirectivesBis",
                location="schemaDefinitionLocation",
            ),
            False,
        ),
        (
            SchemaDefinitionNode(
                operation_type_definitions="schemaDefinitionOperationTypeDefinitions",
                directives="schemaDefinitionDirectives",
                location="schemaDefinitionLocation",
            ),
            SchemaDefinitionNode(
                operation_type_definitions="schemaDefinitionOperationTypeDefinitions",
                directives="schemaDefinitionDirectives",
                location="schemaDefinitionLocationBis",
            ),
            False,
        ),
        (
            SchemaDefinitionNode(
                operation_type_definitions="schemaDefinitionOperationTypeDefinitions",
                directives="schemaDefinitionDirectives",
                location="schemaDefinitionLocation",
            ),
            SchemaDefinitionNode(
                operation_type_definitions="schemaDefinitionOperationTypeDefinitions",
                directives="schemaDefinitionDirectives",
                location="schemaDefinitionLocation",
            ),
            True,
        ),
    ],
)
def test_schemadefinitionnode__eq__(schema_definition_node, other, expected):
    assert (schema_definition_node == other) is expected


@pytest.mark.parametrize(
    "schema_definition_node,expected",
    [
        (
            SchemaDefinitionNode(
                operation_type_definitions="schemaDefinitionOperationTypeDefinitions",
                directives="schemaDefinitionDirectives",
                location="schemaDefinitionLocation",
            ),
            "SchemaDefinitionNode("
            "directives='schemaDefinitionDirectives', "
            "operation_type_definitions='schemaDefinitionOperationTypeDefinitions', "
            "location='schemaDefinitionLocation')",
        )
    ],
)
def test_schemadefinitionnode__repr__(schema_definition_node, expected):
    assert schema_definition_node.__repr__() == expected
