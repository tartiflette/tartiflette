from lark.lexer import Token
from typing import Optional


class Location(object):

    __slots__ = [
        'line',
        'column',
        'position_in_stream',
        'context',
    ]

    def __init__(
        self,
        line: int,
        column: int,
        position_in_stream: int,
        context: str = None
    ):
        self.line = line
        self.column = column
        self.position_in_stream = position_in_stream
        self.context = context

    def __eq__(self, other: 'Location'):
        return isinstance(other, Location) and \
               self.line == other.line and self.column == other.column \
               and self.position_in_stream == other.position_in_stream

    def __repr__(self):
        return 'Location(line: {}, column: {}, ' \
               'position_in_stream: {}, context: ..."{}"...)'.format(
                self.line, self.column, self.position_in_stream, self.context)

    @staticmethod
    def from_token(
        token: Token, input_sdl: Optional[str] = None, window_size: int = 20
    ):
        new_ctx = None
        if input_sdl:
            ctx_start = token.pos_in_stream - window_size
            if ctx_start < 0:
                ctx_start = 0
            ctx_end = token.pos_in_stream + len(token.value) + window_size
            if ctx_end >= len(input_sdl):
                ctx_end = len(input_sdl) - 1
            new_ctx = input_sdl[ctx_start:ctx_end]
        return Location(token.line, token.column, token.pos_in_stream, new_ctx)
