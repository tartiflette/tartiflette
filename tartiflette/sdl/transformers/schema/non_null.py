from tartiflette.sdl.transformers.schema import GraphQLType


class GraphQLNonNullType(GraphQLType):

    # __slots__ = (
    #     'gql_type',
    # )

    def __init__(self, gql_type: GraphQLType, **kwargs):
        super(GraphQLNonNullType, self).__init__(**kwargs)
        self.gql_type = gql_type

    def __repr__(self):
        return "NonNull(gql_type: {})".format(self.gql_type)

    def __eq__(self, other):
        return super(GraphQLNonNullType, self).__eq__(other) and \
               self.gql_type == other.gql_type
