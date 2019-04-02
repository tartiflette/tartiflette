import pytest

from tartiflette.language.ast import SelectionSetNode


def test_selectionsetnode__init__():
    selection_set_node = SelectionSetNode(
        selections="selectionSetSelections", location="selectionSetLocation"
    )
    assert selection_set_node.selections == "selectionSetSelections"
    assert selection_set_node.location == "selectionSetLocation"


@pytest.mark.parametrize(
    "selection_set_node,other,expected",
    [
        (
            SelectionSetNode(
                selections="selectionSetSelections",
                location="selectionSetLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            SelectionSetNode(
                selections="selectionSetSelections",
                location="selectionSetLocation",
            ),
            SelectionSetNode(
                selections="selectionSetSelectionsBis",
                location="selectionSetLocation",
            ),
            False,
        ),
        (
            SelectionSetNode(
                selections="selectionSetSelections",
                location="selectionSetLocation",
            ),
            SelectionSetNode(
                selections="selectionSetSelections",
                location="selectionSetLocationBis",
            ),
            False,
        ),
        (
            SelectionSetNode(
                selections="selectionSetSelections",
                location="selectionSetLocation",
            ),
            SelectionSetNode(
                selections="selectionSetSelections",
                location="selectionSetLocation",
            ),
            True,
        ),
    ],
)
def test_selectionsetnode__eq__(selection_set_node, other, expected):
    assert (selection_set_node == other) is expected


@pytest.mark.parametrize(
    "selection_set_node,expected",
    [
        (
            SelectionSetNode(
                selections="selectionSetSelections",
                location="selectionSetLocation",
            ),
            "SelectionSetNode("
            "selections='selectionSetSelections', "
            "location='selectionSetLocation')",
        )
    ],
)
def test_selectionsetnode__repr__(selection_set_node, expected):
    assert selection_set_node.__repr__() == expected
