import os

from typing import Union

from lark import Lark

from tartiflette.language.parsers.lark.transformers import (
    NodeTransformer,
    TokenTransformer,
)

_LARK_PARSER = Lark.open(
    os.path.join(os.path.dirname(__file__), "graphql_sdl_grammar.lark"),
    start="document",
    parser="lalr",
    lexer="contextual",
    propagate_positions=True,
)


def parse_to_document(sdl: Union[str, bytes]) -> "DocumentNode":
    """
    TODO:
    :param sdl: TODO:
    :type sdl: Union[str, bytes]
    :return: TODO:
    :rtype: DocumentNode

    :Example:
    TODO:
    """
    parsed = _LARK_PARSER.parse(sdl)
    node_transformer = NodeTransformer()
    transformer = TokenTransformer() * node_transformer
    transformer.transform(parsed)
    return node_transformer.document_node
