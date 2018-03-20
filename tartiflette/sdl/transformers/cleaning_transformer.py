from lark.lexer import Token
from lark.tree import Transformer_NoRecurse, Tree

from tartiflette.sdl.transformers.helpers import find_token_in_ast


class CleaningTransformer(Transformer_NoRecurse):
    """
    This lark Transformer cleans up `Token`s and `Tree`s
    for the SchemaTransformer
    """

    def __init__(self, input_sdl: str):
        self.input_sdl = input_sdl

    def name(self, tree: Tree):
        token = find_token_in_ast(
            tree.children, [
                'IDENT',
                'SCHEMA',
                'QUERY',
                'MUTATION',
                'SUBSCRIPTION',
                'SCALAR',
                'TYPE',
                'INTERFACE',
                'IMPLEMENTS',
                'UNION',
                'ENUM',
                'INPUT',
                'EXTEND',
                'DIRECTIVE',
                'ON',
                'TYPE_SYSTEM_DIRECTIVE_LOCATION',
            ]
        )
        token.type = 'IDENT'  # clean up the grammar variations
        return token

    def description(self, tree: Tree):
        token = find_token_in_ast(tree.children, ['STRING', 'LONG_STRING'])
        tmp = bytes(token.value[1:-1], "utf-8").decode('unicode-escape')
        if token.type == 'LONG_STRING':
            tmp = bytes(token.value[3:-3], "utf-8").decode('unicode-escape')
        newtoken = Token(
            'DESCRIPTION', tmp, token.pos_in_stream, token.line, token.column
        )
        tree.children = [newtoken]
        return tree

    def int_value(self, tree: Tree):
        token = find_token_in_ast(tree.children, ['SIGNED_INT'])
        newtoken = Token(
            token.type, int(token.value), token.pos_in_stream, token.line,
            token.column
        )
        tree.children = [newtoken]
        return tree

    def float_value(self, tree: Tree):
        token = find_token_in_ast(tree.children, ['SIGNED_FLOAT'])
        newtoken = Token(
            token.type, float(token.value), token.pos_in_stream, token.line,
            token.column
        )
        tree.children = [newtoken]
        return tree

    def string_value(self, tree: Tree):
        token = find_token_in_ast(tree.children, ['STRING'])
        tmp = bytes(token.value[1:-1], "utf-8").decode('unicode-escape')
        newtoken = Token(
            token.type, tmp, token.pos_in_stream, token.line, token.column
        )
        tree.children = [newtoken]
        return tree

    def true_value(self, tree: Tree):
        token = find_token_in_ast(tree.children, ['TRUE'])
        newtoken = Token(
            token.type, True, token.pos_in_stream, token.line, token.column
        )
        tree.children = [newtoken]
        return tree

    def false_value(self, tree: Tree):
        token = find_token_in_ast(tree.children, ['FALSE'])
        newtoken = Token(
            token.type, False, token.pos_in_stream, token.line, token.column
        )
        tree.children = [newtoken]
        return tree

    def null_value(self, tree: Tree):
        token = find_token_in_ast(tree.children, ['NULL'])
        newtoken = Token(
            token.type, None, token.pos_in_stream, token.line, token.column
        )
        tree.children = [newtoken]
        return tree
