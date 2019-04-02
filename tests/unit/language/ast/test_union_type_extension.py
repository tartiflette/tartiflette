import pytest

from tartiflette.language.ast import UnionTypeExtensionNode


def test_uniontypeextensionnode__init__():
    union_type_extension_node = UnionTypeExtensionNode(
        name="unionTypeExtensionName",
        directives="unionTypeExtensionDirectives",
        types="unionTypeExtensionTypes",
        location="unionTypeExtensionLocation",
    )
    assert union_type_extension_node.name == "unionTypeExtensionName"
    assert (
        union_type_extension_node.directives == "unionTypeExtensionDirectives"
    )
    assert union_type_extension_node.types == "unionTypeExtensionTypes"
    assert union_type_extension_node.location == "unionTypeExtensionLocation"


@pytest.mark.parametrize(
    "union_type_extension_node,other,expected",
    [
        (
            UnionTypeExtensionNode(
                name="unionTypeExtensionName",
                directives="unionTypeExtensionDirectives",
                types="unionTypeExtensionTypes",
                location="unionTypeExtensionLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            UnionTypeExtensionNode(
                name="unionTypeExtensionName",
                directives="unionTypeExtensionDirectives",
                types="unionTypeExtensionTypes",
                location="unionTypeExtensionLocation",
            ),
            UnionTypeExtensionNode(
                name="unionTypeExtensionNameBis",
                directives="unionTypeExtensionDirectives",
                types="unionTypeExtensionTypes",
                location="unionTypeExtensionLocation",
            ),
            False,
        ),
        (
            UnionTypeExtensionNode(
                name="unionTypeExtensionName",
                directives="unionTypeExtensionDirectives",
                types="unionTypeExtensionTypes",
                location="unionTypeExtensionLocation",
            ),
            UnionTypeExtensionNode(
                name="unionTypeExtensionName",
                directives="unionTypeExtensionDirectivesBis",
                types="unionTypeExtensionTypes",
                location="unionTypeExtensionLocation",
            ),
            False,
        ),
        (
            UnionTypeExtensionNode(
                name="unionTypeExtensionName",
                directives="unionTypeExtensionDirectives",
                types="unionTypeExtensionTypes",
                location="unionTypeExtensionLocation",
            ),
            UnionTypeExtensionNode(
                name="unionTypeExtensionName",
                directives="unionTypeExtensionDirectives",
                types="unionTypeExtensionTypesBis",
                location="unionTypeExtensionLocation",
            ),
            False,
        ),
        (
            UnionTypeExtensionNode(
                name="unionTypeExtensionName",
                directives="unionTypeExtensionDirectives",
                types="unionTypeExtensionTypes",
                location="unionTypeExtensionLocation",
            ),
            UnionTypeExtensionNode(
                name="unionTypeExtensionName",
                directives="unionTypeExtensionDirectives",
                types="unionTypeExtensionTypes",
                location="unionTypeExtensionLocationBis",
            ),
            False,
        ),
        (
            UnionTypeExtensionNode(
                name="unionTypeExtensionName",
                directives="unionTypeExtensionDirectives",
                types="unionTypeExtensionTypes",
                location="unionTypeExtensionLocation",
            ),
            UnionTypeExtensionNode(
                name="unionTypeExtensionName",
                directives="unionTypeExtensionDirectives",
                types="unionTypeExtensionTypes",
                location="unionTypeExtensionLocation",
            ),
            True,
        ),
    ],
)
def test_uniontypeextensionnode__eq__(
    union_type_extension_node, other, expected
):
    assert (union_type_extension_node == other) is expected


@pytest.mark.parametrize(
    "union_type_extension_node,expected",
    [
        (
            UnionTypeExtensionNode(
                name="unionTypeExtensionName",
                directives="unionTypeExtensionDirectives",
                types="unionTypeExtensionTypes",
                location="unionTypeExtensionLocation",
            ),
            "UnionTypeExtensionNode("
            "name='unionTypeExtensionName', "
            "directives='unionTypeExtensionDirectives', "
            "types='unionTypeExtensionTypes', "
            "location='unionTypeExtensionLocation')",
        )
    ],
)
def test_uniontypeextensionnode__repr__(union_type_extension_node, expected):
    assert union_type_extension_node.__repr__() == expected
