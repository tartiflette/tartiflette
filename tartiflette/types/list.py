from typing import Optional, Union

from tartiflette.executors.types import ExecutionData
from tartiflette.types.exceptions.tartiflette import InvalidValue
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

    def collect_value(self, value, execution_data: ExecutionData):
        if value is None:
            return None
        if not isinstance(value, list):
            raise InvalidValue(value,
                               gql_type=execution_data.field.gql_type,
                               field=execution_data.field,
                               path=execution_data.path,
                               locations=[execution_data.location])
        results = []
        for index, item in enumerate(value):
            tmp_path = execution_data.path[:]
            tmp_path.append(index)
            tmp_execution_data = ExecutionData(execution_data.parent_result,
                                               tmp_path,
                                               execution_data.arguments,
                                               execution_data.name,
                                               execution_data.field,
                                               execution_data.location)
            try:
                results.append(self.gql_type.collect_value(item, tmp_execution_data))
            except InvalidValue as e:
                results.append(e)
        return results
