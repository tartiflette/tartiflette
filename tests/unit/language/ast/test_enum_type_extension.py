import pytest

from tartiflette.language.ast import EnumTypeExtensionNode


def test_enumtypeextensionnode__init__():
    enum_type_extension_node = EnumTypeExtensionNode(
        name="enumTypeExtensionName",
        directives="enumTypeExtensionDirectives",
        values="enumTypeExtensionValues",
        location="enumTypeExtensionLocation",
    )
    assert enum_type_extension_node.name == "enumTypeExtensionName"
    assert enum_type_extension_node.directives == "enumTypeExtensionDirectives"
    assert enum_type_extension_node.values == "enumTypeExtensionValues"
    assert enum_type_extension_node.location == "enumTypeExtensionLocation"


@pytest.mark.parametrize(
    "enum_type_extension_node,other,expected",
    [
        (
            EnumTypeExtensionNode(
                name="enumTypeExtensionName",
                directives="enumTypeExtensionDirectives",
                values="enumTypeExtensionValues",
                location="enumTypeExtensionLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            EnumTypeExtensionNode(
                name="enumTypeExtensionName",
                directives="enumTypeExtensionDirectives",
                values="enumTypeExtensionValues",
                location="enumTypeExtensionLocation",
            ),
            EnumTypeExtensionNode(
                name="enumTypeExtensionNameBis",
                directives="enumTypeExtensionDirectives",
                values="enumTypeExtensionValues",
                location="enumTypeExtensionLocation",
            ),
            False,
        ),
        (
            EnumTypeExtensionNode(
                name="enumTypeExtensionName",
                directives="enumTypeExtensionDirectives",
                values="enumTypeExtensionValues",
                location="enumTypeExtensionLocation",
            ),
            EnumTypeExtensionNode(
                name="enumTypeExtensionName",
                directives="enumTypeExtensionDirectivesBis",
                values="enumTypeExtensionValues",
                location="enumTypeExtensionLocation",
            ),
            False,
        ),
        (
            EnumTypeExtensionNode(
                name="enumTypeExtensionName",
                directives="enumTypeExtensionDirectives",
                values="enumTypeExtensionValues",
                location="enumTypeExtensionLocation",
            ),
            EnumTypeExtensionNode(
                name="enumTypeExtensionName",
                directives="enumTypeExtensionDirectives",
                values="enumTypeExtensionValuesBis",
                location="enumTypeExtensionLocation",
            ),
            False,
        ),
        (
            EnumTypeExtensionNode(
                name="enumTypeExtensionName",
                directives="enumTypeExtensionDirectives",
                values="enumTypeExtensionValues",
                location="enumTypeExtensionLocation",
            ),
            EnumTypeExtensionNode(
                name="enumTypeExtensionName",
                directives="enumTypeExtensionDirectives",
                values="enumTypeExtensionValues",
                location="enumTypeExtensionLocationBis",
            ),
            False,
        ),
        (
            EnumTypeExtensionNode(
                name="enumTypeExtensionName",
                directives="enumTypeExtensionDirectives",
                values="enumTypeExtensionValues",
                location="enumTypeExtensionLocation",
            ),
            EnumTypeExtensionNode(
                name="enumTypeExtensionName",
                directives="enumTypeExtensionDirectives",
                values="enumTypeExtensionValues",
                location="enumTypeExtensionLocation",
            ),
            True,
        ),
    ],
)
def test_enumtypeextensionnode__eq__(
    enum_type_extension_node, other, expected
):
    assert (enum_type_extension_node == other) is expected


@pytest.mark.parametrize(
    "enum_type_extension_node,expected",
    [
        (
            EnumTypeExtensionNode(
                name="enumTypeExtensionName",
                directives="enumTypeExtensionDirectives",
                values="enumTypeExtensionValues",
                location="enumTypeExtensionLocation",
            ),
            "EnumTypeExtensionNode("
            "name='enumTypeExtensionName', "
            "directives='enumTypeExtensionDirectives', "
            "values='enumTypeExtensionValues', "
            "location='enumTypeExtensionLocation')",
        )
    ],
)
def test_enumtypeextensionnode__repr__(enum_type_extension_node, expected):
    assert enum_type_extension_node.__repr__() == expected
