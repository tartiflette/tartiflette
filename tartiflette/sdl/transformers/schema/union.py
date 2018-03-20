from typing import List, Union

from tartiflette.sdl.transformers.schema import GraphQLNamedTypeDefinition, \
    GraphQLNamedType, Name


class GraphQLUnionTypeDefinition(GraphQLNamedTypeDefinition):
    """
    Union Type Definition

    When a field can return one of a heterogeneous set of types, a Union
    type is used to describe what types are possible as well as providing
    a function to determine which type is actually used when the field
    if resolved.
    """

    # __slots__ = (
    #     'types',
    # )

    def __init__(
        self, name: Union[str, Name], types: List[GraphQLNamedType], **kwargs
    ):
        super(GraphQLUnionTypeDefinition, self).__init__(name=name, **kwargs)
        self.types = types

    def __repr__(self):
        base = super(GraphQLUnionTypeDefinition, self).__repr__()
        return base + "(types: {})".format(self.types)

    def __eq__(self, other):
        return super(GraphQLUnionTypeDefinition, self).__eq__(other) and \
            self.types == other.types
