import pytest

from tartiflette.language.ast import UnionTypeDefinitionNode


def test_uniontypedefinitionnode__init__():
    union_type_definition_node = UnionTypeDefinitionNode(
        name="unionTypeDefinitionName",
        description="unionTypeDefinitionDescription",
        directives="unionTypeDefinitionDirectives",
        types="unionTypeDefinitionTypes",
        location="unionTypeDefinitionLocation",
    )
    assert union_type_definition_node.name == "unionTypeDefinitionName"
    assert (
        union_type_definition_node.description
        == "unionTypeDefinitionDescription"
    )
    assert (
        union_type_definition_node.directives
        == "unionTypeDefinitionDirectives"
    )
    assert union_type_definition_node.types == "unionTypeDefinitionTypes"
    assert union_type_definition_node.location == "unionTypeDefinitionLocation"


@pytest.mark.parametrize(
    "union_type_definition_node,other,expected",
    [
        (
            UnionTypeDefinitionNode(
                name="unionTypeDefinitionName",
                description="unionTypeDefinitionDescription",
                directives="unionTypeDefinitionDirectives",
                types="unionTypeDefinitionTypes",
                location="unionTypeDefinitionLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            UnionTypeDefinitionNode(
                name="unionTypeDefinitionName",
                description="unionTypeDefinitionDescription",
                directives="unionTypeDefinitionDirectives",
                types="unionTypeDefinitionTypes",
                location="unionTypeDefinitionLocation",
            ),
            UnionTypeDefinitionNode(
                name="unionTypeDefinitionNameBis",
                description="unionTypeDefinitionDescription",
                directives="unionTypeDefinitionDirectives",
                types="unionTypeDefinitionTypes",
                location="unionTypeDefinitionLocation",
            ),
            False,
        ),
        (
            UnionTypeDefinitionNode(
                name="unionTypeDefinitionName",
                description="unionTypeDefinitionDescription",
                directives="unionTypeDefinitionDirectives",
                types="unionTypeDefinitionTypes",
                location="unionTypeDefinitionLocation",
            ),
            UnionTypeDefinitionNode(
                name="unionTypeDefinitionName",
                description="unionTypeDefinitionDescriptionBis",
                directives="unionTypeDefinitionDirectives",
                types="unionTypeDefinitionTypes",
                location="unionTypeDefinitionLocation",
            ),
            False,
        ),
        (
            UnionTypeDefinitionNode(
                name="unionTypeDefinitionName",
                description="unionTypeDefinitionDescription",
                directives="unionTypeDefinitionDirectives",
                types="unionTypeDefinitionTypes",
                location="unionTypeDefinitionLocation",
            ),
            UnionTypeDefinitionNode(
                name="unionTypeDefinitionName",
                description="unionTypeDefinitionDescription",
                directives="unionTypeDefinitionDirectivesBis",
                types="unionTypeDefinitionTypes",
                location="unionTypeDefinitionLocation",
            ),
            False,
        ),
        (
            UnionTypeDefinitionNode(
                name="unionTypeDefinitionName",
                description="unionTypeDefinitionDescription",
                directives="unionTypeDefinitionDirectives",
                types="unionTypeDefinitionTypes",
                location="unionTypeDefinitionLocation",
            ),
            UnionTypeDefinitionNode(
                name="unionTypeDefinitionName",
                description="unionTypeDefinitionDescription",
                directives="unionTypeDefinitionDirectives",
                types="unionTypeDefinitionTypesBis",
                location="unionTypeDefinitionLocation",
            ),
            False,
        ),
        (
            UnionTypeDefinitionNode(
                name="unionTypeDefinitionName",
                description="unionTypeDefinitionDescription",
                directives="unionTypeDefinitionDirectives",
                types="unionTypeDefinitionTypes",
                location="unionTypeDefinitionLocation",
            ),
            UnionTypeDefinitionNode(
                name="unionTypeDefinitionName",
                description="unionTypeDefinitionDescription",
                directives="unionTypeDefinitionDirectives",
                types="unionTypeDefinitionTypes",
                location="unionTypeDefinitionLocationBis",
            ),
            False,
        ),
        (
            UnionTypeDefinitionNode(
                name="unionTypeDefinitionName",
                description="unionTypeDefinitionDescription",
                directives="unionTypeDefinitionDirectives",
                types="unionTypeDefinitionTypes",
                location="unionTypeDefinitionLocation",
            ),
            UnionTypeDefinitionNode(
                name="unionTypeDefinitionName",
                description="unionTypeDefinitionDescription",
                directives="unionTypeDefinitionDirectives",
                types="unionTypeDefinitionTypes",
                location="unionTypeDefinitionLocation",
            ),
            True,
        ),
    ],
)
def test_uniontypedefinitionnode__eq__(
    union_type_definition_node, other, expected
):
    assert (union_type_definition_node == other) is expected


@pytest.mark.parametrize(
    "union_type_definition_node,expected",
    [
        (
            UnionTypeDefinitionNode(
                name="unionTypeDefinitionName",
                description="unionTypeDefinitionDescription",
                directives="unionTypeDefinitionDirectives",
                types="unionTypeDefinitionTypes",
                location="unionTypeDefinitionLocation",
            ),
            "UnionTypeDefinitionNode("
            "description='unionTypeDefinitionDescription', "
            "name='unionTypeDefinitionName', "
            "directives='unionTypeDefinitionDirectives', "
            "types='unionTypeDefinitionTypes', "
            "location='unionTypeDefinitionLocation')",
        )
    ],
)
def test_uniontypedefinitionnode__repr__(union_type_definition_node, expected):
    assert union_type_definition_node.__repr__() == expected
