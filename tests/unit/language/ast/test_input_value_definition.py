import pytest

from tartiflette.language.ast import InputValueDefinitionNode


def test_inputvaluedefinitionnode__init__():
    input_value_definition_node = InputValueDefinitionNode(
        name="inputValueDefinitionName",
        type="inputValueDefinitionType",
        description="inputValueDefinitionDescription",
        default_value="inputValueDefinitionDefaultValue",
        directives="inputValueDefinitionDirectives",
        location="inputValueDefinitionLocation",
    )
    assert input_value_definition_node.name == "inputValueDefinitionName"
    assert input_value_definition_node.type == "inputValueDefinitionType"
    assert (
        input_value_definition_node.description
        == "inputValueDefinitionDescription"
    )
    assert (
        input_value_definition_node.default_value
        == "inputValueDefinitionDefaultValue"
    )
    assert (
        input_value_definition_node.directives
        == "inputValueDefinitionDirectives"
    )
    assert (
        input_value_definition_node.location == "inputValueDefinitionLocation"
    )


@pytest.mark.parametrize(
    "input_value_definition_node,other,expected",
    [
        (
            InputValueDefinitionNode(
                name="inputValueDefinitionName",
                type="inputValueDefinitionType",
                description="inputValueDefinitionDescription",
                default_value="inputValueDefinitionDefaultValue",
                directives="inputValueDefinitionDirectives",
                location="inputValueDefinitionLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            InputValueDefinitionNode(
                name="inputValueDefinitionName",
                type="inputValueDefinitionType",
                description="inputValueDefinitionDescription",
                default_value="inputValueDefinitionDefaultValue",
                directives="inputValueDefinitionDirectives",
                location="inputValueDefinitionLocation",
            ),
            InputValueDefinitionNode(
                name="inputValueDefinitionNameBis",
                type="inputValueDefinitionType",
                description="inputValueDefinitionDescription",
                default_value="inputValueDefinitionDefaultValue",
                directives="inputValueDefinitionDirectives",
                location="inputValueDefinitionLocation",
            ),
            False,
        ),
        (
            InputValueDefinitionNode(
                name="inputValueDefinitionName",
                type="inputValueDefinitionType",
                description="inputValueDefinitionDescription",
                default_value="inputValueDefinitionDefaultValue",
                directives="inputValueDefinitionDirectives",
                location="inputValueDefinitionLocation",
            ),
            InputValueDefinitionNode(
                name="inputValueDefinitionName",
                type="inputValueDefinitionTypeBis",
                description="inputValueDefinitionDescription",
                default_value="inputValueDefinitionDefaultValue",
                directives="inputValueDefinitionDirectives",
                location="inputValueDefinitionLocation",
            ),
            False,
        ),
        (
            InputValueDefinitionNode(
                name="inputValueDefinitionName",
                type="inputValueDefinitionType",
                description="inputValueDefinitionDescription",
                default_value="inputValueDefinitionDefaultValue",
                directives="inputValueDefinitionDirectives",
                location="inputValueDefinitionLocation",
            ),
            InputValueDefinitionNode(
                name="inputValueDefinitionName",
                type="inputValueDefinitionType",
                description="inputValueDefinitionDescriptionBis",
                default_value="inputValueDefinitionDefaultValue",
                directives="inputValueDefinitionDirectives",
                location="inputValueDefinitionLocation",
            ),
            False,
        ),
        (
            InputValueDefinitionNode(
                name="inputValueDefinitionName",
                type="inputValueDefinitionType",
                description="inputValueDefinitionDescription",
                default_value="inputValueDefinitionDefaultValue",
                directives="inputValueDefinitionDirectives",
                location="inputValueDefinitionLocation",
            ),
            InputValueDefinitionNode(
                name="inputValueDefinitionName",
                type="inputValueDefinitionType",
                description="inputValueDefinitionDescription",
                default_value="inputValueDefinitionDefaultValueBis",
                directives="inputValueDefinitionDirectives",
                location="inputValueDefinitionLocation",
            ),
            False,
        ),
        (
            InputValueDefinitionNode(
                name="inputValueDefinitionName",
                type="inputValueDefinitionType",
                description="inputValueDefinitionDescription",
                default_value="inputValueDefinitionDefaultValue",
                directives="inputValueDefinitionDirectives",
                location="inputValueDefinitionLocation",
            ),
            InputValueDefinitionNode(
                name="inputValueDefinitionName",
                type="inputValueDefinitionType",
                description="inputValueDefinitionDescription",
                default_value="inputValueDefinitionDefaultValue",
                directives="inputValueDefinitionDirectivesBis",
                location="inputValueDefinitionLocation",
            ),
            False,
        ),
        (
            InputValueDefinitionNode(
                name="inputValueDefinitionName",
                type="inputValueDefinitionType",
                description="inputValueDefinitionDescription",
                default_value="inputValueDefinitionDefaultValue",
                directives="inputValueDefinitionDirectives",
                location="inputValueDefinitionLocation",
            ),
            InputValueDefinitionNode(
                name="inputValueDefinitionName",
                type="inputValueDefinitionType",
                description="inputValueDefinitionDescription",
                default_value="inputValueDefinitionDefaultValue",
                directives="inputValueDefinitionDirectives",
                location="inputValueDefinitionLocationBis",
            ),
            False,
        ),
        (
            InputValueDefinitionNode(
                name="inputValueDefinitionName",
                type="inputValueDefinitionType",
                description="inputValueDefinitionDescription",
                default_value="inputValueDefinitionDefaultValue",
                directives="inputValueDefinitionDirectives",
                location="inputValueDefinitionLocation",
            ),
            InputValueDefinitionNode(
                name="inputValueDefinitionName",
                type="inputValueDefinitionType",
                description="inputValueDefinitionDescription",
                default_value="inputValueDefinitionDefaultValue",
                directives="inputValueDefinitionDirectives",
                location="inputValueDefinitionLocation",
            ),
            True,
        ),
    ],
)
def test_inputvaluedefinitionnode__eq__(
    input_value_definition_node, other, expected
):
    assert (input_value_definition_node == other) is expected


@pytest.mark.parametrize(
    "input_value_definition_node,expected",
    [
        (
            InputValueDefinitionNode(
                name="inputValueDefinitionName",
                type="inputValueDefinitionType",
                description="inputValueDefinitionDescription",
                default_value="inputValueDefinitionDefaultValue",
                directives="inputValueDefinitionDirectives",
                location="inputValueDefinitionLocation",
            ),
            "InputValueDefinitionNode("
            "description='inputValueDefinitionDescription', "
            "name='inputValueDefinitionName', "
            "type='inputValueDefinitionType', "
            "default_value='inputValueDefinitionDefaultValue', "
            "directives='inputValueDefinitionDirectives', "
            "location='inputValueDefinitionLocation')",
        )
    ],
)
def test_inputvaluedefinitionnode__repr__(
    input_value_definition_node, expected
):
    assert input_value_definition_node.__repr__() == expected
