import os

from lark.lark import Lark
from lark.tree import Tree
from tartiflette.sdl.schema import DefaultGraphQLSchema

from tartiflette.sdl.transformers.cleaning_transformer import \
    CleaningTransformer
from tartiflette.sdl.transformers.schema_transformer import SchemaTransformer


def build_graphql_schema_from_sdl(
    input_sdl: str, schema=None
) -> 'GraphQLSchema':
    # TODO: Fix imports so "GraphQLSchema" can be imported here.
    """
    Convert a GraphAL Schema Defnition Language schema into an Abstract
    Syntax Tree.

    :param input_sdl: a string containg the full schema in GraphQL SDL format
    :return: a GraphQLSchema object.
    """
    # TODO: Define where we use the DefaultGraphQLSchema if None is given
    if schema is None:
        schema = DefaultGraphQLSchema
    raw_tree = parse_graphql_sdl_to_ast(input_sdl)
    return transform_ast_to_schema(input_sdl, raw_tree, schema=schema)


def parse_graphql_sdl_to_ast(input_sdl: str) -> Tree:
    """
    Parses a GraphQL SDL schema into an Abstract Syntax Tree (created by the
    lark library).

    We use the LALR(1) parser for fast parsing of huge trees. The
    grammar is thus a bit less legible but much (much) faster.

    :param input_sdl: Any GraphQL SDL schema string
    :return: a Lark parser `Tree`
    """
    __path__ = os.path.dirname(__file__)
    grammar_filename = os.path.join(
        __path__, 'grammar', 'graphql_sdl_grammar.lark'
    )

    with open(grammar_filename) as f:
        gqlsdl_parser = Lark(
            f, start='document', parser='lalr', lexer='contextual'
        )
        gqlsdl = gqlsdl_parser.parse

    return gqlsdl(input_sdl)


def transform_ast_to_schema(
    input_sdl: str, raw_ast: Tree, schema: 'GraphQLSchema' = None
) -> 'GraphQLSchema':
    """
    Transforms the raw Abstract Syntax Tree into a GraphQLSchema.

    :param input_sdl: A GraphQL Schema in SDL format
    :param raw_ast: raw Lark AST that parsed the GraphQL SDL schema
    :return: a GraphQL Schema
    """
    transformer = (
        CleaningTransformer(input_sdl) *
        SchemaTransformer(input_sdl, schema=schema)
    )
    transformer.transform(raw_ast)
    return schema
