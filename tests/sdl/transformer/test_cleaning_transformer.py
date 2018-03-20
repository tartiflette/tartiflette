import pytest
from lark.lexer import Token
from lark.tree import Tree

from tartiflette.sdl.builder import parse_graphql_sdl_to_ast
from tartiflette.sdl.transformers.cleaning_transformer import \
    CleaningTransformer


@pytest.mark.parametrize("full_sdl,expected", [
    # The `name` rule cleans up the name Token
    (
        """
        type Something
        """,
        Tree('document', [
            Tree('type_system_definition', [
                Tree('type_definition', [
                    Tree('object_type_definition', [
                        Token('TYPE', 'type'),
                        Token('IDENT', 'Something'),
                    ]),
                ]),
            ]),
        ]),
    ),
    (
        """
        schema {
            query: RootQueryCustomType
        }
        """,
        Tree('document', [
            Tree('type_system_definition', [
                Tree('schema_definition', [
                    Token('SCHEMA', 'schema'),
                    Tree('query_operation_type_definition', [
                        Token('QUERY', 'query'),
                        Tree('named_type', [
                            Token('IDENT', 'RootQueryCustomType'),
                        ]),
                    ]),
                ]),
            ]),
        ]),
    ),
    # `name` rule extract name and returns a NameNode() object, even 'reserved'
    #  words.
    (
        """
        schema {
            query: implements
        }
        """,
        Tree('document', [
            Tree('type_system_definition', [
                Tree('schema_definition', [
                    Token('SCHEMA', 'schema'),
                    Tree('query_operation_type_definition', [
                        Token('QUERY', 'query'),
                        Tree('named_type', [
                            Token('IDENT', 'implements'),
                        ]),
                    ]),
                ]),
            ]),
        ]),
    ),
])
def test_CleaningTransformer_name(full_sdl, expected):

    raw_tree = parse_graphql_sdl_to_ast(full_sdl)
    assert CleaningTransformer(full_sdl).transform(raw_tree) == expected


@pytest.mark.parametrize("str_value,expected_value", [
    # `value` rule extract value and returns a Value object
    (
        "000123",
        Tree('int_value', [
            Token('SIGNED_INT', 123),
        ]),
    ),
    (
        "-9453",
        Tree('int_value', [
            Token('SIGNED_INT', -9453),
        ]),
    ),
    (
        "42.84",
        Tree('float_value', [
            Token('SIGNED_FLOAT', 42.84),
        ]),
    ),
    (
        "1e-005",
        Tree('float_value', [
            Token('SIGNED_FLOAT', 1e-05),
        ]),
    ),
    (
        "\"Some string value with \\\" escaped quotes\"",
        Tree('string_value', [
            Token('STRING', u'Some string value with " escaped quotes'),
        ]),
    ),
    (
        "true",
        Tree('true_value', [
            Token('TRUE', True),
        ]),
    ),
    (
        "false",
        Tree('false_value', [
            Token('FALSE', False),
        ]),
    ),
    (
        "null",
        Tree('null_value', [
            Token('NULL', None),
        ]),
    ),
    (
        "SOME_KEY",
        Tree('enum_value', [
            Token('IDENT', "SOME_KEY"),
        ]),
    ),
    (
        "[ -42, 0.0314E+2, \"Some str\", true, false, null, ENUM_VAL, [10]]",
        Tree('list_value', [
            Tree('value', [
                Tree('int_value', [
                    Token('SIGNED_INT', -42),
                ]),
            ]),
            Tree('value', [
                Tree('float_value', [
                    Token('SIGNED_FLOAT', 0.0314E+2),
                ]),
            ]),
            Tree('value', [
                Tree('string_value', [
                    Token('STRING', "Some str"),
                ]),
            ]),
            Tree('value', [
                Tree('true_value', [
                    Token('TRUE', True),
                ]),
            ]),
            Tree('value', [
                Tree('false_value', [
                    Token('FALSE', False),
                ]),
            ]),
            Tree('value', [
                Tree('null_value', [
                    Token('NULL', None),
                ]),
            ]),
            Tree('value', [
                Tree('enum_value', [
                    Token('IDENT', "ENUM_VAL"),
                ]),
            ]),
            Tree('value', [
                Tree('list_value', [
                    Tree('value', [
                        Tree('int_value', [
                            Token('SIGNED_INT', 10),
                        ]),
                    ]),
                ]),
            ]),
        ]),
    ),
    (
        "{someKey: 10, moar: \"again\", lst: [42, \"madness\"]}",
        Tree('object_value', [
            Tree('object_field', [
                Token('IDENT', 'someKey'),
                Tree('value', [
                    Tree('int_value', [
                        Token('SIGNED_INT', 10),
                    ]),
                ]),
            ]),
            Tree('object_field', [
                Token('IDENT', 'moar'),
                Tree('value', [
                    Tree('string_value', [
                        Token('STRING', "again"),
                    ]),
                ]),
            ]),
            Tree('object_field', [
                Token('IDENT', 'lst'),
                Tree('value', [
                    Tree('list_value', [
                        Tree('value', [
                            Tree('int_value', [
                                Token('SIGNED_INT', 42),
                            ]),
                        ]),
                        Tree('value', [
                            Tree('string_value', [
                                Token('STRING', "madness"),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ]),
    ),
    (
        "{someKey: 10, subobj: {another: \"yes\"}}",
        Tree('object_value', [
            Tree('object_field', [
                Token('IDENT', 'someKey'),
                Tree('value', [
                    Tree('int_value', [
                        Token('SIGNED_INT', 10),
                    ]),
                ]),
            ]),
            Tree('object_field', [
                Token('IDENT', 'subobj'),
                Tree('value', [
                    Tree('object_value', [
                        Tree('object_field', [
                            Token('IDENT', 'another'),
                            Tree('value', [
                                Tree('string_value', [
                                    Token('STRING', "yes"),
                                ]),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ]),
    ),
])
def test_CleaningTransformer_value(str_value, expected_value):
    full_sdl = """
    type Test {{
        fieldName(arg: Int = {}): String
    }}
    """.format(str_value)

    expected = Tree('document', [
        Tree('type_system_definition', [
            Tree('type_definition', [
                Tree('object_type_definition', [
                    Token('TYPE', 'type'),
                    Token('IDENT', "Test"),
                    Tree('fields_definition', [
                        Tree('field_definition', [
                            Token('IDENT', "fieldName"),
                            Tree('arguments_definition', [
                                Tree('input_value_definition', [
                                    Token('IDENT', "arg"),
                                    Tree('type', [
                                        Tree('named_type', [
                                            Token('IDENT', "Int"),
                                        ]),
                                    ]),
                                    Tree('default_value', [
                                        Tree('value', [
                                            expected_value,
                                        ]),
                                    ]),
                                ]),
                            ]),
                            Tree('type', [
                                Tree('named_type', [
                                    Token('IDENT', "String"),
                                ]),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ]),
    ])

    raw_tree = parse_graphql_sdl_to_ast(full_sdl)
    assert CleaningTransformer(full_sdl).transform(raw_tree) == expected
