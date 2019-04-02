import pytest

from tartiflette.language.ast import NameNode


def test_namenode__init__():
    name_node = NameNode(value="nameValue", location="nameLocation")
    assert name_node.value == "nameValue"
    assert name_node.location == "nameLocation"


@pytest.mark.parametrize(
    "name_node,other,expected",
    [
        (
            NameNode(value="nameValue", location="nameLocation"),
            Ellipsis,
            False,
        ),
        (
            NameNode(value="nameValue", location="nameLocation"),
            NameNode(value="nameValueBis", location="nameLocation"),
            False,
        ),
        (
            NameNode(value="nameValue", location="nameLocation"),
            NameNode(value="nameValue", location="nameLocationBis"),
            False,
        ),
        (
            NameNode(value="nameValue", location="nameLocation"),
            NameNode(value="nameValue", location="nameLocation"),
            True,
        ),
    ],
)
def test_namenode__eq__(name_node, other, expected):
    assert (name_node == other) is expected


@pytest.mark.parametrize(
    "name_node,expected",
    [
        (
            NameNode(value="nameValue", location="nameLocation"),
            "NameNode(value='nameValue', location='nameLocation')",
        )
    ],
)
def test_namenode__repr__(name_node, expected):
    assert name_node.__repr__() == expected
