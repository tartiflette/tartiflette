from tartiflette.types.exceptions.tartiflette import GraphQLError


def to_graphql_error(exception):
    if isinstance(exception, GraphQLError):
        return exception
    return GraphQLError(str(exception))
