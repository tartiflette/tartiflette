import pytest
from lark.tree import Tree
from lark.lexer import Token

from tartiflette.sdl.transformers.helpers import find_token_in_ast


@pytest.mark.parametrize("ast_tree,searched_tokens,expected", [
    (
        Tree('document', [
            Tree('type_system_definition', [
                Tree('schema_definition', [
                    Token('SCHEMA', 'schema'),
                    Tree('query_operation_type_definition', [
                        Token('QUERY', 'query'),
                        Tree('named_type', [
                            Token('IDENT', 'RootQueryCustomType')
                        ]),
                    ]),
                ]),
            ]),
        ]),
        ["QUERY"],
        Token('QUERY', 'query'),
    ),
    (
        Tree('document', [
            Tree('type_system_definition', [
                Tree('schema_definition', [
                    Token('SCHEMA', 'schema'),
                    Tree('query_operation_type_definition', [
                        Tree('named_type', [
                            Token('IDENT', 'RootQueryCustomType')
                        ]),
                        Token('QUERY', 'query'),
                    ]),
                ]),
            ]),
        ]),
        ["QUERY"],
        Token('QUERY', 'query'),
    ),
    (
        Token('QUERY', 'query'),
        ["QUERY"],
        Token('QUERY', 'query'),
    ),
    (
        [Token('QUERY', 'query')],
        ["QUERY"],
        Token('QUERY', 'query'),
    ),
])
def test_find_token_in_ast(ast_tree,searched_tokens,expected):
    token = find_token_in_ast(ast_tree, searched_tokens)
    assert token == expected



