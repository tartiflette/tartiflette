import pytest

from tartiflette.language.ast import FragmentDefinitionNode


def test_fragmentdefinitionnode__init__():
    fragment_definition_node = FragmentDefinitionNode(
        name="fragmentDefinitionName",
        type_condition="fragmentDefinitionTypeCondition",
        selection_set="fragmentDefinitionSelectionSet",
        directives="fragmentDefinitionDirectives",
        location="fragmentDefinitionLocation",
    )
    assert fragment_definition_node.name == "fragmentDefinitionName"
    assert (
        fragment_definition_node.type_condition
        == "fragmentDefinitionTypeCondition"
    )
    assert (
        fragment_definition_node.selection_set
        == "fragmentDefinitionSelectionSet"
    )
    assert (
        fragment_definition_node.directives == "fragmentDefinitionDirectives"
    )
    assert fragment_definition_node.location == "fragmentDefinitionLocation"


@pytest.mark.parametrize(
    "fragment_definition_node,other,expected",
    [
        (
            FragmentDefinitionNode(
                name="fragmentDefinitionName",
                type_condition="fragmentDefinitionTypeCondition",
                selection_set="fragmentDefinitionSelectionSet",
                directives="fragmentDefinitionDirectives",
                location="fragmentDefinitionLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            FragmentDefinitionNode(
                name="fragmentDefinitionName",
                type_condition="fragmentDefinitionTypeCondition",
                selection_set="fragmentDefinitionSelectionSet",
                directives="fragmentDefinitionDirectives",
                location="fragmentDefinitionLocation",
            ),
            FragmentDefinitionNode(
                name="fragmentDefinitionNameBis",
                type_condition="fragmentDefinitionTypeCondition",
                selection_set="fragmentDefinitionSelectionSet",
                directives="fragmentDefinitionDirectives",
                location="fragmentDefinitionLocation",
            ),
            False,
        ),
        (
            FragmentDefinitionNode(
                name="fragmentDefinitionName",
                type_condition="fragmentDefinitionTypeCondition",
                selection_set="fragmentDefinitionSelectionSet",
                directives="fragmentDefinitionDirectives",
                location="fragmentDefinitionLocation",
            ),
            FragmentDefinitionNode(
                name="fragmentDefinitionName",
                type_condition="fragmentDefinitionTypeConditionBis",
                selection_set="fragmentDefinitionSelectionSet",
                directives="fragmentDefinitionDirectives",
                location="fragmentDefinitionLocation",
            ),
            False,
        ),
        (
            FragmentDefinitionNode(
                name="fragmentDefinitionName",
                type_condition="fragmentDefinitionTypeCondition",
                selection_set="fragmentDefinitionSelectionSet",
                directives="fragmentDefinitionDirectives",
                location="fragmentDefinitionLocation",
            ),
            FragmentDefinitionNode(
                name="fragmentDefinitionName",
                type_condition="fragmentDefinitionTypeCondition",
                selection_set="fragmentDefinitionSelectionSetBis",
                directives="fragmentDefinitionDirectives",
                location="fragmentDefinitionLocation",
            ),
            False,
        ),
        (
            FragmentDefinitionNode(
                name="fragmentDefinitionName",
                type_condition="fragmentDefinitionTypeCondition",
                selection_set="fragmentDefinitionSelectionSet",
                directives="fragmentDefinitionDirectives",
                location="fragmentDefinitionLocation",
            ),
            FragmentDefinitionNode(
                name="fragmentDefinitionName",
                type_condition="fragmentDefinitionTypeCondition",
                selection_set="fragmentDefinitionSelectionSet",
                directives="fragmentDefinitionDirectivesBis",
                location="fragmentDefinitionLocation",
            ),
            False,
        ),
        (
            FragmentDefinitionNode(
                name="fragmentDefinitionName",
                type_condition="fragmentDefinitionTypeCondition",
                selection_set="fragmentDefinitionSelectionSet",
                directives="fragmentDefinitionDirectives",
                location="fragmentDefinitionLocation",
            ),
            FragmentDefinitionNode(
                name="fragmentDefinitionName",
                type_condition="fragmentDefinitionTypeCondition",
                selection_set="fragmentDefinitionSelectionSet",
                directives="fragmentDefinitionDirectives",
                location="fragmentDefinitionLocationBis",
            ),
            False,
        ),
        (
            FragmentDefinitionNode(
                name="fragmentDefinitionName",
                type_condition="fragmentDefinitionTypeCondition",
                selection_set="fragmentDefinitionSelectionSet",
                directives="fragmentDefinitionDirectives",
                location="fragmentDefinitionLocation",
            ),
            FragmentDefinitionNode(
                name="fragmentDefinitionName",
                type_condition="fragmentDefinitionTypeCondition",
                selection_set="fragmentDefinitionSelectionSet",
                directives="fragmentDefinitionDirectives",
                location="fragmentDefinitionLocation",
            ),
            True,
        ),
    ],
)
def test_fragmentdefinitionnode__eq__(
    fragment_definition_node, other, expected
):
    assert (fragment_definition_node == other) is expected


@pytest.mark.parametrize(
    "fragment_definition_node,expected",
    [
        (
            FragmentDefinitionNode(
                name="fragmentDefinitionName",
                type_condition="fragmentDefinitionTypeCondition",
                selection_set="fragmentDefinitionSelectionSet",
                directives="fragmentDefinitionDirectives",
                location="fragmentDefinitionLocation",
            ),
            "FragmentDefinitionNode("
            "name='fragmentDefinitionName', "
            "type_condition='fragmentDefinitionTypeCondition', "
            "directives='fragmentDefinitionDirectives', "
            "selection_set='fragmentDefinitionSelectionSet', "
            "location='fragmentDefinitionLocation')",
        )
    ],
)
def test_fragmentdefinitionnode__repr__(fragment_definition_node, expected):
    assert fragment_definition_node.__repr__() == expected
