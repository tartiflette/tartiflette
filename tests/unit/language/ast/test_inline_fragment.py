import pytest

from tartiflette.language.ast import InlineFragmentNode


def test_inlinefragmentnode__init__():
    inline_fragment_node = InlineFragmentNode(
        selection_set="inlineFragmentSelectionSet",
        type_condition="inlineFragmentTypeCondition",
        directives="inlineFragmentDirectives",
        location="inlineFragmentLocation",
    )
    assert inline_fragment_node.selection_set == "inlineFragmentSelectionSet"
    assert inline_fragment_node.type_condition == "inlineFragmentTypeCondition"
    assert inline_fragment_node.directives == "inlineFragmentDirectives"
    assert inline_fragment_node.location == "inlineFragmentLocation"


@pytest.mark.parametrize(
    "inline_fragment_node,other,expected",
    [
        (
            InlineFragmentNode(
                selection_set="inlineFragmentSelectionSet",
                type_condition="inlineFragmentTypeCondition",
                directives="inlineFragmentDirectives",
                location="inlineFragmentLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            InlineFragmentNode(
                selection_set="inlineFragmentSelectionSet",
                type_condition="inlineFragmentTypeCondition",
                directives="inlineFragmentDirectives",
                location="inlineFragmentLocation",
            ),
            InlineFragmentNode(
                selection_set="inlineFragmentSelectionSetBis",
                type_condition="inlineFragmentTypeCondition",
                directives="inlineFragmentDirectives",
                location="inlineFragmentLocation",
            ),
            False,
        ),
        (
            InlineFragmentNode(
                selection_set="inlineFragmentSelectionSet",
                type_condition="inlineFragmentTypeCondition",
                directives="inlineFragmentDirectives",
                location="inlineFragmentLocation",
            ),
            InlineFragmentNode(
                selection_set="inlineFragmentSelectionSet",
                type_condition="inlineFragmentTypeConditionBis",
                directives="inlineFragmentDirectives",
                location="inlineFragmentLocation",
            ),
            False,
        ),
        (
            InlineFragmentNode(
                selection_set="inlineFragmentSelectionSet",
                type_condition="inlineFragmentTypeCondition",
                directives="inlineFragmentDirectives",
                location="inlineFragmentLocation",
            ),
            InlineFragmentNode(
                selection_set="inlineFragmentSelectionSet",
                type_condition="inlineFragmentTypeCondition",
                directives="inlineFragmentDirectivesBis",
                location="inlineFragmentLocation",
            ),
            False,
        ),
        (
            InlineFragmentNode(
                selection_set="inlineFragmentSelectionSet",
                type_condition="inlineFragmentTypeCondition",
                directives="inlineFragmentDirectives",
                location="inlineFragmentLocation",
            ),
            InlineFragmentNode(
                selection_set="inlineFragmentSelectionSet",
                type_condition="inlineFragmentTypeCondition",
                directives="inlineFragmentDirectives",
                location="inlineFragmentLocationBis",
            ),
            False,
        ),
        (
            InlineFragmentNode(
                selection_set="inlineFragmentSelectionSet",
                type_condition="inlineFragmentTypeCondition",
                directives="inlineFragmentDirectives",
                location="inlineFragmentLocation",
            ),
            InlineFragmentNode(
                selection_set="inlineFragmentSelectionSet",
                type_condition="inlineFragmentTypeCondition",
                directives="inlineFragmentDirectives",
                location="inlineFragmentLocation",
            ),
            True,
        ),
    ],
)
def test_inlinefragmentnode__eq__(inline_fragment_node, other, expected):
    assert (inline_fragment_node == other) is expected


@pytest.mark.parametrize(
    "inline_fragment_node,expected",
    [
        (
            InlineFragmentNode(
                selection_set="inlineFragmentSelectionSet",
                type_condition="inlineFragmentTypeCondition",
                directives="inlineFragmentDirectives",
                location="inlineFragmentLocation",
            ),
            "InlineFragmentNode("
            "type_condition='inlineFragmentTypeCondition', "
            "directives='inlineFragmentDirectives', "
            "selection_set='inlineFragmentSelectionSet', "
            "location='inlineFragmentLocation')",
        )
    ],
)
def test_inlinefragmentnode__repr__(inline_fragment_node, expected):
    assert inline_fragment_node.__repr__() == expected
