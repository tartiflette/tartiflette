import pytest

from tartiflette.language.ast import InputObjectTypeExtension


def test_inputobjecttypeextensionnode__init__():
    input_object_type_extension_node = InputObjectTypeExtension(
        name="inputObjectTypeExtensionName",
        directives="inputObjectTypeExtensionDirectives",
        fields="inputObjectTypeExtensionFields",
        location="inputObjectTypeExtensionLocation",
    )
    assert (
        input_object_type_extension_node.name == "inputObjectTypeExtensionName"
    )
    assert (
        input_object_type_extension_node.directives
        == "inputObjectTypeExtensionDirectives"
    )
    assert (
        input_object_type_extension_node.fields
        == "inputObjectTypeExtensionFields"
    )
    assert (
        input_object_type_extension_node.location
        == "inputObjectTypeExtensionLocation"
    )


@pytest.mark.parametrize(
    "input_object_type_extension_node,other,expected",
    [
        (
            InputObjectTypeExtension(
                name="inputObjectTypeExtensionName",
                directives="inputObjectTypeExtensionDirectives",
                fields="inputObjectTypeExtensionFields",
                location="inputObjectTypeExtensionLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            InputObjectTypeExtension(
                name="inputObjectTypeExtensionName",
                directives="inputObjectTypeExtensionDirectives",
                fields="inputObjectTypeExtensionFields",
                location="inputObjectTypeExtensionLocation",
            ),
            InputObjectTypeExtension(
                name="inputObjectTypeExtensionNameBis",
                directives="inputObjectTypeExtensionDirectives",
                fields="inputObjectTypeExtensionFields",
                location="inputObjectTypeExtensionLocation",
            ),
            False,
        ),
        (
            InputObjectTypeExtension(
                name="inputObjectTypeExtensionName",
                directives="inputObjectTypeExtensionDirectives",
                fields="inputObjectTypeExtensionFields",
                location="inputObjectTypeExtensionLocation",
            ),
            InputObjectTypeExtension(
                name="inputObjectTypeExtensionName",
                directives="inputObjectTypeExtensionDirectivesBis",
                fields="inputObjectTypeExtensionFields",
                location="inputObjectTypeExtensionLocation",
            ),
            False,
        ),
        (
            InputObjectTypeExtension(
                name="inputObjectTypeExtensionName",
                directives="inputObjectTypeExtensionDirectives",
                fields="inputObjectTypeExtensionFields",
                location="inputObjectTypeExtensionLocation",
            ),
            InputObjectTypeExtension(
                name="inputObjectTypeExtensionName",
                directives="inputObjectTypeExtensionDirectives",
                fields="inputObjectTypeExtensionFieldsBis",
                location="inputObjectTypeExtensionLocation",
            ),
            False,
        ),
        (
            InputObjectTypeExtension(
                name="inputObjectTypeExtensionName",
                directives="inputObjectTypeExtensionDirectives",
                fields="inputObjectTypeExtensionFields",
                location="inputObjectTypeExtensionLocation",
            ),
            InputObjectTypeExtension(
                name="inputObjectTypeExtensionName",
                directives="inputObjectTypeExtensionDirectives",
                fields="inputObjectTypeExtensionFields",
                location="inputObjectTypeExtensionLocationBis",
            ),
            False,
        ),
        (
            InputObjectTypeExtension(
                name="inputObjectTypeExtensionName",
                directives="inputObjectTypeExtensionDirectives",
                fields="inputObjectTypeExtensionFields",
                location="inputObjectTypeExtensionLocation",
            ),
            InputObjectTypeExtension(
                name="inputObjectTypeExtensionName",
                directives="inputObjectTypeExtensionDirectives",
                fields="inputObjectTypeExtensionFields",
                location="inputObjectTypeExtensionLocation",
            ),
            True,
        ),
    ],
)
def test_inputobjecttypeextensionnode__eq__(
    input_object_type_extension_node, other, expected
):
    assert (input_object_type_extension_node == other) is expected


@pytest.mark.parametrize(
    "input_object_type_extension_node,expected",
    [
        (
            InputObjectTypeExtension(
                name="inputObjectTypeExtensionName",
                directives="inputObjectTypeExtensionDirectives",
                fields="inputObjectTypeExtensionFields",
                location="inputObjectTypeExtensionLocation",
            ),
            "InputObjectTypeExtension("
            "name='inputObjectTypeExtensionName', "
            "directives='inputObjectTypeExtensionDirectives', "
            "fields='inputObjectTypeExtensionFields', "
            "location='inputObjectTypeExtensionLocation')",
        )
    ],
)
def test_inputobjecttypeextensionnode__repr__(
    input_object_type_extension_node, expected
):
    assert input_object_type_extension_node.__repr__() == expected
