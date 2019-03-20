import pytest

from tartiflette.language.ast import ObjectTypeDefinitionNode


def test_objecttypedefinitionnode__init__():
    object_type_definition_node = ObjectTypeDefinitionNode(
        name="objectTypeDefinitionName",
        description="objectTypeDefinitionDescription",
        interfaces="objectTypeDefinitionInterfaces",
        directives="objectTypeDefinitionDirectives",
        fields="objectTypeDefinitionFields",
        location="objectTypeDefinitionLocation",
    )
    assert object_type_definition_node.name == "objectTypeDefinitionName"
    assert (
        object_type_definition_node.description
        == "objectTypeDefinitionDescription"
    )
    assert (
        object_type_definition_node.interfaces
        == "objectTypeDefinitionInterfaces"
    )
    assert (
        object_type_definition_node.directives
        == "objectTypeDefinitionDirectives"
    )
    assert object_type_definition_node.fields == "objectTypeDefinitionFields"
    assert (
        object_type_definition_node.location == "objectTypeDefinitionLocation"
    )


@pytest.mark.parametrize(
    "object_type_definition_node,other,expected",
    [
        (
            ObjectTypeDefinitionNode(
                name="objectTypeDefinitionName",
                description="objectTypeDefinitionDescription",
                interfaces="objectTypeDefinitionInterfaces",
                directives="objectTypeDefinitionDirectives",
                fields="objectTypeDefinitionFields",
                location="objectTypeDefinitionLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            ObjectTypeDefinitionNode(
                name="objectTypeDefinitionName",
                description="objectTypeDefinitionDescription",
                interfaces="objectTypeDefinitionInterfaces",
                directives="objectTypeDefinitionDirectives",
                fields="objectTypeDefinitionFields",
                location="objectTypeDefinitionLocation",
            ),
            ObjectTypeDefinitionNode(
                name="objectTypeDefinitionNameBis",
                description="objectTypeDefinitionDescription",
                interfaces="objectTypeDefinitionInterfaces",
                directives="objectTypeDefinitionDirectives",
                fields="objectTypeDefinitionFields",
                location="objectTypeDefinitionLocation",
            ),
            False,
        ),
        (
            ObjectTypeDefinitionNode(
                name="objectTypeDefinitionName",
                description="objectTypeDefinitionDescription",
                interfaces="objectTypeDefinitionInterfaces",
                directives="objectTypeDefinitionDirectives",
                fields="objectTypeDefinitionFields",
                location="objectTypeDefinitionLocation",
            ),
            ObjectTypeDefinitionNode(
                name="objectTypeDefinitionName",
                description="objectTypeDefinitionDescriptionBis",
                interfaces="objectTypeDefinitionInterfaces",
                directives="objectTypeDefinitionDirectives",
                fields="objectTypeDefinitionFields",
                location="objectTypeDefinitionLocation",
            ),
            False,
        ),
        (
            ObjectTypeDefinitionNode(
                name="objectTypeDefinitionName",
                description="objectTypeDefinitionDescription",
                interfaces="objectTypeDefinitionInterfaces",
                directives="objectTypeDefinitionDirectives",
                fields="objectTypeDefinitionFields",
                location="objectTypeDefinitionLocation",
            ),
            ObjectTypeDefinitionNode(
                name="objectTypeDefinitionName",
                description="objectTypeDefinitionDescription",
                interfaces="objectTypeDefinitionInterfacesBis",
                directives="objectTypeDefinitionDirectives",
                fields="objectTypeDefinitionFields",
                location="objectTypeDefinitionLocation",
            ),
            False,
        ),
        (
            ObjectTypeDefinitionNode(
                name="objectTypeDefinitionName",
                description="objectTypeDefinitionDescription",
                interfaces="objectTypeDefinitionInterfaces",
                directives="objectTypeDefinitionDirectives",
                fields="objectTypeDefinitionFields",
                location="objectTypeDefinitionLocation",
            ),
            ObjectTypeDefinitionNode(
                name="objectTypeDefinitionName",
                description="objectTypeDefinitionDescription",
                interfaces="objectTypeDefinitionInterfaces",
                directives="objectTypeDefinitionDirectivesBis",
                fields="objectTypeDefinitionFields",
                location="objectTypeDefinitionLocation",
            ),
            False,
        ),
        (
            ObjectTypeDefinitionNode(
                name="objectTypeDefinitionName",
                description="objectTypeDefinitionDescription",
                interfaces="objectTypeDefinitionInterfaces",
                directives="objectTypeDefinitionDirectives",
                fields="objectTypeDefinitionFields",
                location="objectTypeDefinitionLocation",
            ),
            ObjectTypeDefinitionNode(
                name="objectTypeDefinitionName",
                description="objectTypeDefinitionDescription",
                interfaces="objectTypeDefinitionInterfaces",
                directives="objectTypeDefinitionDirectives",
                fields="objectTypeDefinitionFieldsBis",
                location="objectTypeDefinitionLocation",
            ),
            False,
        ),
        (
            ObjectTypeDefinitionNode(
                name="objectTypeDefinitionName",
                description="objectTypeDefinitionDescription",
                interfaces="objectTypeDefinitionInterfaces",
                directives="objectTypeDefinitionDirectives",
                fields="objectTypeDefinitionFields",
                location="objectTypeDefinitionLocation",
            ),
            ObjectTypeDefinitionNode(
                name="objectTypeDefinitionName",
                description="objectTypeDefinitionDescription",
                interfaces="objectTypeDefinitionInterfaces",
                directives="objectTypeDefinitionDirectives",
                fields="objectTypeDefinitionFields",
                location="objectTypeDefinitionLocationBis",
            ),
            False,
        ),
        (
            ObjectTypeDefinitionNode(
                name="objectTypeDefinitionName",
                description="objectTypeDefinitionDescription",
                interfaces="objectTypeDefinitionInterfaces",
                directives="objectTypeDefinitionDirectives",
                fields="objectTypeDefinitionFields",
                location="objectTypeDefinitionLocation",
            ),
            ObjectTypeDefinitionNode(
                name="objectTypeDefinitionName",
                description="objectTypeDefinitionDescription",
                interfaces="objectTypeDefinitionInterfaces",
                directives="objectTypeDefinitionDirectives",
                fields="objectTypeDefinitionFields",
                location="objectTypeDefinitionLocation",
            ),
            True,
        ),
    ],
)
def test_objecttypedefinitionnode__eq__(
    object_type_definition_node, other, expected
):
    assert (object_type_definition_node == other) is expected


@pytest.mark.parametrize(
    "object_type_definition_node,expected",
    [
        (
            ObjectTypeDefinitionNode(
                name="objectTypeDefinitionName",
                description="objectTypeDefinitionDescription",
                interfaces="objectTypeDefinitionInterfaces",
                directives="objectTypeDefinitionDirectives",
                fields="objectTypeDefinitionFields",
                location="objectTypeDefinitionLocation",
            ),
            "ObjectTypeDefinitionNode("
            "description='objectTypeDefinitionDescription', "
            "name='objectTypeDefinitionName', "
            "interfaces='objectTypeDefinitionInterfaces', "
            "directives='objectTypeDefinitionDirectives', "
            "fields='objectTypeDefinitionFields', "
            "location='objectTypeDefinitionLocation')",
        )
    ],
)
def test_objecttypedefinitionnode__repr__(
    object_type_definition_node, expected
):
    assert object_type_definition_node.__repr__() == expected
