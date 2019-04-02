import pytest

from tartiflette.language.ast import VariableDefinitionNode


def test_variabledefinitionnode__init__():
    variable_definition_node = VariableDefinitionNode(
        variable="variableDefinitionVariable",
        type="variableDefinitionType",
        default_value="variableDefinitionDefaultValue",
        location="variableDefinitionLocation",
    )
    assert variable_definition_node.variable == "variableDefinitionVariable"
    assert variable_definition_node.type == "variableDefinitionType"
    assert (
        variable_definition_node.default_value
        == "variableDefinitionDefaultValue"
    )
    assert variable_definition_node.location == "variableDefinitionLocation"


@pytest.mark.parametrize(
    "variable_definition_node,other,expected",
    [
        (
            VariableDefinitionNode(
                variable="variableDefinitionVariable",
                type="variableDefinitionType",
                default_value="variableDefinitionDefaultValue",
                location="variableDefinitionLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            VariableDefinitionNode(
                variable="variableDefinitionVariable",
                type="variableDefinitionType",
                default_value="variableDefinitionDefaultValue",
                location="variableDefinitionLocation",
            ),
            VariableDefinitionNode(
                variable="variableDefinitionVariableBis",
                type="variableDefinitionType",
                default_value="variableDefinitionDefaultValue",
                location="variableDefinitionLocation",
            ),
            False,
        ),
        (
            VariableDefinitionNode(
                variable="variableDefinitionVariable",
                type="variableDefinitionType",
                default_value="variableDefinitionDefaultValue",
                location="variableDefinitionLocation",
            ),
            VariableDefinitionNode(
                variable="variableDefinitionVariable",
                type="variableDefinitionTypeBis",
                default_value="variableDefinitionDefaultValue",
                location="variableDefinitionLocation",
            ),
            False,
        ),
        (
            VariableDefinitionNode(
                variable="variableDefinitionVariable",
                type="variableDefinitionType",
                default_value="variableDefinitionDefaultValue",
                location="variableDefinitionLocation",
            ),
            VariableDefinitionNode(
                variable="variableDefinitionVariable",
                type="variableDefinitionType",
                default_value="variableDefinitionDefaultValueBis",
                location="variableDefinitionLocation",
            ),
            False,
        ),
        (
            VariableDefinitionNode(
                variable="variableDefinitionVariable",
                type="variableDefinitionType",
                default_value="variableDefinitionDefaultValue",
                location="variableDefinitionLocation",
            ),
            VariableDefinitionNode(
                variable="variableDefinitionVariable",
                type="variableDefinitionType",
                default_value="variableDefinitionDefaultValue",
                location="variableDefinitionLocationBis",
            ),
            False,
        ),
        (
            VariableDefinitionNode(
                variable="variableDefinitionVariable",
                type="variableDefinitionType",
                default_value="variableDefinitionDefaultValue",
                location="variableDefinitionLocation",
            ),
            VariableDefinitionNode(
                variable="variableDefinitionVariable",
                type="variableDefinitionType",
                default_value="variableDefinitionDefaultValue",
                location="variableDefinitionLocation",
            ),
            True,
        ),
    ],
)
def test_variabledefinitionnode__eq__(
    variable_definition_node, other, expected
):
    assert (variable_definition_node == other) is expected


@pytest.mark.parametrize(
    "variable_definition_node,expected",
    [
        (
            VariableDefinitionNode(
                variable="variableDefinitionVariable",
                type="variableDefinitionType",
                default_value="variableDefinitionDefaultValue",
                location="variableDefinitionLocation",
            ),
            "VariableDefinitionNode(variable='variableDefinitionVariable', "
            "type='variableDefinitionType', "
            "default_value='variableDefinitionDefaultValue', "
            "location='variableDefinitionLocation')",
        )
    ],
)
def test_variabledefinitionnode__repr__(variable_definition_node, expected):
    assert variable_definition_node.__repr__() == expected
