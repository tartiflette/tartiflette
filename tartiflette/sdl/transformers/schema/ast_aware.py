from typing import Union

from lark.lexer import Token
from lark.tree import Tree


class ASTAware(object):

    # __slots__ = (
    #     'ast_node',
    # )

    def __init__(self, **kwargs):
        self.ast_node: Union[Tree, Token] = kwargs.get('ast_node', None)
