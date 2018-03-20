import pytest

from tartiflette.sdl.transformers.helpers import reduce_gql_type
from tartiflette.sdl.transformers.schema import GraphQLListType, \
    GraphQLNamedType, Name, GraphQLNonNullType


@pytest.mark.parametrize("gql_type,expected", [
    (
        GraphQLNamedType(name=Name(name="MyObject")),
        GraphQLNamedType(name=Name(name="MyObject"))
    ),
    (
        GraphQLListType(gql_type=GraphQLNamedType(name=Name(name="MyObject"))),
        GraphQLNamedType(name=Name(name="MyObject"))
    ),
    (
        GraphQLNonNullType(
            gql_type=GraphQLNamedType(name=Name(name="MyObject"))
        ),
        GraphQLNamedType(name=Name(name="MyObject"))
    ),
    (
        GraphQLListType(
            gql_type=GraphQLNonNullType(
                gql_type=GraphQLNamedType(
                    name=Name(name="LeafType"))
            )
        ),
        GraphQLNamedType(name=Name(name="LeafType"))
    ),
    (
        GraphQLNonNullType(
            gql_type=GraphQLListType(
                gql_type=GraphQLNonNullType(
                    gql_type=GraphQLNamedType(
                        name=Name(name="LeafType"))
                )
            )
        ),
        GraphQLNamedType(name=Name(name="LeafType"))
    ),
])
def test_reduce_type(gql_type,expected):
    reduced_gql_type = reduce_gql_type(gql_type)
    assert reduced_gql_type == expected



