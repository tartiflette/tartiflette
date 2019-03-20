import pytest

from tartiflette.language.ast import ObjectTypeExtensionNode


def test_objecttypeextensionnode__init__():
    object_type_extension_node = ObjectTypeExtensionNode(
        name="objectTypeExtensionName",
        interfaces="objectTypeExtensionInterfaces",
        directives="objectTypeExtensionDirectives",
        fields="objectTypeExtensionFields",
        location="objectTypeExtensionLocation",
    )
    assert object_type_extension_node.name == "objectTypeExtensionName"
    assert (
        object_type_extension_node.interfaces
        == "objectTypeExtensionInterfaces"
    )
    assert (
        object_type_extension_node.directives
        == "objectTypeExtensionDirectives"
    )
    assert object_type_extension_node.fields == "objectTypeExtensionFields"
    assert object_type_extension_node.location == "objectTypeExtensionLocation"


@pytest.mark.parametrize(
    "object_type_extension_node,other,expected",
    [
        (
            ObjectTypeExtensionNode(
                name="objectTypeExtensionName",
                interfaces="objectTypeExtensionInterfaces",
                directives="objectTypeExtensionDirectives",
                fields="objectTypeExtensionFields",
                location="objectTypeExtensionLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            ObjectTypeExtensionNode(
                name="objectTypeExtensionName",
                interfaces="objectTypeExtensionInterfaces",
                directives="objectTypeExtensionDirectives",
                fields="objectTypeExtensionFields",
                location="objectTypeExtensionLocation",
            ),
            ObjectTypeExtensionNode(
                name="objectTypeExtensionNameBis",
                interfaces="objectTypeExtensionInterfaces",
                directives="objectTypeExtensionDirectives",
                fields="objectTypeExtensionFields",
                location="objectTypeExtensionLocation",
            ),
            False,
        ),
        (
            ObjectTypeExtensionNode(
                name="objectTypeExtensionName",
                interfaces="objectTypeExtensionInterfaces",
                directives="objectTypeExtensionDirectives",
                fields="objectTypeExtensionFields",
                location="objectTypeExtensionLocation",
            ),
            ObjectTypeExtensionNode(
                name="objectTypeExtensionName",
                interfaces="objectTypeExtensionInterfacesBis",
                directives="objectTypeExtensionDirectives",
                fields="objectTypeExtensionFields",
                location="objectTypeExtensionLocation",
            ),
            False,
        ),
        (
            ObjectTypeExtensionNode(
                name="objectTypeExtensionName",
                interfaces="objectTypeExtensionInterfaces",
                directives="objectTypeExtensionDirectives",
                fields="objectTypeExtensionFields",
                location="objectTypeExtensionLocation",
            ),
            ObjectTypeExtensionNode(
                name="objectTypeExtensionName",
                interfaces="objectTypeExtensionInterfaces",
                directives="objectTypeExtensionDirectivesBis",
                fields="objectTypeExtensionFields",
                location="objectTypeExtensionLocation",
            ),
            False,
        ),
        (
            ObjectTypeExtensionNode(
                name="objectTypeExtensionName",
                interfaces="objectTypeExtensionInterfaces",
                directives="objectTypeExtensionDirectives",
                fields="objectTypeExtensionFields",
                location="objectTypeExtensionLocation",
            ),
            ObjectTypeExtensionNode(
                name="objectTypeExtensionName",
                interfaces="objectTypeExtensionInterfaces",
                directives="objectTypeExtensionDirectives",
                fields="objectTypeExtensionFieldsBis",
                location="objectTypeExtensionLocation",
            ),
            False,
        ),
        (
            ObjectTypeExtensionNode(
                name="objectTypeExtensionName",
                interfaces="objectTypeExtensionInterfaces",
                directives="objectTypeExtensionDirectives",
                fields="objectTypeExtensionFields",
                location="objectTypeExtensionLocation",
            ),
            ObjectTypeExtensionNode(
                name="objectTypeExtensionName",
                interfaces="objectTypeExtensionInterfaces",
                directives="objectTypeExtensionDirectives",
                fields="objectTypeExtensionFields",
                location="objectTypeExtensionLocationBis",
            ),
            False,
        ),
        (
            ObjectTypeExtensionNode(
                name="objectTypeExtensionName",
                interfaces="objectTypeExtensionInterfaces",
                directives="objectTypeExtensionDirectives",
                fields="objectTypeExtensionFields",
                location="objectTypeExtensionLocation",
            ),
            ObjectTypeExtensionNode(
                name="objectTypeExtensionName",
                interfaces="objectTypeExtensionInterfaces",
                directives="objectTypeExtensionDirectives",
                fields="objectTypeExtensionFields",
                location="objectTypeExtensionLocation",
            ),
            True,
        ),
    ],
)
def test_objecttypeextensionnode__eq__(
    object_type_extension_node, other, expected
):
    assert (object_type_extension_node == other) is expected


@pytest.mark.parametrize(
    "object_type_extension_node,expected",
    [
        (
            ObjectTypeExtensionNode(
                name="objectTypeExtensionName",
                interfaces="objectTypeExtensionInterfaces",
                directives="objectTypeExtensionDirectives",
                fields="objectTypeExtensionFields",
                location="objectTypeExtensionLocation",
            ),
            "ObjectTypeExtensionNode("
            "name='objectTypeExtensionName', "
            "interfaces='objectTypeExtensionInterfaces', "
            "directives='objectTypeExtensionDirectives', "
            "fields='objectTypeExtensionFields', "
            "location='objectTypeExtensionLocation')",
        )
    ],
)
def test_objecttypeextensionnode__repr__(object_type_extension_node, expected):
    assert object_type_extension_node.__repr__() == expected
