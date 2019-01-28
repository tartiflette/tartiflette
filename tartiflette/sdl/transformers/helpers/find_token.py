from typing import List, Optional, Union

from lark.lexer import Token
from lark.tree import Tree


def find_token_in_ast(
    ast_node: Union[Tree, Token, list], searched_token_type: List[str]
) -> Optional[Token]:
    if isinstance(ast_node, Token) and ast_node.type in searched_token_type:
        return ast_node
    if isinstance(ast_node, Tree):
        for child in ast_node.children:
            res = find_token_in_ast(child, searched_token_type)
            if res:
                return res
    if isinstance(ast_node, list):
        for child in ast_node:
            res = find_token_in_ast(child, searched_token_type)
            if res:
                return res
    return None
