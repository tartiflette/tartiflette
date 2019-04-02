import pytest

from tartiflette.language.ast import InputObjectTypeDefinitionNode


def test_inputobjecttypedefinitionnode__init__():
    input_object_type_definition_node = InputObjectTypeDefinitionNode(
        name="inputObjectTypeDefinitionName",
        description="inputObjectTypeDefinitionDescription",
        directives="inputObjectTypeDefinitionDirectives",
        fields="inputObjectTypeDefinitionFields",
        location="inputObjectTypeDefinitionLocation",
    )
    assert (
        input_object_type_definition_node.name
        == "inputObjectTypeDefinitionName"
    )
    assert (
        input_object_type_definition_node.description
        == "inputObjectTypeDefinitionDescription"
    )
    assert (
        input_object_type_definition_node.directives
        == "inputObjectTypeDefinitionDirectives"
    )
    assert (
        input_object_type_definition_node.fields
        == "inputObjectTypeDefinitionFields"
    )
    assert (
        input_object_type_definition_node.location
        == "inputObjectTypeDefinitionLocation"
    )


@pytest.mark.parametrize(
    "input_object_type_definition_node,other,expected",
    [
        (
            InputObjectTypeDefinitionNode(
                name="inputObjectTypeDefinitionName",
                description="inputObjectTypeDefinitionDescription",
                directives="inputObjectTypeDefinitionDirectives",
                fields="inputObjectTypeDefinitionFields",
                location="inputObjectTypeDefinitionLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            InputObjectTypeDefinitionNode(
                name="inputObjectTypeDefinitionName",
                description="inputObjectTypeDefinitionDescription",
                directives="inputObjectTypeDefinitionDirectives",
                fields="inputObjectTypeDefinitionFields",
                location="inputObjectTypeDefinitionLocation",
            ),
            InputObjectTypeDefinitionNode(
                name="inputObjectTypeDefinitionNameBis",
                description="inputObjectTypeDefinitionDescription",
                directives="inputObjectTypeDefinitionDirectives",
                fields="inputObjectTypeDefinitionFields",
                location="inputObjectTypeDefinitionLocation",
            ),
            False,
        ),
        (
            InputObjectTypeDefinitionNode(
                name="inputObjectTypeDefinitionName",
                description="inputObjectTypeDefinitionDescription",
                directives="inputObjectTypeDefinitionDirectives",
                fields="inputObjectTypeDefinitionFields",
                location="inputObjectTypeDefinitionLocation",
            ),
            InputObjectTypeDefinitionNode(
                name="inputObjectTypeDefinitionName",
                description="inputObjectTypeDefinitionDescriptionBis",
                directives="inputObjectTypeDefinitionDirectives",
                fields="inputObjectTypeDefinitionFields",
                location="inputObjectTypeDefinitionLocation",
            ),
            False,
        ),
        (
            InputObjectTypeDefinitionNode(
                name="inputObjectTypeDefinitionName",
                description="inputObjectTypeDefinitionDescription",
                directives="inputObjectTypeDefinitionDirectives",
                fields="inputObjectTypeDefinitionFields",
                location="inputObjectTypeDefinitionLocation",
            ),
            InputObjectTypeDefinitionNode(
                name="inputObjectTypeDefinitionName",
                description="inputObjectTypeDefinitionDescription",
                directives="inputObjectTypeDefinitionDirectivesBis",
                fields="inputObjectTypeDefinitionFields",
                location="inputObjectTypeDefinitionLocation",
            ),
            False,
        ),
        (
            InputObjectTypeDefinitionNode(
                name="inputObjectTypeDefinitionName",
                description="inputObjectTypeDefinitionDescription",
                directives="inputObjectTypeDefinitionDirectives",
                fields="inputObjectTypeDefinitionFields",
                location="inputObjectTypeDefinitionLocation",
            ),
            InputObjectTypeDefinitionNode(
                name="inputObjectTypeDefinitionName",
                description="inputObjectTypeDefinitionDescription",
                directives="inputObjectTypeDefinitionDirectives",
                fields="inputObjectTypeDefinitionFieldsBis",
                location="inputObjectTypeDefinitionLocation",
            ),
            False,
        ),
        (
            InputObjectTypeDefinitionNode(
                name="inputObjectTypeDefinitionName",
                description="inputObjectTypeDefinitionDescription",
                directives="inputObjectTypeDefinitionDirectives",
                fields="inputObjectTypeDefinitionFields",
                location="inputObjectTypeDefinitionLocation",
            ),
            InputObjectTypeDefinitionNode(
                name="inputObjectTypeDefinitionName",
                description="inputObjectTypeDefinitionDescription",
                directives="inputObjectTypeDefinitionDirectives",
                fields="inputObjectTypeDefinitionFields",
                location="inputObjectTypeDefinitionLocationBis",
            ),
            False,
        ),
        (
            InputObjectTypeDefinitionNode(
                name="inputObjectTypeDefinitionName",
                description="inputObjectTypeDefinitionDescription",
                directives="inputObjectTypeDefinitionDirectives",
                fields="inputObjectTypeDefinitionFields",
                location="inputObjectTypeDefinitionLocation",
            ),
            InputObjectTypeDefinitionNode(
                name="inputObjectTypeDefinitionName",
                description="inputObjectTypeDefinitionDescription",
                directives="inputObjectTypeDefinitionDirectives",
                fields="inputObjectTypeDefinitionFields",
                location="inputObjectTypeDefinitionLocation",
            ),
            True,
        ),
    ],
)
def test_inputobjecttypedefinitionnode__eq__(
    input_object_type_definition_node, other, expected
):
    assert (input_object_type_definition_node == other) is expected


@pytest.mark.parametrize(
    "input_object_type_definition_node,expected",
    [
        (
            InputObjectTypeDefinitionNode(
                name="inputObjectTypeDefinitionName",
                description="inputObjectTypeDefinitionDescription",
                directives="inputObjectTypeDefinitionDirectives",
                fields="inputObjectTypeDefinitionFields",
                location="inputObjectTypeDefinitionLocation",
            ),
            "InputObjectTypeDefinitionNode("
            "description='inputObjectTypeDefinitionDescription', "
            "name='inputObjectTypeDefinitionName', "
            "directives='inputObjectTypeDefinitionDirectives', "
            "fields='inputObjectTypeDefinitionFields', "
            "location='inputObjectTypeDefinitionLocation')",
        )
    ],
)
def test_inputobjecttypedefinitionnode__repr__(
    input_object_type_definition_node, expected
):
    assert input_object_type_definition_node.__repr__() == expected
