from typing import Any, List, Optional

from tartiflette.executors.types import Info
from tartiflette.types.exceptions.tartiflette import InvalidValue
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
    ):
        super().__init__(name=name, description=description)
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

    def coerce_value(
            self, value: Any, info: Info
    ) -> Any:
        # TODO: This is not OK: see the associated test and comments
        # on the error case. If one of the `gql_type` is a GraphQLObject,
        # it will never fail or check anything :/
        if value is None:
            return value
        for gql_type in self.gql_types:
            try:
                return gql_type.coerce_value(value, info)
            except Exception:
                continue
        raise InvalidValue(value, info)
