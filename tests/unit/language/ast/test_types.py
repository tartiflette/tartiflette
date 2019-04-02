import pytest

from tartiflette.language.ast import ListTypeNode, NonNullTypeNode


def test_listtypenode__init__():
    list_type_node = ListTypeNode(
        type="listTypeType", location="listTypeLocation"
    )
    assert list_type_node.type == "listTypeType"
    assert list_type_node.location == "listTypeLocation"


@pytest.mark.parametrize(
    "list_type_node,other,expected",
    [
        (
            ListTypeNode(type="listTypeType", location="listTypeLocation"),
            Ellipsis,
            False,
        ),
        (
            ListTypeNode(type="listTypeType", location="listTypeLocation"),
            ListTypeNode(type="listTypeTypeBis", location="listTypeLocation"),
            False,
        ),
        (
            ListTypeNode(type="listTypeType", location="listTypeLocation"),
            ListTypeNode(type="listTypeType", location="listTypeLocationBis"),
            False,
        ),
        (
            ListTypeNode(type="listTypeType", location="listTypeLocation"),
            ListTypeNode(type="listTypeType", location="listTypeLocation"),
            True,
        ),
    ],
)
def test_listtypenode__eq__(list_type_node, other, expected):
    assert (list_type_node == other) is expected


@pytest.mark.parametrize(
    "list_type_node,expected",
    [
        (
            ListTypeNode(type="listTypeType", location="listTypeLocation"),
            "ListTypeNode("
            "type='listTypeType', "
            "location='listTypeLocation')",
        )
    ],
)
def test_listtypenode__repr__(list_type_node, expected):
    assert list_type_node.__repr__() == expected


def test_nonnulltypenode__init__():
    non_null_type_node = NonNullTypeNode(
        type="nonNullTypeType", location="nonNullTypeLocation"
    )
    assert non_null_type_node.type == "nonNullTypeType"
    assert non_null_type_node.location == "nonNullTypeLocation"


@pytest.mark.parametrize(
    "non_null_type_node,other,expected",
    [
        (
            NonNullTypeNode(
                type="nonNullTypeType", location="nonNullTypeLocation"
            ),
            Ellipsis,
            False,
        ),
        (
            NonNullTypeNode(
                type="nonNullTypeType", location="nonNullTypeLocation"
            ),
            NonNullTypeNode(
                type="nonNullTypeTypeBis", location="nonNullTypeLocation"
            ),
            False,
        ),
        (
            NonNullTypeNode(
                type="nonNullTypeType", location="nonNullTypeLocation"
            ),
            NonNullTypeNode(
                type="nonNullTypeType", location="nonNullTypeLocationBis"
            ),
            False,
        ),
        (
            NonNullTypeNode(
                type="nonNullTypeType", location="nonNullTypeLocation"
            ),
            NonNullTypeNode(
                type="nonNullTypeType", location="nonNullTypeLocation"
            ),
            True,
        ),
    ],
)
def test_nonnulltypenode__eq__(non_null_type_node, other, expected):
    assert (non_null_type_node == other) is expected


@pytest.mark.parametrize(
    "non_null_type_node,expected",
    [
        (
            NonNullTypeNode(
                type="nonNullTypeType", location="nonNullTypeLocation"
            ),
            "NonNullTypeNode("
            "type='nonNullTypeType', "
            "location='nonNullTypeLocation')",
        )
    ],
)
def test_nonnulltypenode__repr__(non_null_type_node, expected):
    assert non_null_type_node.__repr__() == expected
