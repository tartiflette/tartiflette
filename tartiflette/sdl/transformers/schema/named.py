from typing import Union

from tartiflette.sdl.transformers.schema import Name, GraphQLDefinition, \
    GraphQLType


class GraphQLNamedType(GraphQLType):

    # __slots__ = (
    #     'name',
    # )

    def __init__(self, name: Union[str, Name], **kwargs):
        super(GraphQLNamedType, self).__init__(**kwargs)
        self._name = None
        self.name = name

    def __repr__(self):
        return '{}:{}'.format(self.__class__.__name__, self.name)

    def __eq__(self, other):
        return super(GraphQLNamedType, self).__eq__(other) and \
               self.name == other.name

    @property
    def name(self):
        return self._name.name

    @name.setter
    def name(self, value: Union[str, Name]):
        if isinstance(value, str):
            value = Name(name=value)
        if value.name.startswith('__'):
            raise ValueError(
                'Cannot define a GraphQL name '
                'starting with two underscores. '
                'They are reserved (see specs).'
            )
        self._name = value


class GraphQLNamedTypeDefinition(GraphQLNamedType, GraphQLDefinition):
    """
    `GraphQLNamedType`s have definitions
    """

    def __init__(self, name: Name, **kwargs):
        super(GraphQLNamedTypeDefinition, self).__init__(name=name, **kwargs)

    def __eq__(self, other):
        return super(GraphQLNamedType, self).__eq__(other)
