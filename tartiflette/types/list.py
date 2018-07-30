from typing import Any, Optional, Union

from tartiflette.executors.types import CoercedValue, Info
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
    ):
        super().__init__(name=None, description=description)
        self.gql_type = gql_type

    def __repr__(self) -> str:
        return "{}(gql_type={!r}, description={!r})".format(
            self.__class__.__name__, self.gql_type, self.description
        )

    def __str__(self):
        return "[{!s}]".format(self.gql_type)

    def __eq__(self, other):
        return super().__eq__(other) and self.gql_type == other.gql_type

    def coerce_value(
        self, value: Any, info: Info
    ) -> CoercedValue:
        if value is None:
            return CoercedValue(value, None)
        try:
            results = []
            error = None
            for index, item in enumerate(value):
                tmp_path = info.path[:]
                tmp_path.append(index)
                tmp_info = Info(
                    info.query_field,
                    info.schema_field,
                    info.schema,
                    tmp_path,
                    info.location,
                )
                coerced_value = self.gql_type.coerce_value(
                    item, tmp_info
                )
                if coerced_value.error and coerced_value.error.is_null_error is True:
                    coerced_value.error.is_null_error = False
                    return CoercedValue(None, coerced_value.error)
                elif coerced_value.error and error is None:
                    # The GraphQL spec says 1 error per field: other errors
                    # are discarded. Should we stop the loop ?
                    error = coerced_value.error
                results.append(coerced_value.value)
            return CoercedValue(results, error)
        except TypeError:
            # GraphQLList accepts values of 1 element
            # see the GraphQL.js implementation
            pass
        coerced_value = self.gql_type.coerce_value(value, info)
        return CoercedValue([coerced_value.value], coerced_value.error)
