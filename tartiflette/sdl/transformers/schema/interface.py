from typing import Dict, Union

from tartiflette.sdl.transformers.schema import GraphQLNamedTypeDefinition, \
    GraphQLFieldDefinition, Name


class GraphQLInterfaceTypeDefinition(GraphQLNamedTypeDefinition):
    """
    Interface Type Definition

    It's an abstract type meaning that its purpose is to define a contract
    and enforce it on one or many fields of an Object type.
    The Interface type is used to describe what types are possible,
    what fields are in common across all types, as well as a
    function to determine which type is actually used
    when the field is resolved.
    """

    # __slots__ = (
    #     'fields',
    # )

    def __init__(
        self, name: Union[str, Name],
        fields: Dict[str, GraphQLFieldDefinition], **kwargs
    ):
        # In the function signature above, it should be `OrderedDict` but the
        # python 3.6 interpreter fails to interpret the signature correctly.
        super(GraphQLInterfaceTypeDefinition, self).__init__(
            name=name, **kwargs
        )
        self.fields: Dict[str, GraphQLFieldDefinition] = fields

    def __repr__(self):
        base = super(GraphQLInterfaceTypeDefinition, self).__repr__()
        return base + "(fields: {})".format(self.fields)

    def __eq__(self, other):
        return super(GraphQLInterfaceTypeDefinition, self).__eq__(other) and \
               self.fields == other.fields
