from typing import Union

from tartiflette.types.list import GraphQLList
from tartiflette.types.non_null import GraphQLNonNull

__all__ = ("reduce_type",)


def reduce_type(
    gql_type: Union[str, "GraphQLList", "GraphQLNonNull"]
) -> Union[str, "GraphQLType"]:
    """
    Unwraps the GraphQL type and to return the inner type.
    :param gql_type: schema type to unwrap
    :type gql_type: Union[str, GraphQLList, GraphQLNonNull]
    :return: the unwrapped inner schema type
    :rtype: Union[str, GraphQLType]
    """
    while isinstance(gql_type, (GraphQLList, GraphQLNonNull)):
        gql_type = gql_type.gql_type
    return gql_type
