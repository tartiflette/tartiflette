from typing import Optional

from tartiflette.types.type import GraphQLType


class GraphQLScalarType(GraphQLType):
    """
    Scalar Type Definition

    The leaf values of any request and input values to arguments are
    Scalars (or Enums which are special Scalars) and are defined with a name
    and a series of functions used to convert to and from the request or SDL.

    Example: see the default Int, String or Boolean scalars.
    """

    __slots__ = (
        'name',
        'description',
        'serializer',
        'deserializer',
    )

    def __init__(self, name: str,
                 serializer: Optional[callable]=None,
                 deserializer: Optional[callable]= None,
                 description: Optional[str] = None):
        super().__init__(name=name, description=description)
        self.serializer = serializer
        self.deserializer = deserializer

    def __repr__(self) -> str:
        return "{}(name={!r}, description={!r})".format(
            self.__class__.__name__, self.name, self.description,
        )

    def __eq__(self, other) -> bool:
        # TODO: Need to check if [de]serialize functions need to be equal
        return super().__eq__(other) and self.serializer == other.serializer \
               and self.deserializer == other.deserializer

    def to_value(self, value):
        if value is None:
            return value
        return self.serializer(value)
