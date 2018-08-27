from typing import Any, List, Optional

from tartiflette.executors.types import Info
from tartiflette.types.exceptions.tartiflette import InvalidValue
from tartiflette.types.type import GraphQLType


class GraphQLEnumValue:
    """
    Enums are special leaf values.
    `GraphQLEnumValue`s is a way to represent them.
    """

    def __init__(self, value: Any = None, description: Optional[str] = None):
        self.value = value
        self.description = description

    def __repr__(self):
        return "{}(value={!r}, description={!r})".format(
            self.__class__.__name__, self.value, self.description
        )

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self is other or (
            type(self) is type(other) and self.value == other.value
        )


class GraphQLEnumType(GraphQLType):
    """
    Enum Type Definition

    Some leaf values of requests and input values are Enums.
    GraphQL serializes Enum values as strings, however internally
    Enums can be represented by any kind of type, often integers.

    Note: If a value is not provided in a definition,
    the name of the enum value will be used as its internal value.
    """

    def __init__(
        self,
        name: str,
        values: List[GraphQLEnumValue],
        description: Optional[str] = None,
    ):
        super().__init__(name=name, description=description)
        self.values = values
        # TODO: This will probably need a serialization / deserialization logic
        # and more

    def __repr__(self):
        return "{}(name={!r}, values={!r}, description={!r})".format(
            self.__class__.__name__, self.name, self.values, self.description
        )

    def __eq__(self, other):
        return super().__eq__(other) and self.values == other.values

    def coerce_value(self, value: Any, info: Info,) -> Any:
        if value is None:
            return value
        for enumval in self.values:
            if enumval.value == value:
                return enumval.value
        raise InvalidValue(value, info)
