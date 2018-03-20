from tartiflette.sdl.transformers.schema import GraphQLBaseObject


class GraphQLType(GraphQLBaseObject):
    def __init__(self, **kwargs):
        super(GraphQLType, self).__init__(**kwargs)
