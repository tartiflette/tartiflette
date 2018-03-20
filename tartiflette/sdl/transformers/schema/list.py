from typing import Iterable
from tartiflette.sdl.transformers.schema import GraphQLType, GraphQLValue


class GraphQLListValue(GraphQLValue):
    def __init__(self, lst: Iterable, **kwargs):
        super(GraphQLListValue, self).__init__(value=lst, **kwargs)

    def to_python(self):
        return self.value


class GraphQLListType(GraphQLType):

    # __slots__ = (
    #     'gql_type',
    # )

    def __init__(self, gql_type: GraphQLType, **kwargs):
        super(GraphQLListType, self).__init__(**kwargs)
        self.gql_type = gql_type

    def __repr__(self):
        return "List(gql_type: {})".format(self.gql_type)

    def __eq__(self, other):
        return super(GraphQLListType, self).__eq__(other) and \
               self.gql_type == other.gql_type
