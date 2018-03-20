from typing import Optional, Union

from tartiflette.sdl.transformers.schema import Name, GraphQLType, \
    GraphQLDefinition, GraphQLValue


class GraphQLArgumentDefinition(GraphQLDefinition):
    # __slots__ = (
    #     'name',
    #     'gql_type',
    #     'default_value',
    # )

    def __init__(
        self,
        name: Union[str, Name],
        gql_type: GraphQLType,
        default_value: Optional[GraphQLValue] = None,
        **kwargs
    ):
        super(GraphQLArgumentDefinition, self).__init__(**kwargs)
        self._name = None
        self.name = name
        self.gql_type = gql_type
        self.default_value = default_value

    def __repr__(self):
        return "{}:{}({}={})".format(
            self.__class__.__name__, self.name, self.gql_type,
            self.default_value
        )

    def __eq__(self, other):
        return super(GraphQLArgumentDefinition, self).__eq__(other) and \
                self._name == other._name and \
                self.gql_type == other.gql_type and \
                self.default_value == other.default_value

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
