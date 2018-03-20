from typing import Union, Iterable, Optional, List, Dict

from tartiflette.sdl.transformers.schema import GraphQLValue, \
    GraphQLBaseObject, GraphQLNamedTypeDefinition, \
    Name, GraphQLArgumentDefinition


class GraphQLDirective(GraphQLBaseObject):

    # name arguments?
    def __init__(
        self,
        name: Union[str, Name],
        arguments: Optional[Dict[str, GraphQLValue]] = None,
        **kwargs
    ):
        super(GraphQLDirective, self).__init__(**kwargs)
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        return '@{}(arguments: {})'.format(self.name, self.arguments)

    def __eq__(self, other):
        return isinstance(other, GraphQLDirective) and \
               self.name == other.name and \
               self.arguments == other.arguments


class GraphQLDirectiveDefinition(GraphQLNamedTypeDefinition):

    # __slots__ = (
    #     'location',
    #     'arguments',
    # )

    def __init__(
        self,
        name: Union[str, Name],
        locations: Iterable[str],
        arguments: Optional[List[GraphQLArgumentDefinition]] = None,
        **kwargs
    ):
        super(GraphQLDirectiveDefinition, self).__init__(name=name, **kwargs)
        self.locations = locations
        self.arguments = arguments

    def __repr__(self):
        base = super(GraphQLDirectiveDefinition, self).__repr__()
        return base + "(locations: {}, arguments: {})".format(
            self.locations, self.arguments
        )

    def __eq__(self, other):
        return super(GraphQLDirectiveDefinition, self).__eq__(other) and \
                self.locations == other.locations and \
                self.arguments == other.arguments
