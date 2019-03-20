import pytest

from tartiflette.language.ast import OperationTypeDefinitionNode


def test_operationtypedefinitionnode__init__():
    operation_type_definition_node = OperationTypeDefinitionNode(
        operation_type="operationTypeDefinitionOperationType",
        type="operationTypeDefinitionType",
        location="operationTypeDefinitionLocation",
    )
    assert (
        operation_type_definition_node.operation_type
        == "operationTypeDefinitionOperationType"
    )
    assert operation_type_definition_node.type == "operationTypeDefinitionType"
    assert (
        operation_type_definition_node.location
        == "operationTypeDefinitionLocation"
    )


@pytest.mark.parametrize(
    "operation_type_definition_node,other,expected",
    [
        (
            OperationTypeDefinitionNode(
                operation_type="operationTypeDefinitionOperationType",
                type="operationTypeDefinitionType",
                location="operationTypeDefinitionLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            OperationTypeDefinitionNode(
                operation_type="operationTypeDefinitionOperationType",
                type="operationTypeDefinitionType",
                location="operationTypeDefinitionLocation",
            ),
            OperationTypeDefinitionNode(
                operation_type="operationTypeDefinitionOperationTypeBis",
                type="operationTypeDefinitionType",
                location="operationTypeDefinitionLocation",
            ),
            False,
        ),
        (
            OperationTypeDefinitionNode(
                operation_type="operationTypeDefinitionOperationType",
                type="operationTypeDefinitionType",
                location="operationTypeDefinitionLocation",
            ),
            OperationTypeDefinitionNode(
                operation_type="operationTypeDefinitionOperationType",
                type="operationTypeDefinitionTypeBis",
                location="operationTypeDefinitionLocation",
            ),
            False,
        ),
        (
            OperationTypeDefinitionNode(
                operation_type="operationTypeDefinitionOperationType",
                type="operationTypeDefinitionType",
                location="operationTypeDefinitionLocation",
            ),
            OperationTypeDefinitionNode(
                operation_type="operationTypeDefinitionOperationType",
                type="operationTypeDefinitionType",
                location="operationTypeDefinitionLocationBis",
            ),
            False,
        ),
        (
            OperationTypeDefinitionNode(
                operation_type="operationTypeDefinitionOperationType",
                type="operationTypeDefinitionType",
                location="operationTypeDefinitionLocation",
            ),
            OperationTypeDefinitionNode(
                operation_type="operationTypeDefinitionOperationType",
                type="operationTypeDefinitionType",
                location="operationTypeDefinitionLocation",
            ),
            True,
        ),
    ],
)
def test_operationtypedefinitionnode__eq__(
    operation_type_definition_node, other, expected
):
    assert (operation_type_definition_node == other) is expected


@pytest.mark.parametrize(
    "operation_type_definition_node,expected",
    [
        (
            OperationTypeDefinitionNode(
                operation_type="operationTypeDefinitionOperationType",
                type="operationTypeDefinitionType",
                location="operationTypeDefinitionLocation",
            ),
            "OperationTypeDefinitionNode("
            "operation_type='operationTypeDefinitionOperationType', "
            "type='operationTypeDefinitionType', "
            "location='operationTypeDefinitionLocation')",
        )
    ],
)
def test_operationtypedefinitionnode__repr__(
    operation_type_definition_node, expected
):
    assert operation_type_definition_node.__repr__() == expected
