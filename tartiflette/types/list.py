from typing import Optional, Union

from tartiflette.types.type import GraphQLType


class GraphQLList(GraphQLType):
    """
    List Container
    A GraphQLList is a container, wrapping type that points at another type.
    The type contained will be returned as a list instead of a single item.
    """

    def __init__(
        self,
        gql_type: Union[str, GraphQLType],
        description: Optional[str] = None,
        schema=None,
    ):
        super().__init__(
            name=None, description=description, is_list=True, schema=schema
        )
        self.gql_type = gql_type

    def __repr__(self) -> str:
        return "{}(gql_type={!r}, description={!r})".format(
            self.__class__.__name__, self.gql_type, self.description
        )

    def __str__(self):
        return "[{!s}]".format(self.gql_type)

    def __eq__(self, other):
        return super().__eq__(other) and self.gql_type == other.gql_type

    @property
    def contains_not_null(self) -> bool:
        try:
            return self.gql_type.contains_not_null
        except AttributeError:
            pass
        return False

    # Introspection Attribute
    @property
    def ofType(self):
        if isinstance(self.gql_type, GraphQLType):
            return self.gql_type

        return self.schema.find_type(self.gql_type)

    # Introspection Attribute
    @property
    def kind(self):
        return "LIST"
