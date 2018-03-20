from typing import List, Optional, Dict, Iterable, Union

from tartiflette.sdl.transformers.schema import Name, GraphQLValue, GraphQLNamedTypeDefinition, \
    GraphQLFieldDefinition, GraphQLNamedType


class GraphQLObjectFieldValue(GraphQLValue):
    def __init__(self, key: Name, value: GraphQLValue, **kwargs):
        super(GraphQLObjectFieldValue, self).__init__(
            value=(key, value), **kwargs
        )

    def to_python(self):
        return self.value


class GraphQLObjectValue(GraphQLValue):
    def __init__(self, children: Iterable[GraphQLObjectFieldValue], **kwargs):
        super(GraphQLObjectValue, self).__init__(value=children, **kwargs)

    def to_python(self):
        tmp = {}
        for field in self.value:
            key, value = field.value
            tmp.update({key.name, value})
        return tmp


class GraphQLObjectTypeDefinition(GraphQLNamedTypeDefinition):
    """
    Object Type Definition

    Almost all of the GraphQL types you define will be object types.
    Object types have a name, but most importantly describe their fields.
    """

    # __slots__ = (
    #     'fields',
    #     'interfaces',
    # )

    def __init__(
        self,
        name: Union[str, Name],
        fields: Dict[str, GraphQLFieldDefinition],
        interfaces: Optional[List[GraphQLNamedType]] = None,
        **kwargs
    ):
        # In the function signature above, it should be `OrderedDict` but the
        # python 3.6 interpreter fails to interpret the signature correctly.
        super(GraphQLNamedTypeDefinition, self).__init__(name=name, **kwargs)
        self.fields: Dict[str, GraphQLFieldDefinition] = fields
        self.interfaces: Optional[List[GraphQLNamedType]] = interfaces

    def __repr__(self):
        base = super(GraphQLNamedTypeDefinition, self).__repr__()
        return base + "(fields: {}, interfaces: {})".format(
            self.fields, self.interfaces
        )

    def __eq__(self, other):
        return super(GraphQLObjectTypeDefinition, self).__eq__(other) and \
            self.fields == other.fields and \
            self.interfaces == other.interfaces
