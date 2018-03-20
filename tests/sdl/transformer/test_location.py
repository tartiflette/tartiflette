import pytest
from lark.lexer import Token

from tartiflette.sdl.transformers.location import Location


@pytest.mark.parametrize("input,expected", [
    (
        Token("TEST", "42.42", 84, 2, 4),
        Location(2, 4, 84, None),
    ),
    # ignores the context
    (
        Token("TEST", "token", 22, 1, 22),
        Location(1, 22, 22, "some context that should be ignored"),
    ),
])
def test_Location_from_token(input, expected):

    assert Location.from_token(input) == expected


@pytest.mark.parametrize("input_token,input_context,expected_repr", [
    (
        Token("QUERY", "query", 30, 3, 13),
        """
        schema {
            query: QueryRoot
            mutation: MutationRoot
        }
        """,
        """Location(line: 3, column: 13, position_in_stream: 30, context: ..."chema {\n            query: QueryRoot\n        "...)"""
    ),
    (
        Token("SCHEMA", "schema", 9, 1, 10),
        """
        schema {
            query: QueryRoot
            mutation: MutationRoot
        }
        """,
        """Location(line: 1, column: 10, position_in_stream: 9, context: ..."\n        schema {\n            query"...)"""
    ),
    (
        Token("NAME", "Root", 77, 4, 31),
        """
        schema {
            query: QueryRoot
            mutation: MutationRoot
        }
        """,
        """Location(line: 4, column: 31, position_in_stream: 77, context: ..."  mutation: MutationRoot\n        }\n       "...)"""
    ),
])
def test_Location_from_token_with_context(input_token, input_context, expected_repr):

    loc = Location.from_token(input_token, input_context)
    assert repr(loc) == expected_repr
