from typing import Any, Union

from tartiflette.sdl.transformers.schema import GraphQLValue, GraphQLNamedTypeDefinition, Name


class GraphQLScalarValue(GraphQLValue):
    def __init__(self, value: Any, **kwargs):
        super(GraphQLScalarValue, self).__init__(value=value, **kwargs)

    def to_python(self):
        return self.value


class GraphQLScalarTypeDefinition(GraphQLNamedTypeDefinition):
    """
    Scalar Type Definition

    The leaf values of any request and input values to arguments are
    Scalars (or Enums) and are defined with a name and a series of
    functions used to parse input from the AST or variables to
    ensure validity.

    Example: see the default Int, String or Boolean scalars.
    """

    def __init__(self, name: Union[str, Name], **kwargs):
        super(GraphQLScalarTypeDefinition, self).__init__(name=name, **kwargs)

    def __eq__(self, other):
        return super(GraphQLScalarTypeDefinition, self).__eq__(other)
