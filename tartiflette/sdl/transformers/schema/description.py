from tartiflette.sdl.transformers.schema import ASTAware


class Description(ASTAware):
    __slots__ = [
        'description',
    ]

    def __init__(self, description: str, **kwargs):
        super(Description, self).__init__(**kwargs)
        self.description = description

    def __repr__(self):
        return 'Description({})'.format(self.description)

    def __eq__(self, other):
        return isinstance(other, Description) and \
               self.description == other.description
