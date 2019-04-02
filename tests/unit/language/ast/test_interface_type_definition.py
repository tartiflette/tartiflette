import pytest

from tartiflette.language.ast import InterfaceTypeDefinitionNode


def test_interfacetypedefinitionnode__init__():
    interface_type_definition_node = InterfaceTypeDefinitionNode(
        name="interfaceTypeDefinitionName",
        description="interfaceTypeDefinitionDescription",
        directives="interfaceTypeDefinitionDirectives",
        fields="interfaceTypeDefinitionFields",
        location="interfaceTypeDefinitionLocation",
    )
    assert interface_type_definition_node.name == "interfaceTypeDefinitionName"
    assert (
        interface_type_definition_node.description
        == "interfaceTypeDefinitionDescription"
    )
    assert (
        interface_type_definition_node.directives
        == "interfaceTypeDefinitionDirectives"
    )
    assert (
        interface_type_definition_node.fields
        == "interfaceTypeDefinitionFields"
    )
    assert (
        interface_type_definition_node.location
        == "interfaceTypeDefinitionLocation"
    )


@pytest.mark.parametrize(
    "interface_type_definition_node,other,expected",
    [
        (
            InterfaceTypeDefinitionNode(
                name="interfaceTypeDefinitionName",
                description="interfaceTypeDefinitionDescription",
                directives="interfaceTypeDefinitionDirectives",
                fields="interfaceTypeDefinitionFields",
                location="interfaceTypeDefinitionLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            InterfaceTypeDefinitionNode(
                name="interfaceTypeDefinitionName",
                description="interfaceTypeDefinitionDescription",
                directives="interfaceTypeDefinitionDirectives",
                fields="interfaceTypeDefinitionFields",
                location="interfaceTypeDefinitionLocation",
            ),
            InterfaceTypeDefinitionNode(
                name="interfaceTypeDefinitionNameBis",
                description="interfaceTypeDefinitionDescription",
                directives="interfaceTypeDefinitionDirectives",
                fields="interfaceTypeDefinitionFields",
                location="interfaceTypeDefinitionLocation",
            ),
            False,
        ),
        (
            InterfaceTypeDefinitionNode(
                name="interfaceTypeDefinitionName",
                description="interfaceTypeDefinitionDescription",
                directives="interfaceTypeDefinitionDirectives",
                fields="interfaceTypeDefinitionFields",
                location="interfaceTypeDefinitionLocation",
            ),
            InterfaceTypeDefinitionNode(
                name="interfaceTypeDefinitionName",
                description="interfaceTypeDefinitionDescriptionBis",
                directives="interfaceTypeDefinitionDirectives",
                fields="interfaceTypeDefinitionFields",
                location="interfaceTypeDefinitionLocation",
            ),
            False,
        ),
        (
            InterfaceTypeDefinitionNode(
                name="interfaceTypeDefinitionName",
                description="interfaceTypeDefinitionDescription",
                directives="interfaceTypeDefinitionDirectives",
                fields="interfaceTypeDefinitionFields",
                location="interfaceTypeDefinitionLocation",
            ),
            InterfaceTypeDefinitionNode(
                name="interfaceTypeDefinitionName",
                description="interfaceTypeDefinitionDescription",
                directives="interfaceTypeDefinitionDirectivesBis",
                fields="interfaceTypeDefinitionFields",
                location="interfaceTypeDefinitionLocation",
            ),
            False,
        ),
        (
            InterfaceTypeDefinitionNode(
                name="interfaceTypeDefinitionName",
                description="interfaceTypeDefinitionDescription",
                directives="interfaceTypeDefinitionDirectives",
                fields="interfaceTypeDefinitionFields",
                location="interfaceTypeDefinitionLocation",
            ),
            InterfaceTypeDefinitionNode(
                name="interfaceTypeDefinitionName",
                description="interfaceTypeDefinitionDescription",
                directives="interfaceTypeDefinitionDirectives",
                fields="interfaceTypeDefinitionFieldsBis",
                location="interfaceTypeDefinitionLocation",
            ),
            False,
        ),
        (
            InterfaceTypeDefinitionNode(
                name="interfaceTypeDefinitionName",
                description="interfaceTypeDefinitionDescription",
                directives="interfaceTypeDefinitionDirectives",
                fields="interfaceTypeDefinitionFields",
                location="interfaceTypeDefinitionLocation",
            ),
            InterfaceTypeDefinitionNode(
                name="interfaceTypeDefinitionName",
                description="interfaceTypeDefinitionDescription",
                directives="interfaceTypeDefinitionDirectives",
                fields="interfaceTypeDefinitionFields",
                location="interfaceTypeDefinitionLocationBis",
            ),
            False,
        ),
        (
            InterfaceTypeDefinitionNode(
                name="interfaceTypeDefinitionName",
                description="interfaceTypeDefinitionDescription",
                directives="interfaceTypeDefinitionDirectives",
                fields="interfaceTypeDefinitionFields",
                location="interfaceTypeDefinitionLocation",
            ),
            InterfaceTypeDefinitionNode(
                name="interfaceTypeDefinitionName",
                description="interfaceTypeDefinitionDescription",
                directives="interfaceTypeDefinitionDirectives",
                fields="interfaceTypeDefinitionFields",
                location="interfaceTypeDefinitionLocation",
            ),
            True,
        ),
    ],
)
def test_interfacetypedefinitionnode__eq__(
    interface_type_definition_node, other, expected
):
    assert (interface_type_definition_node == other) is expected


@pytest.mark.parametrize(
    "interface_type_definition_node,expected",
    [
        (
            InterfaceTypeDefinitionNode(
                name="interfaceTypeDefinitionName",
                description="interfaceTypeDefinitionDescription",
                directives="interfaceTypeDefinitionDirectives",
                fields="interfaceTypeDefinitionFields",
                location="interfaceTypeDefinitionLocation",
            ),
            "InterfaceTypeDefinitionNode("
            "description='interfaceTypeDefinitionDescription', "
            "name='interfaceTypeDefinitionName', "
            "directives='interfaceTypeDefinitionDirectives', "
            "fields='interfaceTypeDefinitionFields', "
            "location='interfaceTypeDefinitionLocation')",
        )
    ],
)
def test_interfacetypedefinitionnode__repr__(
    interface_type_definition_node, expected
):
    assert interface_type_definition_node.__repr__() == expected
