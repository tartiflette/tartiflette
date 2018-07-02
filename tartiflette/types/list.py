from typing import Optional, Union, Any, List

from tartiflette.executors.types import ExecutionData
from tartiflette.types.exceptions.tartiflette import InvalidValue
from tartiflette.types.type import GraphQLType


class GraphQLList(GraphQLType):
    """
    List Container
    A GraphQLList is a container, wrapping type that points at another type.
    The type contained will be returned as a list instead of a single item.
    """

    def __init__(self, gql_type: Union[str, GraphQLType],
                 description: Optional[str] = None):
        super().__init__(name=None, description=description)
        self.gql_type = gql_type

    def __repr__(self) -> str:
        return "{}(gql_type={!r}, description={!r})".format(
            self.__class__.__name__, self.gql_type, self.description,
        )

    def __str__(self):
        return '[{!s}]'.format(self.gql_type)

    def __eq__(self, other):
        return super().__eq__(other) and \
               self.gql_type == other.gql_type

    def coerce_value(self, value: Any, execution_data: ExecutionData) -> (Any, List):
        if value is None:
            return None, []
        if not isinstance(value, list):
            return None, [InvalidValue(value,
                               gql_type=execution_data.field.gql_type,
                               field=execution_data.field,
                               path=execution_data.path,
                               locations=[execution_data.location])]
        results = []
        errors = []
        for index, item in enumerate(value):
            tmp_path = execution_data.path[:]
            tmp_path.append(index)
            tmp_execution_data = ExecutionData(execution_data.parent_result,
                                               tmp_path,
                                               execution_data.arguments,
                                               execution_data.name,
                                               execution_data.field,
                                               execution_data.location,
                                               execution_data.schema)
            result, error = self.gql_type.coerce_value(item, tmp_execution_data)
            results.append(result)
            if error:
                errors += error
        return results, errors
