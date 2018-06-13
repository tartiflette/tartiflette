from typing import Optional, Any

from tartiflette.executors.types import ExecutionData
from tartiflette.types.exceptions.tartiflette import InvalidValue
from tartiflette.types.type import GraphQLType


class GraphQLScalarType(GraphQLType):
    """
    Scalar Type Definition

    The leaf values of any request and input values to arguments are
    Scalars (or Enums which are special Scalars) and are defined with a name
    and a series of functions used to convert to and from the request or SDL.

    Example: see the default Int, String or Boolean scalars.
    """

    def __init__(self, name: str,
                 coerce_output: Optional[callable]=None,
                 coerce_input: Optional[callable]= None,
                 description: Optional[str] = None):
        super().__init__(name=name, description=description)
        self.coerce_output = coerce_output
        self.coerce_input = coerce_input

    def __repr__(self) -> str:
        return "{}(name={!r}, description={!r})".format(
            self.__class__.__name__, self.name, self.description,
        )

    def __eq__(self, other) -> bool:
        # TODO: Need to check if [de]serialize functions need to be equal
        return super().__eq__(other) and \
               self.coerce_output == other.coerce_output and \
               self.coerce_input == other.coerce_input

    def type_check(self, value: Any, execution_data: ExecutionData) -> Any:
        try:
            self.coerce_output(value)
            return value
        except TypeError:
            raise InvalidValue(value,
                               gql_type=execution_data.field.gql_type,
                               field=execution_data.field,
                               path=execution_data.path,
                               locations=[execution_data.location],
                               )

    def coerce_value(self, value: Any) -> Any:
        if value is None:
            return value
        return self.coerce_output(value)

    def collect_value(self, value, execution_data: ExecutionData):
        if value is None:
            return value
        return self.coerce_output(value)
