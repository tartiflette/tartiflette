import pytest

from tartiflette.language.ast import OperationDefinitionNode


def test_operationdefinitionnode__init__():
    operation_definition_node = OperationDefinitionNode(
        operation_type="operationDefinitionOperationType",
        selection_set="operationDefinitionSelectionSet",
        name="operationDefinitionName",
        variable_definitions="operationDefinitionVariableDefinitions",
        directives="operationDefinitionDirectives",
        location="operationDefinitionLocation",
    )
    assert (
        operation_definition_node.operation_type
        == "operationDefinitionOperationType"
    )
    assert (
        operation_definition_node.selection_set
        == "operationDefinitionSelectionSet"
    )
    assert operation_definition_node.name == "operationDefinitionName"
    assert (
        operation_definition_node.variable_definitions
        == "operationDefinitionVariableDefinitions"
    )
    assert (
        operation_definition_node.directives == "operationDefinitionDirectives"
    )
    assert operation_definition_node.location == "operationDefinitionLocation"


@pytest.mark.parametrize(
    "operation_definition_node,other,expected",
    [
        (
            OperationDefinitionNode(
                operation_type="operationDefinitionOperationType",
                selection_set="operationDefinitionSelectionSet",
                name="operationDefinitionName",
                variable_definitions="operationDefinitionVariableDefinitions",
                directives="operationDefinitionDirectives",
                location="operationDefinitionLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            OperationDefinitionNode(
                operation_type="operationDefinitionOperationType",
                selection_set="operationDefinitionSelectionSet",
                name="operationDefinitionName",
                variable_definitions="operationDefinitionVariableDefinitions",
                directives="operationDefinitionDirectives",
                location="operationDefinitionLocation",
            ),
            OperationDefinitionNode(
                operation_type="operationDefinitionOperationTypeBis",
                selection_set="operationDefinitionSelectionSet",
                name="operationDefinitionName",
                variable_definitions="operationDefinitionVariableDefinitions",
                directives="operationDefinitionDirectives",
                location="operationDefinitionLocation",
            ),
            False,
        ),
        (
            OperationDefinitionNode(
                operation_type="operationDefinitionOperationType",
                selection_set="operationDefinitionSelectionSet",
                name="operationDefinitionName",
                variable_definitions="operationDefinitionVariableDefinitions",
                directives="operationDefinitionDirectives",
                location="operationDefinitionLocation",
            ),
            OperationDefinitionNode(
                operation_type="operationDefinitionOperationType",
                selection_set="operationDefinitionSelectionSetBis",
                name="operationDefinitionName",
                variable_definitions="operationDefinitionVariableDefinitions",
                directives="operationDefinitionDirectives",
                location="operationDefinitionLocation",
            ),
            False,
        ),
        (
            OperationDefinitionNode(
                operation_type="operationDefinitionOperationType",
                selection_set="operationDefinitionSelectionSet",
                name="operationDefinitionName",
                variable_definitions="operationDefinitionVariableDefinitions",
                directives="operationDefinitionDirectives",
                location="operationDefinitionLocation",
            ),
            OperationDefinitionNode(
                operation_type="operationDefinitionOperationType",
                selection_set="operationDefinitionSelectionSet",
                name="operationDefinitionNameBis",
                variable_definitions="operationDefinitionVariableDefinitions",
                directives="operationDefinitionDirectives",
                location="operationDefinitionLocation",
            ),
            False,
        ),
        (
            OperationDefinitionNode(
                operation_type="operationDefinitionOperationType",
                selection_set="operationDefinitionSelectionSet",
                name="operationDefinitionName",
                variable_definitions="operationDefinitionVariableDefinitions",
                directives="operationDefinitionDirectives",
                location="operationDefinitionLocation",
            ),
            OperationDefinitionNode(
                operation_type="operationDefinitionOperationType",
                selection_set="operationDefinitionSelectionSet",
                name="operationDefinitionName",
                variable_definitions="operationDefinitionVariableDefinitionsBis",
                directives="operationDefinitionDirectives",
                location="operationDefinitionLocation",
            ),
            False,
        ),
        (
            OperationDefinitionNode(
                operation_type="operationDefinitionOperationType",
                selection_set="operationDefinitionSelectionSet",
                name="operationDefinitionName",
                variable_definitions="operationDefinitionVariableDefinitions",
                directives="operationDefinitionDirectives",
                location="operationDefinitionLocation",
            ),
            OperationDefinitionNode(
                operation_type="operationDefinitionOperationType",
                selection_set="operationDefinitionSelectionSet",
                name="operationDefinitionName",
                variable_definitions="operationDefinitionVariableDefinitions",
                directives="operationDefinitionDirectivesBis",
                location="operationDefinitionLocation",
            ),
            False,
        ),
        (
            OperationDefinitionNode(
                operation_type="operationDefinitionOperationType",
                selection_set="operationDefinitionSelectionSet",
                name="operationDefinitionName",
                variable_definitions="operationDefinitionVariableDefinitions",
                directives="operationDefinitionDirectives",
                location="operationDefinitionLocation",
            ),
            OperationDefinitionNode(
                operation_type="operationDefinitionOperationType",
                selection_set="operationDefinitionSelectionSet",
                name="operationDefinitionName",
                variable_definitions="operationDefinitionVariableDefinitions",
                directives="operationDefinitionDirectives",
                location="operationDefinitionLocationBis",
            ),
            False,
        ),
        (
            OperationDefinitionNode(
                operation_type="operationDefinitionOperationType",
                selection_set="operationDefinitionSelectionSet",
                name="operationDefinitionName",
                variable_definitions="operationDefinitionVariableDefinitions",
                directives="operationDefinitionDirectives",
                location="operationDefinitionLocation",
            ),
            OperationDefinitionNode(
                operation_type="operationDefinitionOperationType",
                selection_set="operationDefinitionSelectionSet",
                name="operationDefinitionName",
                variable_definitions="operationDefinitionVariableDefinitions",
                directives="operationDefinitionDirectives",
                location="operationDefinitionLocation",
            ),
            True,
        ),
    ],
)
def test_operationdefinitionnode__eq__(
    operation_definition_node, other, expected
):
    assert (operation_definition_node == other) is expected


@pytest.mark.parametrize(
    "operation_definition_node,expected",
    [
        (
            OperationDefinitionNode(
                operation_type="operationDefinitionOperationType",
                selection_set="operationDefinitionSelectionSet",
                name="operationDefinitionName",
                variable_definitions="operationDefinitionVariableDefinitions",
                directives="operationDefinitionDirectives",
                location="operationDefinitionLocation",
            ),
            "OperationDefinitionNode("
            "operation_type='operationDefinitionOperationType', "
            "name='operationDefinitionName', "
            "variable_definitions='operationDefinitionVariableDefinitions', "
            "directives='operationDefinitionDirectives', "
            "selection_set='operationDefinitionSelectionSet', "
            "location='operationDefinitionLocation')",
        )
    ],
)
def test_operationdefinitionnode__repr__(operation_definition_node, expected):
    assert operation_definition_node.__repr__() == expected
