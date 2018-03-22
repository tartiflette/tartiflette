from typing import Optional


class GraphQLType:
    __slots__ = (
        'name',
        'description',
        # 'sdl_info',  # TODO: Is it useful to store the SDL source AST Node ?
    )

    def __init__(self,
                 name: Optional[str] = None,
                 description: Optional[str]=None):
        self.name = name
        self.description = description

    def __repr__(self) -> str:
        return "{}(name={!r}, description={!r})".format(
            self.__class__.__name__, self.name, self.description
        )

    def __eq__(self, other) -> bool:
        return self is other or (
                type(self) is type(other) and self.name == other.name
        )
