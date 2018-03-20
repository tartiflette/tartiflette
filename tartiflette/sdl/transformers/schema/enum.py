from typing import List, Union

from tartiflette.sdl.transformers.schema import Name, GraphQLDefinition, \
    GraphQLValue, GraphQLNamedTypeDefinition


class GraphQLEnumValue(GraphQLValue):
    def __init__(self, key: str, **kwargs):
        super(GraphQLEnumValue, self).__init__(value=key, **kwargs)

    def to_python(self):
        # TODO: How can we make the link between an ENUM definition and
        # the value here ?
        return self.value


class GraphQLEnumValueDefinition(GraphQLEnumValue, GraphQLDefinition):
    def __init__(self, key: str, **kwargs):
        super(GraphQLEnumValueDefinition, self).__init__(key=key, **kwargs)

    def __eq__(self, other):
        return super(GraphQLEnumValueDefinition, self).__eq__(other)


class GraphQLEnumTypeDefinition(GraphQLNamedTypeDefinition):
    """
    Enum Type Definition

    Some leaf values of requests and input values are Enums.
    GraphQL serializes Enum values as strings, however internally
    Enums can be represented by any kind of type, often integers.

    Note: If a value is not provided in a definition,
    the name of the enum value will be used as its internal value.
    """

    __slots__ = [
        'values',
    ]

    def __init__(
        self, name: Union[str, Name], values: List[GraphQLEnumValueDefinition],
        **kwargs
    ):
        super(GraphQLEnumTypeDefinition, self).__init__(name=name, **kwargs)
        self.values = values

    def __repr__(self):
        base = super(GraphQLEnumTypeDefinition, self).__repr__()
        return base + '(values: {})'.format(self.values)

    def __eq__(self, other):
        return super(GraphQLEnumTypeDefinition, self).__eq__(other) and \
               self.values == other.values
