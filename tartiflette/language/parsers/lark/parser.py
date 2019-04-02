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
    Returns a DocumentNode instance which represents the SDL after being
    parsed.
    :param sdl: sdl to parse and transform into a DocumentNode
    :type query: Union[str, bytes]
    :return: a DocumentNode representing the sdl
    :rtype: DocumentNode

    :Example:

    >>> from tartiflette.language.parsers.lark import parse_to_document
    >>>
    >>>
    >>> sdl_document = parse_to_document('''type Query {
    >>>   hello(name: String!): String!
    >>> }''')
    """
    parsed = _LARK_PARSER.parse(sdl)
    node_transformer = NodeTransformer()
    transformer = TokenTransformer() * node_transformer
    transformer.transform(parsed)
    return node_transformer.document_node
