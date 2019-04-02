from unittest.mock import Mock

import pytest

from lark import Tree
from lark.lexer import Token

from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark.transformers.token_transformer import (
    TokenTransformer,
    _find_token,
    _override_tree_children,
)

_DEFAULT_TREE_META_MOCK = Mock(line=1, column=2, end_line=3, end_column=4)
_EXPECTED_TREE_LOCATION = Location(line=1, column=2, line_end=3, column_end=4)


@pytest.mark.parametrize(
    "node,searched_token_type,expected",
    [
        (Token("unknown", None), "token_type", None),
        (
            Tree(data="rule", children=[Token("unknown", None)]),
            "token_type",
            None,
        ),
        ([], "token_type", None),
        ([Token("unknown", None)], "token_type", None),
        (Token("token_type", None), "token_type", Token("token_type", None)),
        (
            Tree(data="rule", children=[Token("token_type", None)]),
            "token_type",
            Token("token_type", None),
        ),
        ([Token("token_type", None)], "token_type", Token("token_type", None)),
        (
            Tree(
                data="rule",
                children=[
                    Token("unknown", 1),
                    Token("token_type", 2),
                    Token("token_type", 3),
                ],
            ),
            "token_type",
            Token("token_type", 2),
        ),
        (
            [
                Token("unknown", 1),
                Token("token_type", 2),
                Token("token_type", 3),
            ],
            "token_type",
            Token("token_type", 2),
        ),
    ],
)
def test_find_token(node, searched_token_type, expected):
    assert _find_token(node, searched_token_type) == expected


