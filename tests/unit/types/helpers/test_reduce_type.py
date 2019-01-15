import pytest

from tartiflette.types.helpers import reduce_type
from tartiflette.types.list import GraphQLList
from tartiflette.types.non_null import GraphQLNonNull


@pytest.mark.parametrize(
    "gql_type,expected",
    [
        (GraphQLNonNull(gql_type="MyObject"), "MyObject"),
        (GraphQLList(gql_type="MyObject"), "MyObject"),
        (
            GraphQLList(gql_type=GraphQLNonNull(gql_type="MyObject")),
            "MyObject",
        ),
        (
            GraphQLNonNull(
                gql_type=GraphQLList(
                    gql_type=GraphQLNonNull(gql_type="LeafType")
                )
            ),
            "LeafType",
        ),
    ],
)
def test_reduce_type(gql_type, expected):
    reduced_gql_type = reduce_type(gql_type)
    assert reduced_gql_type == expected
