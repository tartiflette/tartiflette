import pytest

from tartiflette.language.ast import DirectiveDefinitionNode


def test_directivedefinitionnode__init__():
    directive_definition_node = DirectiveDefinitionNode(
        name="directiveDefinitionName",
        locations="directiveDefinitionLocations",
        description="directiveDefinitionDescription",
        arguments="directiveDefinitionArguments",
        location="directiveDefinitionLocation",
    )
    assert directive_definition_node.name == "directiveDefinitionName"
    assert (
        directive_definition_node.locations == "directiveDefinitionLocations"
    )
    assert (
        directive_definition_node.description
        == "directiveDefinitionDescription"
    )
    assert (
        directive_definition_node.arguments == "directiveDefinitionArguments"
    )
    assert directive_definition_node.location == "directiveDefinitionLocation"


@pytest.mark.parametrize(
    "directive_definition_node,other,expected",
    [
        (
            DirectiveDefinitionNode(
                name="directiveDefinitionName",
                locations="directiveDefinitionLocations",
                description="directiveDefinitionDescription",
                arguments="directiveDefinitionArguments",
                location="directiveDefinitionLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            DirectiveDefinitionNode(
                name="directiveDefinitionName",
                locations="directiveDefinitionLocations",
                description="directiveDefinitionDescription",
                arguments="directiveDefinitionArguments",
                location="directiveDefinitionLocation",
            ),
            DirectiveDefinitionNode(
                name="directiveDefinitionNameBis",
                locations="directiveDefinitionLocations",
                description="directiveDefinitionDescription",
                arguments="directiveDefinitionArguments",
                location="directiveDefinitionLocation",
            ),
            False,
        ),
        (
            DirectiveDefinitionNode(
                name="directiveDefinitionName",
                locations="directiveDefinitionLocations",
                description="directiveDefinitionDescription",
                arguments="directiveDefinitionArguments",
                location="directiveDefinitionLocation",
            ),
            DirectiveDefinitionNode(
                name="directiveDefinitionName",
                locations="directiveDefinitionLocationsBis",
                description="directiveDefinitionDescription",
                arguments="directiveDefinitionArguments",
                location="directiveDefinitionLocation",
            ),
            False,
        ),
        (
            DirectiveDefinitionNode(
                name="directiveDefinitionName",
                locations="directiveDefinitionLocations",
                description="directiveDefinitionDescription",
                arguments="directiveDefinitionArguments",
                location="directiveDefinitionLocation",
            ),
            DirectiveDefinitionNode(
                name="directiveDefinitionName",
                locations="directiveDefinitionLocations",
                description="directiveDefinitionDescriptionBis",
                arguments="directiveDefinitionArguments",
                location="directiveDefinitionLocation",
            ),
            False,
        ),
        (
            DirectiveDefinitionNode(
                name="directiveDefinitionName",
                locations="directiveDefinitionLocations",
                description="directiveDefinitionDescription",
                arguments="directiveDefinitionArguments",
                location="directiveDefinitionLocation",
            ),
            DirectiveDefinitionNode(
                name="directiveDefinitionName",
                locations="directiveDefinitionLocations",
                description="directiveDefinitionDescription",
                arguments="directiveDefinitionArgumentsBis",
                location="directiveDefinitionLocation",
            ),
            False,
        ),
        (
            DirectiveDefinitionNode(
                name="directiveDefinitionName",
                locations="directiveDefinitionLocations",
                description="directiveDefinitionDescription",
                arguments="directiveDefinitionArguments",
                location="directiveDefinitionLocation",
            ),
            DirectiveDefinitionNode(
                name="directiveDefinitionName",
                locations="directiveDefinitionLocations",
                description="directiveDefinitionDescription",
                arguments="directiveDefinitionArguments",
                location="directiveDefinitionLocationBis",
            ),
            False,
        ),
        (
            DirectiveDefinitionNode(
                name="directiveDefinitionName",
                locations="directiveDefinitionLocations",
                description="directiveDefinitionDescription",
                arguments="directiveDefinitionArguments",
                location="directiveDefinitionLocation",
            ),
            DirectiveDefinitionNode(
                name="directiveDefinitionName",
                locations="directiveDefinitionLocations",
                description="directiveDefinitionDescription",
                arguments="directiveDefinitionArguments",
                location="directiveDefinitionLocation",
            ),
            True,
        ),
    ],
)
def test_directivedefinitionnode__eq__(
    directive_definition_node, other, expected
):
    assert (directive_definition_node == other) is expected


@pytest.mark.parametrize(
    "directive_definition_node,expected",
    [
        (
            DirectiveDefinitionNode(
                name="directiveDefinitionName",
                locations="directiveDefinitionLocations",
                description="directiveDefinitionDescription",
                arguments="directiveDefinitionArguments",
                location="directiveDefinitionLocation",
            ),
            "DirectiveDefinitionNode("
            "description='directiveDefinitionDescription', "
            "name='directiveDefinitionName', "
            "arguments='directiveDefinitionArguments', "
            "locations='directiveDefinitionLocations', "
            "location='directiveDefinitionLocation')",
        )
    ],
)
def test_directivedefinitionnode__repr__(directive_definition_node, expected):
    assert directive_definition_node.__repr__() == expected
