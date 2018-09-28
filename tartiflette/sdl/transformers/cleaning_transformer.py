from lark import Tree, v_args
from lark.lexer import Token
from lark.visitors import Transformer_InPlace

from tartiflette.sdl.transformers.helpers import find_token_in_ast

# pylint: disable=no-self-use


@v_args(tree=True)
class CleaningTransformer(Transformer_InPlace):
    """
    This lark Transformer cleans up `Token`s and `Tree`s
    for the SchemaTransformer
    """

    def __init__(self, input_sdl: str):
        self.input_sdl = input_sdl

    def name(self, tree: Tree) -> Tree:
        token = find_token_in_ast(
            tree.children,
            [
                "IDENT",
                "SCHEMA",
                "QUERY",
                "MUTATION",
                "SUBSCRIPTION",
                "SCALAR",
                "TYPE",
                "INTERFACE",
                "IMPLEMENTS",
                "UNION",
                "ENUM",
                "INPUT",
                "EXTEND",
                "DIRECTIVE",
                "ON",
                "TYPE_SYSTEM_DIRECTIVE_LOCATION",
            ],
        )
        token.type = "IDENT"  # clean up the grammar variations
        return token

    def description(self, tree: Tree) -> Tree:
        """
        We convert tokens 'STRING' and 'LONG_STRING' into a 'DESCRIPTION'
        Token.
        'STRING' tokens contain the first and last quote `"` and are thus
        removed in the process. A similar method is applied to `LONG_STRING`
        that have three `"` quotes before and after the string.

        :param tree: a lark Tree
        :return: returns a Tree
        """
        token = find_token_in_ast(tree.children, ["STRING", "LONG_STRING"])
        cleaned_str = bytes(token.value[1:-1], "utf-8").decode(
            "unicode-escape"
        )
        # TODO: For `LONG_STRING`s, we should remove the indentation spaces
        if token.type == "LONG_STRING":
            cleaned_str = bytes(token.value[3:-3], "utf-8").decode(
                "unicode-escape"
            )
        new_token = Token(
            "DESCRIPTION",
            cleaned_str,
            token.pos_in_stream,
            token.line,
            token.column,
        )
        tree.children = [new_token]
        return tree

    def int_value(self, tree: Tree):
        token = find_token_in_ast(tree.children, ["SIGNED_INT"])
        newtoken = Token(
            token.type,
            int(token.value),
            token.pos_in_stream,
            token.line,
            token.column,
        )
        tree.children = [newtoken]
        return tree

    def float_value(self, tree: Tree):
        token = find_token_in_ast(tree.children, ["SIGNED_FLOAT"])
        newtoken = Token(
            token.type,
            float(token.value),
            token.pos_in_stream,
            token.line,
            token.column,
        )
        tree.children = [newtoken]
        return tree

    def string_value(self, tree: Tree):
        token = find_token_in_ast(tree.children, ["STRING"])
        tmp = bytes(token.value[1:-1], "utf-8").decode("unicode-escape")
        newtoken = Token(
            token.type, tmp, token.pos_in_stream, token.line, token.column
        )
        tree.children = [newtoken]
        return tree

    def true_value(self, tree: Tree) -> Tree:
        token = find_token_in_ast(tree.children, ["TRUE"])
        newtoken = Token(
            token.type, True, token.pos_in_stream, token.line, token.column
        )
        tree.children = [newtoken]
        return tree

    def false_value(self, tree: Tree) -> Tree:
        token = find_token_in_ast(tree.children, ["FALSE"])
        newtoken = Token(
            token.type, False, token.pos_in_stream, token.line, token.column
        )
        tree.children = [newtoken]
        return tree

    def null_value(self, tree: Tree) -> Tree:
        token = find_token_in_ast(tree.children, ["NULL"])
        newtoken = Token(
            token.type, None, token.pos_in_stream, token.line, token.column
        )
        tree.children = [newtoken]
        return tree
