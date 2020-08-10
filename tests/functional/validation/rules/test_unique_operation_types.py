import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import UniqueOperationTypesRule
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
            type Foo

            schema {
              query: Foo
              mutation: Foo
              subscription: Foo
            }
            """,
            [],
        ),
        (
            """
            type Foo

            schema { query: Foo }

            extend schema {
              mutation: Foo
              subscription: Foo
            }
            """,
            [],
        ),
        (
            """
            type Foo

            schema { query: Foo }
            extend schema { mutation: Foo }
            extend schema { subscription: Foo }
            """,
            [],
        ),
        (
            """
            type Foo

            extend schema { mutation: Foo }
            extend schema { subscription: Foo }

            schema { query: Foo }
            """,
            [],
        ),
        (
            """
            type Foo

            schema {
              query: Foo
              mutation: Foo
              subscription: Foo

              query: Foo
              mutation: Foo
              subscription: Foo
            }
            """,
            [
                TartifletteError(
                    message="There can be only one < query > type in schema.",
                    locations=[
                        Location(line=5, column=15, line_end=5, column_end=25),
                        Location(line=9, column=15, line_end=9, column_end=25),
                    ],
                ),
                TartifletteError(
                    message="There can be only one < mutation > type in schema.",
                    locations=[
                        Location(line=6, column=15, line_end=6, column_end=28),
                        Location(
                            line=10, column=15, line_end=10, column_end=28
                        ),
                    ],
                ),
                TartifletteError(
                    message="There can be only one < subscription > type in schema.",
                    locations=[
                        Location(line=7, column=15, line_end=7, column_end=32),
                        Location(
                            line=11, column=15, line_end=11, column_end=32
                        ),
                    ],
                ),
            ],
        ),
        (
            """
            type Foo

            schema {
              query: Foo
              mutation: Foo
              subscription: Foo
            }

            extend schema {
              query: Foo
              mutation: Foo
              subscription: Foo
            }
            """,
            [
                TartifletteError(
                    message="There can be only one < query > type in schema.",
                    locations=[
                        Location(line=5, column=15, line_end=5, column_end=25),
                        Location(
                            line=11, column=15, line_end=11, column_end=25
                        ),
                    ],
                ),
                TartifletteError(
                    message="There can be only one < mutation > type in schema.",
                    locations=[
                        Location(line=6, column=15, line_end=6, column_end=28),
                        Location(
                            line=12, column=15, line_end=12, column_end=28
                        ),
                    ],
                ),
                TartifletteError(
                    message="There can be only one < subscription > type in schema.",
                    locations=[
                        Location(line=7, column=15, line_end=7, column_end=32),
                        Location(
                            line=13, column=15, line_end=13, column_end=32
                        ),
                    ],
                ),
            ],
        ),
        (
            """
            type Foo

            schema {
              query: Foo
              mutation: Foo
              subscription: Foo
            }

            extend schema {
              query: Foo
              mutation: Foo
              subscription: Foo
            }

            extend schema {
              query: Foo
              mutation: Foo
              subscription: Foo
            }
            """,
            [
                TartifletteError(
                    message="There can be only one < query > type in schema.",
                    locations=[
                        Location(line=5, column=15, line_end=5, column_end=25),
                        Location(
                            line=11, column=15, line_end=11, column_end=25
                        ),
                    ],
                ),
                TartifletteError(
                    message="There can be only one < mutation > type in schema.",
                    locations=[
                        Location(line=6, column=15, line_end=6, column_end=28),
                        Location(
                            line=12, column=15, line_end=12, column_end=28
                        ),
                    ],
                ),
                TartifletteError(
                    message="There can be only one < subscription > type in schema.",
                    locations=[
                        Location(line=7, column=15, line_end=7, column_end=32),
                        Location(
                            line=13, column=15, line_end=13, column_end=32
                        ),
                    ],
                ),
                TartifletteError(
                    message="There can be only one < query > type in schema.",
                    locations=[
                        Location(line=5, column=15, line_end=5, column_end=25),
                        Location(
                            line=17, column=15, line_end=17, column_end=25
                        ),
                    ],
                ),
                TartifletteError(
                    message="There can be only one < mutation > type in schema.",
                    locations=[
                        Location(line=6, column=15, line_end=6, column_end=28),
                        Location(
                            line=18, column=15, line_end=18, column_end=28
                        ),
                    ],
                ),
                TartifletteError(
                    message="There can be only one < subscription > type in schema.",
                    locations=[
                        Location(line=7, column=15, line_end=7, column_end=32),
                        Location(
                            line=19, column=15, line_end=19, column_end=32
                        ),
                    ],
                ),
            ],
        ),
        (
            """
            type Foo

            schema {
              query: Foo
            }

            extend schema {
              mutation: Foo
              subscription: Foo
            }

            extend schema {
              query: Foo
              mutation: Foo
              subscription: Foo
            }
            """,
            [
                TartifletteError(
                    message="There can be only one < query > type in schema.",
                    locations=[
                        Location(line=5, column=15, line_end=5, column_end=25),
                        Location(
                            line=14, column=15, line_end=14, column_end=25
                        ),
                    ],
                ),
                TartifletteError(
                    message="There can be only one < mutation > type in schema.",
                    locations=[
                        Location(line=9, column=15, line_end=9, column_end=28),
                        Location(
                            line=15, column=15, line_end=15, column_end=28
                        ),
                    ],
                ),
                TartifletteError(
                    message="There can be only one < subscription > type in schema.",
                    locations=[
                        Location(
                            line=10, column=15, line_end=10, column_end=32
                        ),
                        Location(
                            line=16, column=15, line_end=16, column_end=32
                        ),
                    ],
                ),
            ],
        ),
    ],
)
async def test_unique_operation_types(sdl, expected):
    assert (
        validate_sdl(parse_to_document(sdl), rules=[UniqueOperationTypesRule])
        == expected
    )
