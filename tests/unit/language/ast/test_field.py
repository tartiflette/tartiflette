import pytest

from tartiflette.language.ast import FieldNode


def test_fieldnode__init__():
    field_node = FieldNode(
        name="fieldName",
        alias="fieldAlias",
        arguments="fieldArguments",
        directives="fieldDirectives",
        selection_set="fieldSelectionSet",
        location="fieldLocation",
    )
    assert field_node.name == "fieldName"
    assert field_node.alias == "fieldAlias"
    assert field_node.arguments == "fieldArguments"
    assert field_node.directives == "fieldDirectives"
    assert field_node.selection_set == "fieldSelectionSet"
    assert field_node.location == "fieldLocation"


@pytest.mark.parametrize(
    "field_node,other,expected",
    [
        (
            FieldNode(
                name="fieldName",
                alias="fieldAlias",
                arguments="fieldArguments",
                directives="fieldDirectives",
                selection_set="fieldSelectionSet",
                location="fieldLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            FieldNode(
                name="fieldName",
                alias="fieldAlias",
                arguments="fieldArguments",
                directives="fieldDirectives",
                selection_set="fieldSelectionSet",
                location="fieldLocation",
            ),
            FieldNode(
                name="fieldNameBis",
                alias="fieldAlias",
                arguments="fieldArguments",
                directives="fieldDirectives",
                selection_set="fieldSelectionSet",
                location="fieldLocation",
            ),
            False,
        ),
        (
            FieldNode(
                name="fieldName",
                alias="fieldAlias",
                arguments="fieldArguments",
                directives="fieldDirectives",
                selection_set="fieldSelectionSet",
                location="fieldLocation",
            ),
            FieldNode(
                name="fieldName",
                alias="fieldAliasBis",
                arguments="fieldArguments",
                directives="fieldDirectives",
                selection_set="fieldSelectionSet",
                location="fieldLocation",
            ),
            False,
        ),
        (
            FieldNode(
                name="fieldName",
                alias="fieldAlias",
                arguments="fieldArguments",
                directives="fieldDirectives",
                selection_set="fieldSelectionSet",
                location="fieldLocation",
            ),
            FieldNode(
                name="fieldName",
                alias="fieldAlias",
                arguments="fieldArgumentsBis",
                directives="fieldDirectives",
                selection_set="fieldSelectionSet",
                location="fieldLocation",
            ),
            False,
        ),
        (
            FieldNode(
                name="fieldName",
                alias="fieldAlias",
                arguments="fieldArguments",
                directives="fieldDirectives",
                selection_set="fieldSelectionSet",
                location="fieldLocation",
            ),
            FieldNode(
                name="fieldName",
                alias="fieldAlias",
                arguments="fieldArguments",
                directives="fieldDirectivesBis",
                selection_set="fieldSelectionSet",
                location="fieldLocation",
            ),
            False,
        ),
        (
            FieldNode(
                name="fieldName",
                alias="fieldAlias",
                arguments="fieldArguments",
                directives="fieldDirectives",
                selection_set="fieldSelectionSet",
                location="fieldLocation",
            ),
            FieldNode(
                name="fieldName",
                alias="fieldAlias",
                arguments="fieldArguments",
                directives="fieldDirectives",
                selection_set="fieldSelectionSetBis",
                location="fieldLocation",
            ),
            False,
        ),
        (
            FieldNode(
                name="fieldName",
                alias="fieldAlias",
                arguments="fieldArguments",
                directives="fieldDirectives",
                selection_set="fieldSelectionSet",
                location="fieldLocation",
            ),
            FieldNode(
                name="fieldName",
                alias="fieldAlias",
                arguments="fieldArguments",
                directives="fieldDirectives",
                selection_set="fieldSelectionSet",
                location="fieldLocationBis",
            ),
            False,
        ),
        (
            FieldNode(
                name="fieldName",
                alias="fieldAlias",
                arguments="fieldArguments",
                directives="fieldDirectives",
                selection_set="fieldSelectionSet",
                location="fieldLocation",
            ),
            FieldNode(
                name="fieldName",
                alias="fieldAlias",
                arguments="fieldArguments",
                directives="fieldDirectives",
                selection_set="fieldSelectionSet",
                location="fieldLocation",
            ),
            True,
        ),
    ],
)
def test_fieldnode__eq__(field_node, other, expected):
    assert (field_node == other) is expected


@pytest.mark.parametrize(
    "field_node,expected",
    [
        (
            FieldNode(
                name="fieldName",
                alias="fieldAlias",
                arguments="fieldArguments",
                directives="fieldDirectives",
                selection_set="fieldSelectionSet",
                location="fieldLocation",
            ),
            "FieldNode(alias='fieldAlias', name='fieldName', "
            "arguments='fieldArguments', directives='fieldDirectives', "
            "selection_set='fieldSelectionSet', "
            "location='fieldLocation')",
        )
    ],
)
def test_fieldnode__repr__(field_node, expected):
    assert field_node.__repr__() == expected
