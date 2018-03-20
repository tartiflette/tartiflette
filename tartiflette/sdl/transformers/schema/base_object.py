from tartiflette.sdl.transformers.schema import ASTAware


class GraphQLBaseObject(ASTAware):
    def __init__(self, **kwargs):
        super(GraphQLBaseObject, self).__init__(**kwargs)

    def __eq__(self, other):
        return type(other) is type(self)
