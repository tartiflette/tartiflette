from typing import Union

from tartiflette.types.type import GraphQLType


def get_graphql_type(
    schema: "GraphQLSchema", graphql_type: Union[str, "GraphQLType"]
) -> "GraphQLType":
    """
    Returns the GraphQL type instance which refer to `graphql_type`.
    :param schema: the GraphQLSchema instance to use
    :param graphql_type: the GraphQL type to find
    :type schema: GraphQLSchema
    :type graphql_type: GraphQLType
    :return: the GraphQL type instance which refer to `graphql_type`
    :rtype: GraphQLType
    """
    if isinstance(graphql_type, GraphQLType):
        return graphql_type
    return schema.find_type(graphql_type)
