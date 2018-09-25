from typing import List, Optional

from tartiflette.types.type import GraphQLType


class GraphQLUnionType(GraphQLType):
    """
    Union Type Definition

    When a field can return one of a heterogeneous set of types, a Union
    type is used to describe what types are possible as well as providing
    a function to determine which type is actually used when the field
    if resolved.
    """

    def __init__(
        self,
        name: str,
        gql_types: List[GraphQLType],
        description: Optional[str] = None,
        schema=None,
    ):
        super().__init__(name=name, description=description, schema=schema)
        self.gql_types = gql_types

    def __repr__(self) -> str:
        return "{}(name={!r}, gql_types={!r}, description={!r})".format(
            self.__class__.__name__,
            self.name,
            self.gql_types,
            self.description,
        )

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.gql_types == other.gql_types

    # Introspection Attribute
    @property
    def kind(self):
        return "UNION"
