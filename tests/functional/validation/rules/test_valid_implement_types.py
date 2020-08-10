import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import ValidImplementTypesRule
from tartiflette.validation.validate import validate_sdl


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            interface Foo
            type Bar implements Foo
            """,
            [],
        ),
        (
            """
            interface Foo
            interface Bar
            type Baz implements Foo & Bar
            """,
            [],
        ),
        (
            """
            scalar Foo
            type Bar implements Foo
            """,
            [
                TartifletteError(
                    message="Type < Bar > must only implement Interface types, it cannot implement < Foo >.",
                    locations=[
                        Location(line=3, column=33, line_end=3, column_end=36)
                    ],
                )
            ],
        ),
        (
            """
            type Foo
            input Bar
            union Baz
            type Foobar implements Foo & Bar & Baz
            """,
            [
                TartifletteError(
                    message="Type < Foobar > must only implement Interface types, it cannot implement < Foo >.",
                    locations=[
                        Location(line=5, column=36, line_end=5, column_end=39)
                    ],
                ),
                TartifletteError(
                    message="Type < Foobar > must only implement Interface types, it cannot implement < Bar >.",
                    locations=[
                        Location(line=5, column=42, line_end=5, column_end=45)
                    ],
                ),
                TartifletteError(
                    message="Type < Foobar > must only implement Interface types, it cannot implement < Baz >.",
                    locations=[
                        Location(line=5, column=48, line_end=5, column_end=51)
                    ],
                ),
            ],
        ),
    ],
)
async def test_valid_implement_types(sdl, expected):
    assert (
        validate_sdl(parse_to_document(sdl), rules=[ValidImplementTypesRule])
        == expected
    )
