from typing import Optional, Any

from tartiflette.executors.types import ExecutionData


class GraphQLType:

    def __init__(self,
                 name: Optional[str] = None,
                 description: Optional[str]=None):
        self.name = name
        self.description = description
        # self.sdl_info  # TODO: Is it useful to store the SDL source AST Node ?

    def __repr__(self) -> str:
        return "{}(name={!r}, description={!r})".format(
            self.__class__.__name__, self.name, self.description
        )

    def __str__(self):
        return '{!s}'.format(self.name)

    def __eq__(self, other) -> bool:
        return self is other or (
                type(self) is type(other) and self.name == other.name
        )

    def type_check(self, value: Any, execution_data: ExecutionData) -> Any:
        raise NotImplementedError("The GraphQLType %s must implement "
                                  "a type_check(value) method." %
                                  self.__class__.__name__)

    def coerce_value(self, value: Any) -> Any:
        raise NotImplementedError("The GraphQLType %s must implement "
                                  "a coerce_value(value) method." %
                                  self.__class__.__name__)

    def collect_value(self, value, execution_data: ExecutionData):
        if value is None:
            return None
        return {}
