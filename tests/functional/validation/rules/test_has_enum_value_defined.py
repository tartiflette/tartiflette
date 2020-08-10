import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import HasEnumValueDefinedRule
from tartiflette.validation.validate import validate_sdl


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            enum Foo {
              VALUE1
            }
            """,
            [],
        ),
        (
            """
            enum Foo
            extend enum Foo {
              VALUE1
            }
            """,
            [],
        ),
        (
            """
            enum Foo {
              VALUE1
              VALUE2
            }
            enum Bar {
              VALUE1
              VALUE2
            }
            """,
            [],
        ),
        (
            """
            enum Foo
            enum Bar
            extend enum Foo {
              VALUE1
              VALUE2
            }
            extend enum Bar {
              VALUE1
              VALUE2
            }
            """,
            [],
        ),
        (
            """
            enum Foo {
              VALUE1
            }
            """,
            [],
        ),
        (
            """
            enum Foo
            extend enum Foo {
              VALUE1
            }
            """,
            [],
        ),
        (
            """
            enum Foo {
              VALUE1
              VALUE2
            }
            enum Bar {
              VALUE1
              VALUE2
            }
            """,
            [],
        ),
        (
            """
            enum Foo
            enum Bar
            extend enum Foo {
              VALUE1
              VALUE2
            }
            extend enum Bar {
              VALUE1
              VALUE2
            }
            """,
            [],
        ),
        (
            """
            enum Foo
            """,
            [
                TartifletteError(
                    message="Enum type < Foo > must define one or more values.",
                    locations=[
                        Location(line=2, column=13, line_end=2, column_end=21)
                    ],
                )
            ],
        ),
        (
            """
            enum Foo
            extend enum Foo @noop
            """,
            [
                TartifletteError(
                    message="Enum type < Foo > must define one or more values.",
                    locations=[
                        Location(line=2, column=13, line_end=2, column_end=21),
                        Location(line=3, column=13, line_end=3, column_end=34),
                    ],
                )
            ],
        ),
        (
            """
            enum Foo {
              VALUE1
              VALUE2
            }
            enum Bar
            """,
            [
                TartifletteError(
                    message="Enum type < Bar > must define one or more values.",
                    locations=[
                        Location(line=6, column=13, line_end=6, column_end=21)
                    ],
                )
            ],
        ),
        (
            """
            enum Foo
            enum Bar
            extend enum Foo {
              VALUE1
              VALUE2
            }
            extend enum Bar @noop
            """,
            [
                TartifletteError(
                    message="Enum type < Bar > must define one or more values.",
                    locations=[
                        Location(line=3, column=13, line_end=3, column_end=21),
                        Location(line=8, column=13, line_end=8, column_end=34),
                    ],
                )
            ],
        ),
    ],
)
async def test_has_enum_value_defined(sdl, expected):
    assert (
        validate_sdl(parse_to_document(sdl), rules=[HasEnumValueDefinedRule])
        == expected
    )
