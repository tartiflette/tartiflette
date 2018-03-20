from tartiflette.sdl.transformers.schema import GraphQLBaseObject


class GraphQLDefinition(GraphQLBaseObject):
    """
    This object serves to "mark" the classes that act as definitions
    """

    # __slots__ = (
    #     'description',
    # )

    def __init__(self, **kwargs):
        super(GraphQLBaseObject, self).__init__(**kwargs)
        self.description = kwargs.get('description', None)
