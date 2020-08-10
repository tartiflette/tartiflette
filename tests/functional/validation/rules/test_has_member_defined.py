import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import HasMemberDefinedRule
from tartiflette.validation.validate import validate_sdl


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            interface Foobar
            scalar String
            type Foo
            type Bar
            union Baz = Foo
            type Qux implements Foobar
            schema {
              query: Qux
            }
            """,
            [],
        ),
        (
            """
            interface Foobar
            scalar String
            type Foo
            type Bar
            union Baz = Foo | Bar
            type Qux implements Foobar
            schema {
              query: Qux
            }
            """,
            [],
        ),
        (
            """
            interface Foobar
            scalar String
            type Foo
            type Bar
            union Baz
            extend union Baz = Foo
            type Qux implements Foobar
            schema {
              query: Qux
            }
            """,
            [],
        ),
        (
            """
            interface Foobar
            scalar String
            type Foo
            type Bar
            union Baz
            extend union Baz = Foo | Bar
            type Qux implements Foobar
            schema {
              query: Qux
            }
            """,
            [],
        ),
        (
            """
            interface Foobar
            scalar String
            type Foo
            type Bar
            union Baz
            type Qux implements Foobar
            schema {
              query: Qux
            }
            """,
            [
                TartifletteError(
                    message="Union type < Baz > must define one or more member types.",
                    locations=[
                        Location(line=6, column=13, line_end=6, column_end=22)
                    ],
                )
            ],
        ),
        (
            """
            interface Foobar
            scalar String
            type Foo
            type Bar
            union Baz
            type Qux implements Foobar
            schema {
              query: Qux
            }
            """,
            [
                TartifletteError(
                    message="Union type < Baz > must define one or more member types.",
                    locations=[
                        Location(line=6, column=13, line_end=6, column_end=22)
                    ],
                )
            ],
        ),
        (
            """
            interface Foobar
            scalar String
            type Foo
            type Bar
            union Baz
            extend union Baz @noop
            type Qux implements Foobar
            schema {
              query: Qux
            }
            """,
            [
                TartifletteError(
                    message="Union type < Baz > must define one or more member types.",
                    locations=[
                        Location(line=6, column=13, line_end=6, column_end=22),
                        Location(line=7, column=13, line_end=7, column_end=35),
                    ],
                )
            ],
        ),
        (
            """
            interface Foobar
            scalar String
            type Foo
            type Bar
            union Baz
            extend union Baz @noop
            type Qux implements Foobar
            schema {
              query: Qux
            }
            """,
            [
                TartifletteError(
                    message="Union type < Baz > must define one or more member types.",
                    locations=[
                        Location(line=6, column=13, line_end=6, column_end=22),
                        Location(line=7, column=13, line_end=7, column_end=35),
                    ],
                )
            ],
        ),
        (
            """
            interface Foobar
            scalar String
            type Foo
            type Bar
            union Baz
            union Foobar
            extend union Baz @noop
            type Qux implements Foobar
            schema {
              query: Qux
            }
            """,
            [
                TartifletteError(
                    message="Union type < Baz > must define one or more member types.",
                    locations=[
                        Location(line=6, column=13, line_end=6, column_end=22),
                        Location(line=8, column=13, line_end=8, column_end=35),
                    ],
                ),
                TartifletteError(
                    message="Union type < Foobar > must define one or more member types.",
                    locations=[
                        Location(line=7, column=13, line_end=7, column_end=25)
                    ],
                ),
            ],
        ),
        (
            """
            interface Foobar
            scalar String
            type Foo
            type Bar
            union Baz
            union Foobar
            extend union Baz @noop
            extend union Foobar = Foo | Bar
            type Qux implements Foobar
            schema {
              query: Qux
            }
            """,
            [
                TartifletteError(
                    message="Union type < Baz > must define one or more member types.",
                    locations=[
                        Location(line=6, column=13, line_end=6, column_end=22),
                        Location(line=8, column=13, line_end=8, column_end=35),
                    ],
                )
            ],
        ),
    ],
)
async def test_has_member_defined(sdl, expected):
    assert (
        validate_sdl(parse_to_document(sdl), rules=[HasMemberDefinedRule])
        == expected
    )
