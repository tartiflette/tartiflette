from tartiflette.sdl.transformers.schema import GraphQLType, GraphQLListType, \
    GraphQLNonNullType, GraphQLNamedType


def reduce_gql_type(gql_type: GraphQLType) -> GraphQLNamedType:
    if isinstance(gql_type, (GraphQLListType, GraphQLNonNullType)):
        return reduce_gql_type(gql_type.gql_type)
    elif isinstance(gql_type, GraphQLNamedType):
        return gql_type
    else:
        raise ValueError(
            "Expected GraphQLType, "
            "got `{}`".format(gql_type.__class__.__name__)
        )
