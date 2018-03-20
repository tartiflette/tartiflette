from tartiflette.sdl.transformers.schema import ASTAware


class Name(ASTAware):
    __slots__ = [
        'name',
    ]

    def __init__(self, name: str, **kwargs):
        super(Name, self).__init__(**kwargs)
        self.name = name

    def __repr__(self):
        return 'Name({})'.format(self.name)

    def __eq__(self, other):
        return isinstance(other, Name) and \
               self.name == other.name
