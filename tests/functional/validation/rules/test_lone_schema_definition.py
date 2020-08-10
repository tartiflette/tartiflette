import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import LoneSchemaDefinitionRule
from tartiflette.validation.validate import validate_sdl


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            type Query {
              foo: String
            }
            """,
            [],
        ),
        (
            """
            type Foo {
              foo: String
            }

            schema {
              query: Foo
            }
            """,
            [],
        ),
        (
            """
            type Foo {
              foo: String
            }

            schema {
              query: Foo
            }

            schema {
              mutation: Foo
            }

            schema {
              subscription: Foo
            }
            """,
            [
                TartifletteError(
                    message="Must provide only one schema definition.",
                    locations=[
                        Location(line=6, column=13, line_end=8, column_end=14),
                        Location(
                            line=10, column=13, line_end=12, column_end=14
                        ),
                    ],
                ),
                TartifletteError(
                    message="Must provide only one schema definition.",
                    locations=[
                        Location(line=6, column=13, line_end=8, column_end=14),
                        Location(
                            line=14, column=13, line_end=16, column_end=14
                        ),
                    ],
                ),
            ],
        ),
    ],
)
async def test_lone_schema_definition(sdl, expected):
    assert (
        validate_sdl(parse_to_document(sdl), rules=[LoneSchemaDefinitionRule])
        == expected
    )
