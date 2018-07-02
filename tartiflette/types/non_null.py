from typing import Optional, Union, Any, List

from tartiflette.executors.types import ExecutionData
from tartiflette.types.exceptions.tartiflette import \
    InvalidValue
from tartiflette.types.type import GraphQLType


class GraphQLNonNull(GraphQLType):
    """
    Nom-Null Container
    A GraphQLNonNull is a container, wrapping type that points at another type.
    The type contained cannot return a null/None value at execution time.
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
        return '{!s}!'.format(self.gql_type)

    def __eq__(self, other):
        return super().__eq__(other) and \
               self.gql_type == other.gql_type

    def coerce_value(self, value: Any, execution_data: ExecutionData) -> (Any, List):
        if value is None:
            return None, [InvalidValue(value,
                gql_type=execution_data.field.gql_type,
                field=execution_data.field,
                path=execution_data.path,
                locations=[execution_data.location])]
        return self.gql_type.coerce_value(value, execution_data)