@pytest.mark.parametrize(
    "tree,new_child",
    [
        (Tree(data="rule", children=[]), Token("token_type", None)),
        (Tree(data="rule", children=[]), None),
    ],
)
def test_override_tree_children(tree, new_child):
    result = _override_tree_children(tree, new_child)
    assert result is tree
    assert len(result.children) == 1
    assert result.children[0] == new_child


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(data="int_value", children=[Token("INTEGER_PART", "0")]),
            Tree(data="int_value", children=[Token("INT_VALUE", 0)]),
        ),
        (
            Tree(data="int_value", children=[Token("INTEGER_PART", "-0")]),
            Tree(data="int_value", children=[Token("INT_VALUE", 0)]),
        ),
        (
            Tree(data="int_value", children=[Token("INTEGER_PART", "1")]),
            Tree(data="int_value", children=[Token("INT_VALUE", 1)]),
        ),
        (
            Tree(data="int_value", children=[Token("INTEGER_PART", "-1")]),
            Tree(data="int_value", children=[Token("INT_VALUE", -1)]),
        ),
        (
            Tree(data="int_value", children=[Token("INTEGER_PART", "21")]),
            Tree(data="int_value", children=[Token("INT_VALUE", 21)]),
        ),
        (
            Tree(data="int_value", children=[Token("INTEGER_PART", "-21")]),
            Tree(data="int_value", children=[Token("INT_VALUE", -21)]),
        ),
    ],
)
def test_tokentransformer_int_value(tree, expected):
    assert TokenTransformer().transform(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="float_value",
                children=[
                    Token("INTEGER_PART", "0"),
                    Token("FRACTIONAL_PART", ".0"),
                ],
            ),
            Tree(data="float_value", children=[Token("FLOAT_VALUE", 0.0)]),
        ),
        (
            Tree(
                data="float_value",
                children=[
                    Token("INTEGER_PART", "-0"),
                    Token("FRACTIONAL_PART", ".0"),
                ],
            ),
            Tree(data="float_value", children=[Token("FLOAT_VALUE", -0.0)]),
        ),
        (
            Tree(
                data="float_value",
                children=[
                    Token("INTEGER_PART", "1"),
                    Token("FRACTIONAL_PART", ".2"),
                ],
            ),
            Tree(data="float_value", children=[Token("FLOAT_VALUE", 1.2)]),
        ),
        (
            Tree(
                data="float_value",
                children=[
                    Token("INTEGER_PART", "-1"),
                    Token("FRACTIONAL_PART", ".2"),
                ],
            ),
            Tree(data="float_value", children=[Token("FLOAT_VALUE", -1.2)]),
        ),
        (
            Tree(
                data="float_value",
                children=[
                    Token("INTEGER_PART", "21"),
                    Token("FRACTIONAL_PART", ".23"),
                ],
            ),
            Tree(data="float_value", children=[Token("FLOAT_VALUE", 21.23)]),
        ),
        (
            Tree(
                data="float_value",
                children=[
                    Token("INTEGER_PART", "-21"),
                    Token("FRACTIONAL_PART", ".23"),
                ],
            ),
            Tree(data="float_value", children=[Token("FLOAT_VALUE", -21.23)]),
        ),
        (
            Tree(
                data="float_value",
                children=[
                    Token("INTEGER_PART", "1234"),
                    Token("EXPONENT_PART", "e2"),
                ],
            ),
            Tree(
                data="float_value", children=[Token("FLOAT_VALUE", 123_400.0)]
            ),
        ),
        (
            Tree(
                data="float_value",
                children=[
                    Token("INTEGER_PART", "-1234"),
                    Token("EXPONENT_PART", "e2"),
                ],
            ),
            Tree(
                data="float_value", children=[Token("FLOAT_VALUE", -123_400.0)]
            ),
        ),
        (
            Tree(
                data="float_value",
                children=[
                    Token("INTEGER_PART", "123"),
                    Token("FRACTIONAL_PART", ".456"),
                    Token("EXPONENT_PART", "e2"),
                ],
            ),
            Tree(data="float_value", children=[Token("FLOAT_VALUE", 12345.6)]),
        ),
        (
            Tree(
                data="float_value",
                children=[
                    Token("INTEGER_PART", "-123"),
                    Token("FRACTIONAL_PART", ".456"),
                    Token("EXPONENT_PART", "e2"),
                ],
            ),
            Tree(
                data="float_value", children=[Token("FLOAT_VALUE", -12345.6)]
            ),
        ),
    ],
)
def test_tokentransformer_float_value(tree, expected):
    assert TokenTransformer().transform(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(data="string_value", children=[Token("STRING", '"aString"')]),
            Tree(
                data="string_value",
                children=[Token("STRING_VALUE", "aString")],
            ),
        ),
        (
            Tree(
                data="string_value",
                children=[Token("LONG_STRING", '"""aLongString"""')],
            ),
            Tree(
                data="string_value",
                children=[Token("STRING_VALUE", "aLongString")],
            ),
        ),
    ],
)
def test_tokentransformer_string_value(tree, expected):
    assert TokenTransformer().transform(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(data="boolean_value", children=[Token("FALSE", "false")]),
            Tree(
                data="boolean_value", children=[Token("BOOLEAN_VALUE", False)]
            ),
        ),
        (
            Tree(data="boolean_value", children=[Token("TRUE", "true")]),
            Tree(
                data="boolean_value", children=[Token("BOOLEAN_VALUE", True)]
            ),
        ),
    ],
)
def test_tokentransformer_boolean_value(tree, expected):
    assert TokenTransformer().transform(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(data="null_value", children=[Token("NULL", "null")]),
            Tree(data="null_value", children=[Token("NULL_VALUE", None)]),
        ),
        (
            Tree(data="null_value", children=[Token("TRUE", "null")]),
            Tree(data="null_value", children=[Token("NULL_VALUE", None)]),
        ),
    ],
)
def test_tokentransformer_null_value(tree, expected):
    assert TokenTransformer().transform(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(data="enum_value", children=[Token("NAME", "ENUM_VALUE")]),
            Tree(data="enum_value", children=[Token("ENUM", "ENUM_VALUE")]),
        )
    ],
)
def test_tokentransformer_enum_value(tree, expected):
    assert TokenTransformer().transform(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(data="name", children=[Token("__ANON_0", "aName")]),
            Tree(data="name", children=[Token("NAME", "aName")]),
        ),
        (
            Tree(data="name", children=[Token("INPUT", "input")]),
            Tree(data="name", children=[Token("NAME", "input")]),
        ),
        (
            Tree(data="name", children=[Token("QUERY", "query")]),
            Tree(data="name", children=[Token("NAME", "query")]),
        ),
        (
            Tree(data="name", children=[Token("EXTEND", "extend")]),
            Tree(data="name", children=[Token("NAME", "extend")]),
        ),
    ],
)
def test_tokentransformer_name(tree, expected):
    assert TokenTransformer().transform(tree) == expected


@pytest.mark.parametrize(
    "tree,expected",
    [
        (
            Tree(
                data="description",
                children=[Token("STRING_VALUE", "aDescription")],
            ),
            Tree(
                data="description",
                children=[Token("DESCRIPTION", "aDescription")],
            ),
        )
    ],
)
def test_tokentransformer_description(tree, expected):
    assert TokenTransformer().transform(tree) == expected
