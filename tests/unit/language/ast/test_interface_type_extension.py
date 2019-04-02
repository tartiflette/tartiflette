import pytest

from tartiflette.language.ast import InterfaceTypeExtensionNode


def test_interfacetypeextensionnode__init__():
    interface_type_extension_node = InterfaceTypeExtensionNode(
        name="interfaceTypeExtensionName",
        directives="interfaceTypeExtensionDirectives",
        fields="interfaceTypeExtensionFields",
        location="interfaceTypeExtensionLocation",
    )
    assert interface_type_extension_node.name == "interfaceTypeExtensionName"
    assert (
        interface_type_extension_node.directives
        == "interfaceTypeExtensionDirectives"
    )
    assert (
        interface_type_extension_node.fields == "interfaceTypeExtensionFields"
    )
    assert (
        interface_type_extension_node.location
        == "interfaceTypeExtensionLocation"
    )


@pytest.mark.parametrize(
    "interface_type_extension_node,other,expected",
    [
        (
            InterfaceTypeExtensionNode(
                name="interfaceTypeExtensionName",
                directives="interfaceTypeExtensionDirectives",
                fields="interfaceTypeExtensionFields",
                location="interfaceTypeExtensionLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            InterfaceTypeExtensionNode(
                name="interfaceTypeExtensionName",
                directives="interfaceTypeExtensionDirectives",
                fields="interfaceTypeExtensionFields",
                location="interfaceTypeExtensionLocation",
            ),
            InterfaceTypeExtensionNode(
                name="interfaceTypeExtensionNameBis",
                directives="interfaceTypeExtensionDirectives",
                fields="interfaceTypeExtensionFields",
                location="interfaceTypeExtensionLocation",
            ),
            False,
        ),
        (
            InterfaceTypeExtensionNode(
                name="interfaceTypeExtensionName",
                directives="interfaceTypeExtensionDirectives",
                fields="interfaceTypeExtensionFields",
                location="interfaceTypeExtensionLocation",
            ),
            InterfaceTypeExtensionNode(
                name="interfaceTypeExtensionName",
                directives="interfaceTypeExtensionDirectivesBis",
                fields="interfaceTypeExtensionFields",
                location="interfaceTypeExtensionLocation",
            ),
            False,
        ),
        (
            InterfaceTypeExtensionNode(
                name="interfaceTypeExtensionName",
                directives="interfaceTypeExtensionDirectives",
                fields="interfaceTypeExtensionFields",
                location="interfaceTypeExtensionLocation",
            ),
            InterfaceTypeExtensionNode(
                name="interfaceTypeExtensionName",
                directives="interfaceTypeExtensionDirectives",
                fields="interfaceTypeExtensionFieldsBis",
                location="interfaceTypeExtensionLocation",
            ),
            False,
        ),
        (
            InterfaceTypeExtensionNode(
                name="interfaceTypeExtensionName",
                directives="interfaceTypeExtensionDirectives",
                fields="interfaceTypeExtensionFields",
                location="interfaceTypeExtensionLocation",
            ),
            InterfaceTypeExtensionNode(
                name="interfaceTypeExtensionName",
                directives="interfaceTypeExtensionDirectives",
                fields="interfaceTypeExtensionFields",
                location="interfaceTypeExtensionLocationBis",
            ),
            False,
        ),
        (
            InterfaceTypeExtensionNode(
                name="interfaceTypeExtensionName",
                directives="interfaceTypeExtensionDirectives",
                fields="interfaceTypeExtensionFields",
                location="interfaceTypeExtensionLocation",
            ),
            InterfaceTypeExtensionNode(
                name="interfaceTypeExtensionName",
                directives="interfaceTypeExtensionDirectives",
                fields="interfaceTypeExtensionFields",
                location="interfaceTypeExtensionLocation",
            ),
            True,
        ),
    ],
)
def test_interfacetypeextensionnode__eq__(
    interface_type_extension_node, other, expected
):
    assert (interface_type_extension_node == other) is expected


@pytest.mark.parametrize(
    "interface_type_extension_node,expected",
    [
        (
            InterfaceTypeExtensionNode(
                name="interfaceTypeExtensionName",
                directives="interfaceTypeExtensionDirectives",
                fields="interfaceTypeExtensionFields",
                location="interfaceTypeExtensionLocation",
            ),
            "InterfaceTypeExtensionNode("
            "name='interfaceTypeExtensionName', "
            "directives='interfaceTypeExtensionDirectives', "
            "fields='interfaceTypeExtensionFields', "
            "location='interfaceTypeExtensionLocation')",
        )
    ],
)
def test_interfacetypeextensionnode__repr__(
    interface_type_extension_node, expected
):
    assert interface_type_extension_node.__repr__() == expected
