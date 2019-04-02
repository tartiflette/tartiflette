import pytest

from tartiflette.language.ast import FieldDefinitionNode


def test_fielddefinitionnode__init__():
    field_definition_node = FieldDefinitionNode(
        name="fieldDefinitionName",
        type="fieldDefinitionType",
        description="fieldDefinitionDescription",
        arguments="fieldDefinitionArguments",
        directives="fieldDefinitionDirectives",
        location="fieldDefinitionLocation",
    )
    assert field_definition_node.name == "fieldDefinitionName"
    assert field_definition_node.type == "fieldDefinitionType"
    assert field_definition_node.description == "fieldDefinitionDescription"
    assert field_definition_node.arguments == "fieldDefinitionArguments"
    assert field_definition_node.directives == "fieldDefinitionDirectives"
    assert field_definition_node.location == "fieldDefinitionLocation"


@pytest.mark.parametrize(
    "field_definition_node,other,expected",
    [
        (
            FieldDefinitionNode(
                name="fieldDefinitionName",
                type="fieldDefinitionType",
                description="fieldDefinitionDescription",
                arguments="fieldDefinitionArguments",
                directives="fieldDefinitionDirectives",
                location="fieldDefinitionLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            FieldDefinitionNode(
                name="fieldDefinitionName",
                type="fieldDefinitionType",
                description="fieldDefinitionDescription",
                arguments="fieldDefinitionArguments",
                directives="fieldDefinitionDirectives",
                location="fieldDefinitionLocation",
            ),
            FieldDefinitionNode(
                name="fieldDefinitionNameBis",
                type="fieldDefinitionType",
                description="fieldDefinitionDescription",
                arguments="fieldDefinitionArguments",
                directives="fieldDefinitionDirectives",
                location="fieldDefinitionLocation",
            ),
            False,
        ),
        (
            FieldDefinitionNode(
                name="fieldDefinitionName",
                type="fieldDefinitionType",
                description="fieldDefinitionDescription",
                arguments="fieldDefinitionArguments",
                directives="fieldDefinitionDirectives",
                location="fieldDefinitionLocation",
            ),
            FieldDefinitionNode(
                name="fieldDefinitionName",
                type="fieldDefinitionTypeBis",
                description="fieldDefinitionDescription",
                arguments="fieldDefinitionArguments",
                directives="fieldDefinitionDirectives",
                location="fieldDefinitionLocation",
            ),
            False,
        ),
        (
            FieldDefinitionNode(
                name="fieldDefinitionName",
                type="fieldDefinitionType",
                description="fieldDefinitionDescription",
                arguments="fieldDefinitionArguments",
                directives="fieldDefinitionDirectives",
                location="fieldDefinitionLocation",
            ),
            FieldDefinitionNode(
                name="fieldDefinitionName",
                type="fieldDefinitionType",
                description="fieldDefinitionDescriptionBis",
                arguments="fieldDefinitionArguments",
                directives="fieldDefinitionDirectives",
                location="fieldDefinitionLocation",
            ),
            False,
        ),
        (
            FieldDefinitionNode(
                name="fieldDefinitionName",
                type="fieldDefinitionType",
                description="fieldDefinitionDescription",
                arguments="fieldDefinitionArguments",
                directives="fieldDefinitionDirectives",
                location="fieldDefinitionLocation",
            ),
            FieldDefinitionNode(
                name="fieldDefinitionName",
                type="fieldDefinitionType",
                description="fieldDefinitionDescription",
                arguments="fieldDefinitionArgumentsBis",
                directives="fieldDefinitionDirectives",
                location="fieldDefinitionLocation",
            ),
            False,
        ),
        (
            FieldDefinitionNode(
                name="fieldDefinitionName",
                type="fieldDefinitionType",
                description="fieldDefinitionDescription",
                arguments="fieldDefinitionArguments",
                directives="fieldDefinitionDirectives",
                location="fieldDefinitionLocation",
            ),
            FieldDefinitionNode(
                name="fieldDefinitionName",
                type="fieldDefinitionType",
                description="fieldDefinitionDescription",
                arguments="fieldDefinitionArguments",
                directives="fieldDefinitionDirectivesBis",
                location="fieldDefinitionLocation",
            ),
            False,
        ),
        (
            FieldDefinitionNode(
                name="fieldDefinitionName",
                type="fieldDefinitionType",
                description="fieldDefinitionDescription",
                arguments="fieldDefinitionArguments",
                directives="fieldDefinitionDirectives",
                location="fieldDefinitionLocation",
            ),
            FieldDefinitionNode(
                name="fieldDefinitionName",
                type="fieldDefinitionType",
                description="fieldDefinitionDescription",
                arguments="fieldDefinitionArguments",
                directives="fieldDefinitionDirectives",
                location="fieldDefinitionLocationBis",
            ),
            False,
        ),
        (
            FieldDefinitionNode(
                name="fieldDefinitionName",
                type="fieldDefinitionType",
                description="fieldDefinitionDescription",
                arguments="fieldDefinitionArguments",
                directives="fieldDefinitionDirectives",
                location="fieldDefinitionLocation",
            ),
            FieldDefinitionNode(
                name="fieldDefinitionName",
                type="fieldDefinitionType",
                description="fieldDefinitionDescription",
                arguments="fieldDefinitionArguments",
                directives="fieldDefinitionDirectives",
                location="fieldDefinitionLocation",
            ),
            True,
        ),
    ],
)
def test_fielddefinitionnode__eq__(field_definition_node, other, expected):
    assert (field_definition_node == other) is expected


@pytest.mark.parametrize(
    "field_definition_node,expected",
    [
        (
            FieldDefinitionNode(
                name="fieldDefinitionName",
                type="fieldDefinitionType",
                description="fieldDefinitionDescription",
                arguments="fieldDefinitionArguments",
                directives="fieldDefinitionDirectives",
                location="fieldDefinitionLocation",
            ),
            "FieldDefinitionNode("
            "description='fieldDefinitionDescription', "
            "name='fieldDefinitionName', "
            "arguments='fieldDefinitionArguments', "
            "type='fieldDefinitionType', "
            "directives='fieldDefinitionDirectives', "
            "location='fieldDefinitionLocation')",
        )
    ],
)
def test_fielddefinitionnode__repr__(field_definition_node, expected):
    assert field_definition_node.__repr__() == expected
