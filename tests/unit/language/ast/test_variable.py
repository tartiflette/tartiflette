import pytest

from tartiflette.language.ast import VariableNode


def test_variablenode__init__():
    variable_node = VariableNode(
        name="variableName", location="variableLocation"
    )
    assert variable_node.name == "variableName"
    assert variable_node.location == "variableLocation"


@pytest.mark.parametrize(
    "variable_node,other,expected",
    [
        (
            VariableNode(name="variableName", location="variableLocation"),
            Ellipsis,
            False,
        ),
        (
            VariableNode(name="variableName", location="variableLocation"),
            VariableNode(name="variableNameBis", location="variableLocation"),
            False,
        ),
        (
            VariableNode(name="variableName", location="variableLocation"),
            VariableNode(name="variableName", location="variableLocationBis"),
            False,
        ),
        (
            VariableNode(name="variableName", location="variableLocation"),
            VariableNode(name="variableName", location="variableLocation"),
            True,
        ),
    ],
)
def test_variablenode__eq__(variable_node, other, expected):
    assert (variable_node == other) is expected


@pytest.mark.parametrize(
    "variable_node,expected",
    [
        (
            VariableNode(name="variableName", location="variableLocation"),
            "VariableNode(name='variableName', location='variableLocation')",
        )
    ],
)
def test_variablenode__repr__(variable_node, expected):
    assert variable_node.__repr__() == expected
