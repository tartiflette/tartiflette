from typing import Union

from tartiflette.types.list import GraphQLList
from tartiflette.types.non_null import GraphQLNonNull


def reduce_type(
    gql_type: Union[str, GraphQLList, GraphQLNonNull]
) -> Union[str, "GraphQLType"]:
    while isinstance(gql_type, (GraphQLList, GraphQLNonNull)):
        gql_type = gql_type.gql_type
    return gql_type
