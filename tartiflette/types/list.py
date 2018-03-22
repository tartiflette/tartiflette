from typing import Optional

from tartiflette.types.type import GraphQLType


class GraphQLList(GraphQLType):
    """
    List Container
    A GraphQLList is a container, wrapping type that points at another type.
    The type contained will be returned as a list instead of a single item.
    """
    __slots__ = (
        'name',
        'description',
        'gql_type',
    )

    def __init__(self, gql_type: str, description: Optional[str] = None):
        super().__init__(name=None, description=description)
        self.gql_type = gql_type

    def __repr__(self) -> str:
        return "{}(gql_type={!r}, description={!r})".format(
            self.__class__.__name__, self.gql_type, self.description,
        )

    def __eq__(self, other):
        return super().__eq__(other) and \
               self.gql_type == other.gql_type

