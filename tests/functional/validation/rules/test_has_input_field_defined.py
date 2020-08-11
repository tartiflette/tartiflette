import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import HasInputFieldDefinedRule
from tartiflette.validation.validate import validate_sdl


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            input Foo {
              field1: String
            }
            type Query {
              field2(arg1: String!): String
            }
            """,
            [],
        ),
        (
            """
            input Foo
            extend input Foo {
              field1: String
            }
            type Query {
              field2(arg1: String!): String
            }
            """,
            [],
        ),
        (
            """
            input Foo {
              field1: String
              field2: String
            }
            input Bar {
              field1: String
              field2: String
            }
            type Query {
              field2(arg1: String!): String
            }
            """,
            [],
        ),
        (
            """
            input Foo
            input Bar
            extend input Foo {
              field1: String
              field2: String
            }
            extend input Bar {
              field1: String
              field2: String
            }
            type Query {
              field2(arg1: String!): String
            }
            """,
            [],
        ),
        (
            """
            input Foo {
              field1: String
            }
            type Query {
              field2(arg1: String!): String
            }
            """,
            [],
        ),
        (
            """
            input Foo
            extend input Foo {
              field1: String
            }
            type Query {
              field2(arg1: String!): String
            }
            """,
            [],
        ),
        (
            """
            input Foo {
              field1: String
              field2: String
            }
            input Bar {
              field1: String
              field2: String
            }
            type Query {
              field2(arg1: String!): String
            }
            """,
            [],
        ),
        (
            """
            input Foo
            input Bar
            extend input Foo {
              field1: String
              field2: String
            }
            extend input Bar {
              field1: String
              field2: String
            }
            type Query {
              field2(arg1: String!): String
            }
            """,
            [],
        ),
        (
            """
            input Foo
            type Query {
              field2(arg1: String!): String
            }
            """,
            [
                TartifletteError(
                    message="Input Object type < Foo > must define one or more fields.",
                    locations=[
                        Location(line=2, column=13, line_end=2, column_end=22)
                    ],
                )
            ],
        ),
        (
            """
            input Foo
            extend input Foo @noop
            type Query {
              field2(arg1: String!): String
            }
            """,
            [
                TartifletteError(
                    message="Input Object type < Foo > must define one or more fields.",
                    locations=[
                        Location(line=2, column=13, line_end=2, column_end=22),
                        Location(line=3, column=13, line_end=3, column_end=35),
                    ],
                )
            ],
        ),
        (
            """
            input Foo {
              field1: String
              field2: String
            }
            input Bar
            type Query {
              field2(arg1: String!): String
            }
            """,
            [
                TartifletteError(
                    message="Input Object type < Bar > must define one or more fields.",
                    locations=[
                        Location(line=6, column=13, line_end=6, column_end=22)
                    ],
                )
            ],
        ),
        (
            """
            input Foo
            input Bar
            extend input Foo {
              field1: String
              field2: String
            }
            extend input Bar @noop
            type Query {
              field2(arg1: String!): String
            }
            """,
            [
                TartifletteError(
                    message="Input Object type < Bar > must define one or more fields.",
                    locations=[
                        Location(line=3, column=13, line_end=3, column_end=22),
                        Location(line=8, column=13, line_end=8, column_end=35),
                    ],
                )
            ],
        ),
    ],
)
async def test_has_input_field_defined(sdl, expected):
    assert (
        validate_sdl(parse_to_document(sdl), rules=[HasInputFieldDefinedRule])
        == expected
    )
