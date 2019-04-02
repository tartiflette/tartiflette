import pytest

from tartiflette.language.ast import EnumValueDefinitionNode


def test_enumvaluedefinitionnode__init__():
    enum_value_definition_node = EnumValueDefinitionNode(
        name="enumValueDefinitionName",
        description="enumValueDefinitionDescription",
        directives="enumValueDefinitionDirectives",
        location="enumValueDefinitionLocation",
    )
    assert enum_value_definition_node.name == "enumValueDefinitionName"
    assert (
        enum_value_definition_node.description
        == "enumValueDefinitionDescription"
    )
    assert (
        enum_value_definition_node.directives
        == "enumValueDefinitionDirectives"
    )
    assert enum_value_definition_node.location == "enumValueDefinitionLocation"


@pytest.mark.parametrize(
    "enum_value_definition_node,other,expected",
    [
        (
            EnumValueDefinitionNode(
                name="enumValueDefinitionName",
                description="enumValueDefinitionDescription",
                directives="enumValueDefinitionDirectives",
                location="enumValueDefinitionLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            EnumValueDefinitionNode(
                name="enumValueDefinitionName",
                description="enumValueDefinitionDescription",
                directives="enumValueDefinitionDirectives",
                location="enumValueDefinitionLocation",
            ),
            EnumValueDefinitionNode(
                name="enumValueDefinitionNameBis",
                description="enumValueDefinitionDescription",
                directives="enumValueDefinitionDirectives",
                location="enumValueDefinitionLocation",
            ),
            False,
        ),
        (
            EnumValueDefinitionNode(
                name="enumValueDefinitionName",
                description="enumValueDefinitionDescription",
                directives="enumValueDefinitionDirectives",
                location="enumValueDefinitionLocation",
            ),
            EnumValueDefinitionNode(
                name="enumValueDefinitionName",
                description="enumValueDefinitionDescriptionBis",
                directives="enumValueDefinitionDirectives",
                location="enumValueDefinitionLocation",
            ),
            False,
        ),
        (
            EnumValueDefinitionNode(
                name="enumValueDefinitionName",
                description="enumValueDefinitionDescription",
                directives="enumValueDefinitionDirectives",
                location="enumValueDefinitionLocation",
            ),
            EnumValueDefinitionNode(
                name="enumValueDefinitionName",
                description="enumValueDefinitionDescription",
                directives="enumValueDefinitionDirectivesBis",
                location="enumValueDefinitionLocation",
            ),
            False,
        ),
        (
            EnumValueDefinitionNode(
                name="enumValueDefinitionName",
                description="enumValueDefinitionDescription",
                directives="enumValueDefinitionDirectives",
                location="enumValueDefinitionLocation",
            ),
            EnumValueDefinitionNode(
                name="enumValueDefinitionName",
                description="enumValueDefinitionDescription",
                directives="enumValueDefinitionDirectives",
                location="enumValueDefinitionLocationBis",
            ),
            False,
        ),
        (
            EnumValueDefinitionNode(
                name="enumValueDefinitionName",
                description="enumValueDefinitionDescription",
                directives="enumValueDefinitionDirectives",
                location="enumValueDefinitionLocation",
            ),
            EnumValueDefinitionNode(
                name="enumValueDefinitionName",
                description="enumValueDefinitionDescription",
                directives="enumValueDefinitionDirectives",
                location="enumValueDefinitionLocation",
            ),
            True,
        ),
    ],
)
def test_enumvaluedefinitionnode__eq__(
    enum_value_definition_node, other, expected
):
    assert (enum_value_definition_node == other) is expected


@pytest.mark.parametrize(
    "enum_value_definition_node,expected",
    [
        (
            EnumValueDefinitionNode(
                name="enumValueDefinitionName",
                description="enumValueDefinitionDescription",
                directives="enumValueDefinitionDirectives",
                location="enumValueDefinitionLocation",
            ),
            "EnumValueDefinitionNode("
            "description='enumValueDefinitionDescription', "
            "name='enumValueDefinitionName', "
            "directives='enumValueDefinitionDirectives', "
            "location='enumValueDefinitionLocation')",
        )
    ],
)
def test_enumvaluedefinitionnode__repr__(enum_value_definition_node, expected):
    assert enum_value_definition_node.__repr__() == expected
