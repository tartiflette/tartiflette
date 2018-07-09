from typing import Optional, Union, Any

from tartiflette.executors.types import ExecutionData, CoercedValue
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
        self, value: Any, execution_data: ExecutionData
    ) -> CoercedValue:
        if value is None:
            return CoercedValue(value, None)
        try:
            results = []
            errors = []
            for index, item in enumerate(value):
                tmp_path = execution_data.path[:]
                tmp_path.append(index)
                tmp_execution_data = ExecutionData(
                    execution_data.parent_result,
                    tmp_path,
                    execution_data.arguments,
                    execution_data.name,
                    execution_data.field,
                    execution_data.location,
                    execution_data.schema,
                )
                coerced_value = self.gql_type.coerce_value(
                    item, tmp_execution_data
                )
                if not coerced_value.errors:
                    results.append(coerced_value.value)
                if coerced_value.errors:
                    errors += coerced_value.errors
            return CoercedValue(results, errors)
        except TypeError:
            # GraphQLList accepts values of 1 element
            # see the GraphQL.js implementation
            pass
        coerced_value = self.gql_type.coerce_value(value, execution_data)
        if coerced_value.errors:
            return coerced_value
        return CoercedValue([coerced_value.value], None)
