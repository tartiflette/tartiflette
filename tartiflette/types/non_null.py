from typing import Any, Optional, Union

from tartiflette.executors.types import CoercedValue, Info
from tartiflette.types.exceptions.tartiflette import InvalidValue
from tartiflette.types.type import GraphQLType


class GraphQLNonNull(GraphQLType):
    """
    Nom-Null Container
    A GraphQLNonNull is a container, wrapping type that points at another type.
    The type contained cannot return a null/None value at execution time.
    """

    def __init__(
        self,
        gql_type: Union[str, GraphQLType],
        description: Optional[str] = None,
    ):
        super().__init__(name=None, description=description)
        self.gql_type = gql_type

    def __repr__(self) -> str:
        return "{}(gql_type={!r}, description={!r})".format(
            self.__class__.__name__, self.gql_type, self.description
        )

    def __str__(self):
        return "{!s}!".format(self.gql_type)

    def __eq__(self, other):
        return super().__eq__(other) and self.gql_type == other.gql_type

    def coerce_value(
        self, value: Any, info: Info
    ) -> CoercedValue:
        if value is None:
            return CoercedValue(None, InvalidValue(value, info, is_null_error=True))
        val = self.gql_type.coerce_value(value, info)
        if val.value is None:
            return CoercedValue(None, InvalidValue(value, info, is_null_error=True))
        return val
