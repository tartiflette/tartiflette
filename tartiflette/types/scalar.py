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

    def __init__(
        self,
        name: str,
        coerce_output: Optional[callable] = None,
        coerce_input: Optional[callable] = None,
        description: Optional[str] = None,
        schema=None,
    ):
        super().__init__(name=name, description=description, schema=schema)
        self.coerce_output = coerce_output
        self.coerce_input = coerce_input

    def __repr__(self) -> str:
        return "{}(name={!r}, description={!r})".format(
            self.__class__.__name__, self.name, self.description
        )

    def __eq__(self, other) -> bool:
        # TODO: Comparing function pointers is not ideal here...
        return (
            super().__eq__(other)
            and self.coerce_output == other.coerce_output
            and self.coerce_input == other.coerce_input
        )

    # Introspection Attribute
    @property
    def kind(self):
        return "SCALAR"
