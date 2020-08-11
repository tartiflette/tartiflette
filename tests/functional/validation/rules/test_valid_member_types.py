import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import ValidMemberTypesRule
from tartiflette.validation.validate import validate_sdl


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            type Foo
            type Bar
            union Foobar = Foo
            """,
            [],
        ),
        (
            """
            type Foo
            type Bar
            union Foobar = Foo | Bar
            """,
            [],
        ),
        (
            """
            type Foo
            type Bar
            union Foobar
            extend union Foobar = Foo
            """,
            [],
        ),
        (
            """
            type Foo
            type Bar
            union Foobar
            extend union Foobar = Foo | Bar
            """,
            [],
        ),
        (
            """
            interface Foo
            input Bar
            union Foobar = Foo
            """,
            [
                TartifletteError(
                    message="Union type < Foobar > can only include Object types, it cannot include < Foo >.",
                    locations=[
                        Location(line=4, column=28, line_end=4, column_end=31)
                    ],
                )
            ],
        ),
        (
            """
            interface Foo
            input Bar
            union Foobar = Foo | Bar
            """,
            [
                TartifletteError(
                    message="Union type < Foobar > can only include Object types, it cannot include < Foo >.",
                    locations=[
                        Location(line=4, column=28, line_end=4, column_end=31)
                    ],
                ),
                TartifletteError(
                    message="Union type < Foobar > can only include Object types, it cannot include < Bar >.",
                    locations=[
                        Location(line=4, column=34, line_end=4, column_end=37)
                    ],
                ),
            ],
        ),
        (
            """
            interface Foo
            input Bar
            union Foobar
            extend union Foobar = Foo
            """,
            [
                TartifletteError(
                    message="Union type < Foobar > can only include Object types, it cannot include < Foo >.",
                    locations=[
                        Location(line=5, column=35, line_end=5, column_end=38)
                    ],
                )
            ],
        ),
        (
            """
            interface Foo
            input Bar
            union Foobar
            extend union Foobar = Foo | Bar
            """,
            [
                TartifletteError(
                    message="Union type < Foobar > can only include Object types, it cannot include < Foo >.",
                    locations=[
                        Location(line=5, column=35, line_end=5, column_end=38)
                    ],
                ),
                TartifletteError(
                    message="Union type < Foobar > can only include Object types, it cannot include < Bar >.",
                    locations=[
                        Location(line=5, column=41, line_end=5, column_end=44)
                    ],
                ),
            ],
        ),
    ],
)
async def test_valid_member_types(sdl, expected):
    assert (
        validate_sdl(parse_to_document(sdl), rules=[ValidMemberTypesRule])
        == expected
    )
