import pytest

from tartiflette.language.ast import DirectiveNode


def test_directivenode__init__():
    directive_node = DirectiveNode(
        name="directiveName",
        arguments="directiveArguments",
        location="directiveLocation",
    )
    assert directive_node.name == "directiveName"
    assert directive_node.arguments == "directiveArguments"
    assert directive_node.location == "directiveLocation"


@pytest.mark.parametrize(
    "directive_node,other,expected",
    [
        (
            DirectiveNode(
                name="directiveName",
                arguments="directiveArguments",
                location="directiveLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            DirectiveNode(
                name="directiveName",
                arguments="directiveArguments",
                location="directiveLocation",
            ),
            DirectiveNode(
                name="directiveNameBis",
                arguments="directiveArguments",
                location="directiveLocation",
            ),
            False,
        ),
        (
            DirectiveNode(
                name="directiveName",
                arguments="directiveArguments",
                location="directiveLocation",
            ),
            DirectiveNode(
                name="directiveName",
                arguments="directiveArgumentsBis",
                location="directiveLocation",
            ),
            False,
        ),
        (
            DirectiveNode(
                name="directiveName",
                arguments="directiveArguments",
                location="directiveLocation",
            ),
            DirectiveNode(
                name="directiveName",
                arguments="directiveArguments",
                location="directiveLocationBis",
            ),
            False,
        ),
        (
            DirectiveNode(
                name="directiveName",
                arguments="directiveArguments",
                location="directiveLocation",
            ),
            DirectiveNode(
                name="directiveName",
                arguments="directiveArguments",
                location="directiveLocation",
            ),
            True,
        ),
    ],
)
def test_directivenode__eq__(directive_node, other, expected):
    assert (directive_node == other) is expected


@pytest.mark.parametrize(
    "directive_node,expected",
    [
        (
            DirectiveNode(
                name="directiveName",
                arguments="directiveArguments",
                location="directiveLocation",
            ),
            "DirectiveNode(name='directiveName', "
            "arguments='directiveArguments', location='directiveLocation')",
        )
    ],
)
def test_directivenode__repr__(directive_node, expected):
    assert directive_node.__repr__() == expected
