import os

from typing import Optional

from lark import Lark, Tree

from tartiflette.schema import GraphQLSchema
from tartiflette.sdl.transformers.cleaning_transformer import (
    CleaningTransformer,
)
from tartiflette.sdl.transformers.schema_transformer import SchemaTransformer

_GRAMMAR_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "grammar", "graphql_sdl_grammar.lark"
)


def build_graphql_schema_from_sdl(
    sdl: str, schema: Optional[GraphQLSchema] = None
) -> GraphQLSchema:
    """
    Convert a GraphQL Schema Defnition Language schema into an Abstract
    Syntax Tree.

    :param sdl: a string containg the full schema in GraphQL SDL format
    :param schema: Specify a GraphQLSchema if needed
    :return: a GraphQLSchema object.
    """
    return transform_ast_to_schema(
        sdl, parse_graphql_sdl_to_ast(sdl), schema=schema
    )


def parse_graphql_sdl_to_ast(sdl: str) -> Tree:
    """
    Parses a GraphQL SDL schema into an Abstract Syntax Tree (created by the
    lark library).

    We use the LALR(1) parser for fast parsing of huge trees. The
    grammar is thus a bit less legible but much (much) faster.

    :param sdl: Any GraphQL SDL schema string
    :return: a Lark parser `Tree`
    """
    gqlsdl_parser = Lark.open(
        _GRAMMAR_FILE_PATH,
        start="document",
        parser="lalr",
        lexer="contextual",
        propagate_positions=True,
    )
    gqlsdl = gqlsdl_parser.parse
    return gqlsdl(sdl)

    # TODO: Improve this as below
    # try:
    #     return gqlsdl(sdl)
    # except (UnexpectedToken, ParseError, UnexpectedInput) as e:
    #     raise InvalidSDL(e.message)


def transform_ast_to_schema(
    sdl: str, raw_ast: Tree, schema: Optional[GraphQLSchema] = None
) -> GraphQLSchema:
    """
    Transforms the raw Abstract Syntax Tree into a GraphQLSchema.

    :param sdl: A GraphQL Schema in SDL format
    :param raw_ast: raw Lark AST that parsed the GraphQL SDL schema
    :param schema: A GraphQLSchema to pass to the transformer if needed
    :return: a GraphQL Schema
    """
    transformer = CleaningTransformer(sdl) * SchemaTransformer(
        sdl, schema=schema
    )
    transformer.transform(raw_ast)
    return schema
