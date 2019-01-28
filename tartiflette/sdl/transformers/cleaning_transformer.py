from lark import Tree, v_args
from lark.lexer import Token
from lark.visitors import Transformer_InPlace

from tartiflette.sdl.transformers.helpers import find_token_in_ast

_NAME_TOKENS = [
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
]
_DESCRIPTION_TOKENS = ["STRING", "LONG_STRING"]
_INT_TOKENS = ["SIGNED_INT"]
_FLOAT_TOKENS = ["SIGNED_FLOAT"]
_STRING_TOKENS = ["STRING"]
_TRUE_TOKENS = ["TRUE"]
_FALSE_TOKENS = ["FALSE"]
_NULL_TOKENS = ["NULL"]


@v_args(tree=True)
class CleaningTransformer(Transformer_InPlace):
    """
    This lark Transformer cleans up `Token`s and `Tree`s
    for the SchemaTransformer
    """

    def __init__(self, input_sdl: str) -> None:
        self.input_sdl = input_sdl

    @staticmethod
    def _add_new_token(tree: Tree, new_token: Token) -> Tree:
        tree.children = [new_token]
        return tree

    def name(self, tree: Tree) -> Tree:
        # pylint: disable=no-self-use
        token = find_token_in_ast(tree.children, _NAME_TOKENS)
        token.type = "IDENT"  # Clean up the grammar variations
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
        token = find_token_in_ast(tree.children, _DESCRIPTION_TOKENS)
        cleaned_str = bytes(token.value[1:-1], "utf-8").decode(
            "unicode-escape"
        )
        # TODO: For `LONG_STRING`s, we should remove the indentation spaces
        if token.type == "LONG_STRING":
            cleaned_str = bytes(token.value[3:-3], "utf-8").decode(
                "unicode-escape"
            )
        return self._add_new_token(
            tree,
            Token(
                "DESCRIPTION",
                cleaned_str,
                token.pos_in_stream,
                token.line,
                token.column,
            ),
        )

    def int_value(self, tree: Tree) -> Tree:
        token = find_token_in_ast(tree.children, _INT_TOKENS)
        return self._add_new_token(
            tree,
            Token(
                token.type,
                int(token.value),
                token.pos_in_stream,
                token.line,
                token.column,
            ),
        )

    def float_value(self, tree: Tree) -> Tree:
        token = find_token_in_ast(tree.children, _FLOAT_TOKENS)
        return self._add_new_token(
            tree,
            Token(
                token.type,
                float(token.value),
                token.pos_in_stream,
                token.line,
                token.column,
            ),
        )

    def string_value(self, tree: Tree) -> Tree:
        token = find_token_in_ast(tree.children, _STRING_TOKENS)
        token_value = bytes(token.value[1:-1], "utf-8").decode(
            "unicode-escape"
        )
        return self._add_new_token(
            tree,
            Token(
                token.type,
                token_value,
                token.pos_in_stream,
                token.line,
                token.column,
            ),
        )

    def true_value(self, tree: Tree) -> Tree:
        token = find_token_in_ast(tree.children, _TRUE_TOKENS)
        return self._add_new_token(
            tree,
            Token(
                token.type, True, token.pos_in_stream, token.line, token.column
            ),
        )

    def false_value(self, tree: Tree) -> Tree:
        token = find_token_in_ast(tree.children, _FALSE_TOKENS)
        return self._add_new_token(
            tree,
            Token(
                token.type,
                False,
                token.pos_in_stream,
                token.line,
                token.column,
            ),
        )

    def null_value(self, tree: Tree) -> Tree:
        token = find_token_in_ast(tree.children, _NULL_TOKENS)
        return self._add_new_token(
            tree,
            Token(
                token.type, None, token.pos_in_stream, token.line, token.column
            ),
        )
