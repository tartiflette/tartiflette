import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import UniqueTypeNamesRule
from tartiflette.validation.validate import validate_sdl


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            directive @test on SCHEMA
            """,
            [],
        ),
        (
            """
            type Foo
            """,
            [],
        ),
        (
            """
            type Foo
            type Bar
            type Baz
            """,
            [],
        ),
        (
            """
            type Foo

            scalar Foo
            type Foo
            interface Foo
            union Foo
            enum Foo
            input Foo
            """,
            [
                TartifletteError(
                    message="There can be only one type named < Foo >.",
                    locations=[
                        Location(line=2, column=18, line_end=2, column_end=21),
                        Location(line=4, column=20, line_end=4, column_end=23),
                    ],
                ),
                TartifletteError(
                    message="There can be only one type named < Foo >.",
                    locations=[
                        Location(line=2, column=18, line_end=2, column_end=21),
                        Location(line=5, column=18, line_end=5, column_end=21),
                    ],
                ),
                TartifletteError(
                    message="There can be only one type named < Foo >.",
                    locations=[
                        Location(line=2, column=18, line_end=2, column_end=21),
                        Location(line=6, column=23, line_end=6, column_end=26),
                    ],
                ),
                TartifletteError(
                    message="There can be only one type named < Foo >.",
                    locations=[
                        Location(line=2, column=18, line_end=2, column_end=21),
                        Location(line=7, column=19, line_end=7, column_end=22),
                    ],
                ),
                TartifletteError(
                    message="There can be only one type named < Foo >.",
                    locations=[
                        Location(line=2, column=18, line_end=2, column_end=21),
                        Location(line=8, column=18, line_end=8, column_end=21),
                    ],
                ),
                TartifletteError(
                    message="There can be only one type named < Foo >.",
                    locations=[
                        Location(line=2, column=18, line_end=2, column_end=21),
                        Location(line=9, column=19, line_end=9, column_end=22),
                    ],
                ),
            ],
        ),
    ],
)
async def test_unique_type_names(sdl, expected):
    assert (
        validate_sdl(parse_to_document(sdl), rules=[UniqueTypeNamesRule])
        == expected
    )
