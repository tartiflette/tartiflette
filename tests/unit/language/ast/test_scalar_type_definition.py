import pytest

from tartiflette.language.ast import ScalarTypeDefinitionNode


def test_scalartypedefinitionnode__init__():
    scalar_type_definition_node = ScalarTypeDefinitionNode(
        name="scalarTypeDefinitionName",
        description="scalarTypeDefinitionDescription",
        directives="scalarTypeDefinitionDirectives",
        location="scalarTypeDefinitionLocation",
    )
    assert scalar_type_definition_node.name == "scalarTypeDefinitionName"
    assert (
        scalar_type_definition_node.description
        == "scalarTypeDefinitionDescription"
    )
    assert (
        scalar_type_definition_node.directives
        == "scalarTypeDefinitionDirectives"
    )
    assert (
        scalar_type_definition_node.location == "scalarTypeDefinitionLocation"
    )


@pytest.mark.parametrize(
    "scalar_type_definition_node,other,expected",
    [
        (
            ScalarTypeDefinitionNode(
                name="scalarTypeDefinitionName",
                description="scalarTypeDefinitionDescription",
                directives="scalarTypeDefinitionDirectives",
                location="scalarTypeDefinitionLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            ScalarTypeDefinitionNode(
                name="scalarTypeDefinitionName",
                description="scalarTypeDefinitionDescription",
                directives="scalarTypeDefinitionDirectives",
                location="scalarTypeDefinitionLocation",
            ),
            ScalarTypeDefinitionNode(
                name="scalarTypeDefinitionNameBis",
                description="scalarTypeDefinitionDescription",
                directives="scalarTypeDefinitionDirectives",
                location="scalarTypeDefinitionLocation",
            ),
            False,
        ),
        (
            ScalarTypeDefinitionNode(
                name="scalarTypeDefinitionName",
                description="scalarTypeDefinitionDescription",
                directives="scalarTypeDefinitionDirectives",
                location="scalarTypeDefinitionLocation",
            ),
            ScalarTypeDefinitionNode(
                name="scalarTypeDefinitionName",
                description="scalarTypeDefinitionDescriptionBis",
                directives="scalarTypeDefinitionDirectives",
                location="scalarTypeDefinitionLocation",
            ),
            False,
        ),
        (
            ScalarTypeDefinitionNode(
                name="scalarTypeDefinitionName",
                description="scalarTypeDefinitionDescription",
                directives="scalarTypeDefinitionDirectives",
                location="scalarTypeDefinitionLocation",
            ),
            ScalarTypeDefinitionNode(
                name="scalarTypeDefinitionName",
                description="scalarTypeDefinitionDescription",
                directives="scalarTypeDefinitionDirectivesBis",
                location="scalarTypeDefinitionLocation",
            ),
            False,
        ),
        (
            ScalarTypeDefinitionNode(
                name="scalarTypeDefinitionName",
                description="scalarTypeDefinitionDescription",
                directives="scalarTypeDefinitionDirectives",
                location="scalarTypeDefinitionLocation",
            ),
            ScalarTypeDefinitionNode(
                name="scalarTypeDefinitionName",
                description="scalarTypeDefinitionDescription",
                directives="scalarTypeDefinitionDirectives",
                location="scalarTypeDefinitionLocationBis",
            ),
            False,
        ),
        (
            ScalarTypeDefinitionNode(
                name="scalarTypeDefinitionName",
                description="scalarTypeDefinitionDescription",
                directives="scalarTypeDefinitionDirectives",
                location="scalarTypeDefinitionLocation",
            ),
            ScalarTypeDefinitionNode(
                name="scalarTypeDefinitionName",
                description="scalarTypeDefinitionDescription",
                directives="scalarTypeDefinitionDirectives",
                location="scalarTypeDefinitionLocation",
            ),
            True,
        ),
    ],
)
def test_scalartypedefinitionnode__eq__(
    scalar_type_definition_node, other, expected
):
    assert (scalar_type_definition_node == other) is expected


@pytest.mark.parametrize(
    "scalar_type_definition_node,expected",
    [
        (
            ScalarTypeDefinitionNode(
                name="scalarTypeDefinitionName",
                description="scalarTypeDefinitionDescription",
                directives="scalarTypeDefinitionDirectives",
                location="scalarTypeDefinitionLocation",
            ),
            "ScalarTypeDefinitionNode("
            "description='scalarTypeDefinitionDescription', "
            "name='scalarTypeDefinitionName', "
            "directives='scalarTypeDefinitionDirectives', "
            "location='scalarTypeDefinitionLocation')",
        )
    ],
)
def test_scalartypedefinitionnode__repr__(
    scalar_type_definition_node, expected
):
    assert scalar_type_definition_node.__repr__() == expected
