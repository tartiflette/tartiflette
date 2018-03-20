from typing import Any, Optional

from tartiflette.sdl.transformers.schema import GraphQLBaseObject, \
    GraphQLType


class GraphQLValue(GraphQLBaseObject):

    # __slots__ = (
    #     'value',
    # )

    def __init__(
        self, value: Any, gql_type: Optional[GraphQLType] = None, **kwargs
    ):
        super(GraphQLValue, self).__init__(**kwargs)
        self.gql_type = gql_type
        self.value = value

    def __eq__(self, other):
        return type(other) is type(self) and \
               self.gql_type == other.gql_type and \
               self.value == other.value

    def __repr__(self):
        return '{}:{}({})'.format(
            self.__class__.__name__, self.gql_type, self.value
        )

    def to_python(self):
        if hasattr(self.value, "to_python"):
            return self.value.to_python()
        return self.value
