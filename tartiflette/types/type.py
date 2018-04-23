from typing import Optional

from tartiflette.executors.types import ExecutionData


class GraphQLType:
    __slots__ = (
        'name',
        'description',
        # 'sdl_info',  # TODO: Is it useful to store the SDL source AST Node ?
    )

    def __init__(self,
                 name: Optional[str] = None,
                 description: Optional[str]=None):
        self.name = name
        self.description = description

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

    def collect_value(self, value, execution_data: ExecutionData):
        raise NotImplementedError(
            "{} must implement a `collect_value` function.".format(
                self.__class__.__name__
            )
        )
