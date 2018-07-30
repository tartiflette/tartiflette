from typing import Any, Optional

from tartiflette.executors.types import CoercedValue, Info


class GraphQLType:
    def __init__(
            self, name: Optional[str] = None, description: Optional[str] = None
    ):
        self.name = name
        self.description = description
        # self.sdl_info  # TODO: Is it useful to store the SDL source AST Node ?

    def __repr__(self) -> str:
        return "{}(name={!r}, description={!r})".format(
            self.__class__.__name__, self.name, self.description
        )

    def __str__(self):
        return "{!s}".format(self.name)

    def __eq__(self, other) -> bool:
        return self is other or (
                type(self) is type(other) and self.name == other.name
        )

    def coerce_value(
            self, value: Any, info: Info
    ) -> CoercedValue:
        raise NotImplementedError(
            "The GraphQLType %s must implement "
            "a coerce_value(value) method." % self.__class__.__name__
        )
