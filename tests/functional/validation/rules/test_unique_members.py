import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import UniqueMembersRule
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
            type Foo
            type Bar
            union Foobar = Foo | Foo
            """,
            [
                TartifletteError(
                    message="Union type < Foobar > can only include type < Foo > once.",
                    locations=[
                        Location(line=4, column=28, line_end=4, column_end=31),
                        Location(line=4, column=34, line_end=4, column_end=37),
                    ],
                )
            ],
        ),
        (
            """
            type Foo
            type Bar
            union Foobar = Foo | Bar | Foo | Bar
            """,
            [
                TartifletteError(
                    message="Union type < Foobar > can only include type < Foo > once.",
                    locations=[
                        Location(line=4, column=28, line_end=4, column_end=31),
                        Location(line=4, column=40, line_end=4, column_end=43),
                    ],
                ),
                TartifletteError(
                    message="Union type < Foobar > can only include type < Bar > once.",
                    locations=[
                        Location(line=4, column=34, line_end=4, column_end=37),
                        Location(line=4, column=46, line_end=4, column_end=49),
                    ],
                ),
            ],
        ),
        (
            """
            type Foo
            type Bar
            union Foobar
            extend union Foobar = Foo | Foo
            """,
            [
                TartifletteError(
                    message="Union type < Foobar > can only include type < Foo > once.",
                    locations=[
                        Location(line=5, column=35, line_end=5, column_end=38),
                        Location(line=5, column=41, line_end=5, column_end=44),
                    ],
                )
            ],
        ),
        (
            """
            type Foo
            type Bar
            union Foobar
            extend union Foobar = Foo | Bar | Foo | Bar
            """,
            [
                TartifletteError(
                    message="Union type < Foobar > can only include type < Foo > once.",
                    locations=[
                        Location(line=5, column=35, line_end=5, column_end=38),
                        Location(line=5, column=47, line_end=5, column_end=50),
                    ],
                ),
                TartifletteError(
                    message="Union type < Foobar > can only include type < Bar > once.",
                    locations=[
                        Location(line=5, column=41, line_end=5, column_end=44),
                        Location(line=5, column=53, line_end=5, column_end=56),
                    ],
                ),
            ],
        ),
        (
            """
            type Foo
            type Bar
            union Foobar = Foo | Foo
            extend union Foobar = Foo | Foo
            """,
            [
                TartifletteError(
                    message="Union type < Foobar > can only include type < Foo > once.",
                    locations=[
                        Location(line=4, column=28, line_end=4, column_end=31),
                        Location(line=4, column=34, line_end=4, column_end=37),
                    ],
                ),
                TartifletteError(
                    message="Union type < Foobar > can only include type < Foo > once.",
                    locations=[
                        Location(line=4, column=28, line_end=4, column_end=31),
                        Location(line=5, column=35, line_end=5, column_end=38),
                    ],
                ),
                TartifletteError(
                    message="Union type < Foobar > can only include type < Foo > once.",
                    locations=[
                        Location(line=4, column=28, line_end=4, column_end=31),
                        Location(line=5, column=41, line_end=5, column_end=44),
                    ],
                ),
            ],
        ),
        (
            """
            type Foo
            type Bar
            union Foobar = Foo | Bar | Foo | Bar
            extend union Foobar = Foo | Bar | Foo | Bar
            """,
            [
                TartifletteError(
                    message="Union type < Foobar > can only include type < Foo > once.",
                    locations=[
                        Location(line=4, column=28, line_end=4, column_end=31),
                        Location(line=4, column=40, line_end=4, column_end=43),
                    ],
                ),
                TartifletteError(
                    message="Union type < Foobar > can only include type < Bar > once.",
                    locations=[
                        Location(line=4, column=34, line_end=4, column_end=37),
                        Location(line=4, column=46, line_end=4, column_end=49),
                    ],
                ),
                TartifletteError(
                    message="Union type < Foobar > can only include type < Foo > once.",
                    locations=[
                        Location(line=4, column=28, line_end=4, column_end=31),
                        Location(line=5, column=35, line_end=5, column_end=38),
                    ],
                ),
                TartifletteError(
                    message="Union type < Foobar > can only include type < Bar > once.",
                    locations=[
                        Location(line=4, column=34, line_end=4, column_end=37),
                        Location(line=5, column=41, line_end=5, column_end=44),
                    ],
                ),
                TartifletteError(
                    message="Union type < Foobar > can only include type < Foo > once.",
                    locations=[
                        Location(line=4, column=28, line_end=4, column_end=31),
                        Location(line=5, column=47, line_end=5, column_end=50),
                    ],
                ),
                TartifletteError(
                    message="Union type < Foobar > can only include type < Bar > once.",
                    locations=[
                        Location(line=4, column=34, line_end=4, column_end=37),
                        Location(line=5, column=53, line_end=5, column_end=56),
                    ],
                ),
            ],
        ),
    ],
)
async def test_unique_members(sdl, expected):
    assert (
        validate_sdl(parse_to_document(sdl), rules=[UniqueMembersRule])
        == expected
    )
