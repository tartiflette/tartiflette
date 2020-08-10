import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import UniqueDirectiveNamesRule
from tartiflette.validation.validate import validate_sdl


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            type Foo
            """,
            [],
        ),
        (
            """
            directive @foo on SCHEMA
            """,
            [],
        ),
        (
            """
            directive @foo on SCHEMA
            directive @bar on SCHEMA
            directive @baz on SCHEMA
            """,
            [],
        ),
        (
            """
            type foo

            directive @foo on SCHEMA
            """,
            [],
        ),
        (
            """
            directive @foo on SCHEMA

            directive @foo on SCHEMA
            """,
            [
                TartifletteError(
                    message="There can be only one directive named < @foo >.",
                    locations=[
                        Location(line=2, column=24, line_end=2, column_end=27),
                        Location(line=4, column=24, line_end=4, column_end=27),
                    ],
                )
            ],
        ),
        (
            """
            directive @foo on SCHEMA

            directive @foo on SCHEMA
            directive @foo on SCHEMA
            """,
            [
                TartifletteError(
                    message="There can be only one directive named < @foo >.",
                    locations=[
                        Location(line=2, column=24, line_end=2, column_end=27),
                        Location(line=4, column=24, line_end=4, column_end=27),
                    ],
                ),
                TartifletteError(
                    message="There can be only one directive named < @foo >.",
                    locations=[
                        Location(line=2, column=24, line_end=2, column_end=27),
                        Location(line=5, column=24, line_end=5, column_end=27),
                    ],
                ),
            ],
        ),
    ],
)
async def test_unique_directive_names(sdl, expected):
    assert (
        validate_sdl(parse_to_document(sdl), rules=[UniqueDirectiveNamesRule])
        == expected
    )
