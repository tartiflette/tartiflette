import pytest

from tartiflette.language.ast import FragmentSpreadNode


def test_fragmentspreadnode__init__():
    fragment_spread_node = FragmentSpreadNode(
        name="fragmentSpreadName",
        directives="fragmentSpreadDirectives",
        location="fragmentSpreadLocation",
    )
    assert fragment_spread_node.name == "fragmentSpreadName"
    assert fragment_spread_node.directives == "fragmentSpreadDirectives"
    assert fragment_spread_node.location == "fragmentSpreadLocation"


@pytest.mark.parametrize(
    "fragment_spread_node,other,expected",
    [
        (
            FragmentSpreadNode(
                name="fragmentSpreadName",
                directives="fragmentSpreadDirectives",
                location="fragmentSpreadLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            FragmentSpreadNode(
                name="fragmentSpreadName",
                directives="fragmentSpreadDirectives",
                location="fragmentSpreadLocation",
            ),
            FragmentSpreadNode(
                name="fragmentSpreadNameBis",
                directives="fragmentSpreadDirectives",
                location="fragmentSpreadLocation",
            ),
            False,
        ),
        (
            FragmentSpreadNode(
                name="fragmentSpreadName",
                directives="fragmentSpreadDirectives",
                location="fragmentSpreadLocation",
            ),
            FragmentSpreadNode(
                name="fragmentSpreadName",
                directives="fragmentSpreadDirectivesBis",
                location="fragmentSpreadLocation",
            ),
            False,
        ),
        (
            FragmentSpreadNode(
                name="fragmentSpreadName",
                directives="fragmentSpreadDirectives",
                location="fragmentSpreadLocation",
            ),
            FragmentSpreadNode(
                name="fragmentSpreadName",
                directives="fragmentSpreadDirectives",
                location="fragmentSpreadLocationBis",
            ),
            False,
        ),
        (
            FragmentSpreadNode(
                name="fragmentSpreadName",
                directives="fragmentSpreadDirectives",
                location="fragmentSpreadLocation",
            ),
            FragmentSpreadNode(
                name="fragmentSpreadName",
                directives="fragmentSpreadDirectives",
                location="fragmentSpreadLocation",
            ),
            True,
        ),
    ],
)
def test_fragmentspreadnode__eq__(fragment_spread_node, other, expected):
    assert (fragment_spread_node == other) is expected


@pytest.mark.parametrize(
    "fragment_spread_node,expected",
    [
        (
            FragmentSpreadNode(
                name="fragmentSpreadName",
                directives="fragmentSpreadDirectives",
                location="fragmentSpreadLocation",
            ),
            "FragmentSpreadNode("
            "name='fragmentSpreadName', "
            "directives='fragmentSpreadDirectives', "
            "location='fragmentSpreadLocation')",
        )
    ],
)
def test_fragmentspreadnode__repr__(fragment_spread_node, expected):
    assert fragment_spread_node.__repr__() == expected
