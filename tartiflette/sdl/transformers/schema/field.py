from collections import OrderedDict
from typing import Optional, Union, Dict

from tartiflette.sdl.transformers.schema import Name, GraphQLDefinition, \
    GraphQLArgumentDefinition


class GraphQLFieldDefinition(GraphQLDefinition):

    # __slots__ = (
    #     'name',
    #     'gql_type',
    #     'arguments',
    #     'resolver',
    # )

    def __init__(
        self,
        name: Union[str, Name],
        gql_type: Union[str, 'GraphQLOutputType'],
        arguments: Optional[Dict[str, GraphQLArgumentDefinition]] = None,
        resolver: Optional[callable] = None,
        **kwargs
    ):
        super(GraphQLFieldDefinition, self).__init__(**kwargs)
        self._name = None
        self.name = name
        self.gql_type = gql_type
        self.arguments = arguments if arguments else OrderedDict()
        self.resolver = resolver

    def __repr__(self):
        return "GraphQLFieldDefinition<{}>" \
               "(name: {}, arguments: {}, resolver: {}]>".format(
                self.gql_type, self.name, self.arguments, self.resolver)

    def __eq__(self, other):
        return super(GraphQLFieldDefinition, self).__eq__(other) and \
               self._name == other._name and \
               self.gql_type == other.gql_type and \
               self.arguments == other.arguments and \
               self.resolver == other.resolver

    @property
    def name(self):
        return self._name.name

    @name.setter
    def name(self, value: Union[str, Name]):
        if isinstance(value, str):
            value = Name(name=value)
        if value.name.startswith('__'):
            raise ValueError(
                'Cannot define a GraphQL field name '
                'starting with two underscores. '
                'They are reserved (see specs).'
            )
        self._name = value
