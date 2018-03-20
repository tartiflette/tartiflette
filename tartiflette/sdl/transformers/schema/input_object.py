from typing import Dict, Union

from tartiflette.sdl.transformers.schema import GraphQLNamedTypeDefinition, \
    GraphQLFieldDefinition, Name


class GraphQLInputObjectTypeDefinition(GraphQLNamedTypeDefinition):
    """
    Input Object Type Definition

    An input object defines a structured collection of fields which may be
    supplied to a field argument.

    Using `NonNull` will ensure that a value must be provided by the query
    """

    # __slots__ = (
    #     'fields',
    # )

    def __init__(
        self, name: Union[str, Name],
        fields: Dict[str, GraphQLFieldDefinition], **kwargs
    ):
        super(GraphQLInputObjectTypeDefinition, self).__init__(
            name=name, **kwargs
        )
        # In the function signature above, it should be `OrderedDict` but the
        # python 3.6 interpreter fails to interpret the signature correctly.
        self.fields: Dict[str, GraphQLFieldDefinition] = fields

    def __repr__(self):
        base = super(GraphQLInputObjectTypeDefinition, self).__repr__()
        return base + "(fields: {})".format(self.fields)

    def __eq__(self, other):
        return super(GraphQLInputObjectTypeDefinition, self).__eq__(other) and \
               self.fields == other.fields
