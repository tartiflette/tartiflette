from typing import List, Optional, Any

from tartiflette.types.type import GraphQLType


class GraphQLEnumValue:
    """
    Enums are special leaf values.
    `GraphQLEnumValue`s is a way to represent them.
    """
    __slots__ = (
        'name',
        'description',
        'value',
    )

    def __init__(self, value: Any = None, name: Optional[str]=None, description: Optional[str]=None):
        self.value = value
        self.name = str(name)
        self.description = description

    def __repr__(self):
        return "{}(value={}, name={}, description={})".format(
            self.__class__.__name__,
            self.value, self.name, self.description
        )

    def __eq__(self, other):
        # TODO: We do not compare descriptions. Should we ?
        return self is other or (
            type(self) is type(other) and
            self.value == other.value and
            self.name == other.name
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

    __slots__ = (
        'name',
        'description',
        'values',
    )

    def __init__(
        self, name: str,
            values: List[GraphQLEnumValue],
            description: Optional[str]=None):
        super().__init__(name=name, description=description)
        self.values = values
        # TODO: This will probably need a serialization / deserialization logic
        # and more

    def __repr__(self):
        return "{}(name={}, values={}, description={})".format(
            self.__class__.__name__, self.name, self.values, self.description
        )

    def __eq__(self, other):
        return super().__eq__(other) and \
               self.values == other.values
