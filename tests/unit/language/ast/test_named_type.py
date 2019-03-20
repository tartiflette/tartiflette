import pytest

from tartiflette.language.ast import NamedTypeNode


def test_namedtypenode__init__():
    named_type_node = NamedTypeNode(
        name="namedTypeName", location="namedTypeLocation"
    )
    assert named_type_node.name == "namedTypeName"
    assert named_type_node.location == "namedTypeLocation"


@pytest.mark.parametrize(
    "named_type_node,other,expected",
    [
        (
            NamedTypeNode(name="namedTypeName", location="namedTypeLocation"),
            Ellipsis,
            False,
        ),
        (
            NamedTypeNode(name="namedTypeName", location="namedTypeLocation"),
            NamedTypeNode(
                name="namedTypeNameBis", location="namedTypeLocation"
            ),
            False,
        ),
        (
            NamedTypeNode(name="namedTypeName", location="namedTypeLocation"),
            NamedTypeNode(
                name="namedTypeName", location="namedTypeLocationBis"
            ),
            False,
        ),
        (
            NamedTypeNode(name="namedTypeName", location="namedTypeLocation"),
            NamedTypeNode(name="namedTypeName", location="namedTypeLocation"),
            True,
        ),
    ],
)
def test_namedtypenode__eq__(named_type_node, other, expected):
    assert (named_type_node == other) is expected


@pytest.mark.parametrize(
    "named_type_node,expected",
    [
        (
            NamedTypeNode(name="namedTypeName", location="namedTypeLocation"),
            "NamedTypeNode(name='namedTypeName', "
            "location='namedTypeLocation')",
        )
    ],
)
def test_namedtypenode__repr__(named_type_node, expected):
    assert named_type_node.__repr__() == expected
