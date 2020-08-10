import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import UniqueInterfaceImplementationRule
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
            type Bar implements Foo & Foo
            """,
            [
                TartifletteError(
                    message="Type < Bar > can only implement < Foo > once.",
                    locations=[
                        Location(line=3, column=33, line_end=3, column_end=36),
                        Location(line=3, column=39, line_end=3, column_end=42),
                    ],
                )
            ],
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
            interface Foo
            interface Bar
            type Baz implements Foo & Bar & Foo
            """,
            [
                TartifletteError(
                    message="Type < Baz > can only implement < Foo > once.",
                    locations=[
                        Location(line=4, column=33, line_end=4, column_end=36),
                        Location(line=4, column=45, line_end=4, column_end=48),
                    ],
                )
            ],
        ),
        (
            """
            interface Foo
            interface Bar
            type Baz implements Foo & Bar & Foo & Bar
            """,
            [
                TartifletteError(
                    message="Type < Baz > can only implement < Foo > once.",
                    locations=[
                        Location(line=4, column=33, line_end=4, column_end=36),
                        Location(line=4, column=45, line_end=4, column_end=48),
                    ],
                ),
                TartifletteError(
                    message="Type < Baz > can only implement < Bar > once.",
                    locations=[
                        Location(line=4, column=39, line_end=4, column_end=42),
                        Location(line=4, column=51, line_end=4, column_end=54),
                    ],
                ),
            ],
        ),
    ],
)
async def test_unique_interface_implementation(sdl, expected):
    assert (
        validate_sdl(
            parse_to_document(sdl), rules=[UniqueInterfaceImplementationRule]
        )
        == expected
    )
