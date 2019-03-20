import pytest

from tartiflette.language.ast import ScalarTypeExtensionNode


def test_scalartypeextensionnode__init__():
    scalar_type_extension_node = ScalarTypeExtensionNode(
        name="scalarTypeExtensionName",
        directives="scalarTypeExtensionDirectives",
        location="scalarTypeExtensionLocation",
    )
    assert scalar_type_extension_node.name == "scalarTypeExtensionName"
    assert (
        scalar_type_extension_node.directives
        == "scalarTypeExtensionDirectives"
    )
    assert scalar_type_extension_node.location == "scalarTypeExtensionLocation"


@pytest.mark.parametrize(
    "scalar_type_extension_node,other,expected",
    [
        (
            ScalarTypeExtensionNode(
                name="scalarTypeExtensionName",
                directives="scalarTypeExtensionDirectives",
                location="scalarTypeExtensionLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            ScalarTypeExtensionNode(
                name="scalarTypeExtensionName",
                directives="scalarTypeExtensionDirectives",
                location="scalarTypeExtensionLocation",
            ),
            ScalarTypeExtensionNode(
                name="scalarTypeExtensionNameBis",
                directives="scalarTypeExtensionDirectives",
                location="scalarTypeExtensionLocation",
            ),
            False,
        ),
        (
            ScalarTypeExtensionNode(
                name="scalarTypeExtensionName",
                directives="scalarTypeExtensionDirectives",
                location="scalarTypeExtensionLocation",
            ),
            ScalarTypeExtensionNode(
                name="scalarTypeExtensionName",
                directives="scalarTypeExtensionDirectivesBis",
                location="scalarTypeExtensionLocation",
            ),
            False,
        ),
        (
            ScalarTypeExtensionNode(
                name="scalarTypeExtensionName",
                directives="scalarTypeExtensionDirectives",
                location="scalarTypeExtensionLocation",
            ),
            ScalarTypeExtensionNode(
                name="scalarTypeExtensionName",
                directives="scalarTypeExtensionDirectives",
                location="scalarTypeExtensionLocationBis",
            ),
            False,
        ),
        (
            ScalarTypeExtensionNode(
                name="scalarTypeExtensionName",
                directives="scalarTypeExtensionDirectives",
                location="scalarTypeExtensionLocation",
            ),
            ScalarTypeExtensionNode(
                name="scalarTypeExtensionName",
                directives="scalarTypeExtensionDirectives",
                location="scalarTypeExtensionLocation",
            ),
            True,
        ),
    ],
)
def test_scalartypeextensionnode__eq__(
    scalar_type_extension_node, other, expected
):
    assert (scalar_type_extension_node == other) is expected


@pytest.mark.parametrize(
    "scalar_type_extension_node,expected",
    [
        (
            ScalarTypeExtensionNode(
                name="scalarTypeExtensionName",
                directives="scalarTypeExtensionDirectives",
                location="scalarTypeExtensionLocation",
            ),
            "ScalarTypeExtensionNode("
            "name='scalarTypeExtensionName', "
            "directives='scalarTypeExtensionDirectives', "
            "location='scalarTypeExtensionLocation')",
        )
    ],
)
def test_scalartypeextensionnode__repr__(scalar_type_extension_node, expected):
    assert scalar_type_extension_node.__repr__() == expected
