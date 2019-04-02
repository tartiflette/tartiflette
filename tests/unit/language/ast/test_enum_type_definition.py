import pytest

from tartiflette.language.ast import EnumTypeDefinitionNode


def test_enumtypedefinitionnode__init__():
    enum_type_definition_node = EnumTypeDefinitionNode(
        name="enumTypeDefinitionName",
        description="enumTypeDefinitionDescription",
        directives="enumTypeDefinitionDirectives",
        values="enumTypeDefinitionValues",
        location="enumTypeDefinitionLocation",
    )
    assert enum_type_definition_node.name == "enumTypeDefinitionName"
    assert (
        enum_type_definition_node.description
        == "enumTypeDefinitionDescription"
    )
    assert (
        enum_type_definition_node.directives == "enumTypeDefinitionDirectives"
    )
    assert enum_type_definition_node.values == "enumTypeDefinitionValues"
    assert enum_type_definition_node.location == "enumTypeDefinitionLocation"


@pytest.mark.parametrize(
    "enum_type_definition_node,other,expected",
    [
        (
            EnumTypeDefinitionNode(
                name="enumTypeDefinitionName",
                description="enumTypeDefinitionDescription",
                directives="enumTypeDefinitionDirectives",
                values="enumTypeDefinitionValues",
                location="enumTypeDefinitionLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            EnumTypeDefinitionNode(
                name="enumTypeDefinitionName",
                description="enumTypeDefinitionDescription",
                directives="enumTypeDefinitionDirectives",
                values="enumTypeDefinitionValues",
                location="enumTypeDefinitionLocation",
            ),
            EnumTypeDefinitionNode(
                name="enumTypeDefinitionNameBis",
                description="enumTypeDefinitionDescription",
                directives="enumTypeDefinitionDirectives",
                values="enumTypeDefinitionValues",
                location="enumTypeDefinitionLocation",
            ),
            False,
        ),
        (
            EnumTypeDefinitionNode(
                name="enumTypeDefinitionName",
                description="enumTypeDefinitionDescription",
                directives="enumTypeDefinitionDirectives",
                values="enumTypeDefinitionValues",
                location="enumTypeDefinitionLocation",
            ),
            EnumTypeDefinitionNode(
                name="enumTypeDefinitionName",
                description="enumTypeDefinitionDescriptionBis",
                directives="enumTypeDefinitionDirectives",
                values="enumTypeDefinitionValues",
                location="enumTypeDefinitionLocation",
            ),
            False,
        ),
        (
            EnumTypeDefinitionNode(
                name="enumTypeDefinitionName",
                description="enumTypeDefinitionDescription",
                directives="enumTypeDefinitionDirectives",
                values="enumTypeDefinitionValues",
                location="enumTypeDefinitionLocation",
            ),
            EnumTypeDefinitionNode(
                name="enumTypeDefinitionName",
                description="enumTypeDefinitionDescription",
                directives="enumTypeDefinitionDirectivesBis",
                values="enumTypeDefinitionValues",
                location="enumTypeDefinitionLocation",
            ),
            False,
        ),
        (
            EnumTypeDefinitionNode(
                name="enumTypeDefinitionName",
                description="enumTypeDefinitionDescription",
                directives="enumTypeDefinitionDirectives",
                values="enumTypeDefinitionValues",
                location="enumTypeDefinitionLocation",
            ),
            EnumTypeDefinitionNode(
                name="enumTypeDefinitionName",
                description="enumTypeDefinitionDescription",
                directives="enumTypeDefinitionDirectives",
                values="enumTypeDefinitionValuesBis",
                location="enumTypeDefinitionLocation",
            ),
            False,
        ),
        (
            EnumTypeDefinitionNode(
                name="enumTypeDefinitionName",
                description="enumTypeDefinitionDescription",
                directives="enumTypeDefinitionDirectives",
                values="enumTypeDefinitionValues",
                location="enumTypeDefinitionLocation",
            ),
            EnumTypeDefinitionNode(
                name="enumTypeDefinitionName",
                description="enumTypeDefinitionDescription",
                directives="enumTypeDefinitionDirectives",
                values="enumTypeDefinitionValues",
                location="enumTypeDefinitionLocationBis",
            ),
            False,
        ),
        (
            EnumTypeDefinitionNode(
                name="enumTypeDefinitionName",
                description="enumTypeDefinitionDescription",
                directives="enumTypeDefinitionDirectives",
                values="enumTypeDefinitionValues",
                location="enumTypeDefinitionLocation",
            ),
            EnumTypeDefinitionNode(
                name="enumTypeDefinitionName",
                description="enumTypeDefinitionDescription",
                directives="enumTypeDefinitionDirectives",
                values="enumTypeDefinitionValues",
                location="enumTypeDefinitionLocation",
            ),
            True,
        ),
    ],
)
def test_enumtypedefinitionnode__eq__(
    enum_type_definition_node, other, expected
):
    assert (enum_type_definition_node == other) is expected


@pytest.mark.parametrize(
    "enum_type_definition_node,expected",
    [
        (
            EnumTypeDefinitionNode(
                name="enumTypeDefinitionName",
                description="enumTypeDefinitionDescription",
                directives="enumTypeDefinitionDirectives",
                values="enumTypeDefinitionValues",
                location="enumTypeDefinitionLocation",
            ),
            "EnumTypeDefinitionNode("
            "description='enumTypeDefinitionDescription', "
            "name='enumTypeDefinitionName', "
            "directives='enumTypeDefinitionDirectives', "
            "values='enumTypeDefinitionValues', "
            "location='enumTypeDefinitionLocation')",
        )
    ],
)
def test_enumtypedefinitionnode__repr__(enum_type_definition_node, expected):
    assert enum_type_definition_node.__repr__() == expected
