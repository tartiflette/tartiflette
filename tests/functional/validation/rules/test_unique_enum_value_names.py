import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import UniqueEnumValueNamesRule
from tartiflette.validation.validate import validate_sdl


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            enum SomeEnum
            """,
            [],
        ),
        (
            """
            enum SomeEnum {
              FOO
            }
            """,
            [],
        ),
        (
            """
            enum SomeEnum {
              FOO
              BAR
            }
            """,
            [],
        ),
        (
            """
            enum SomeEnum {
              FOO
              BAR
              FOO
            }
            """,
            [
                TartifletteError(
                    message="Enum value < SomeEnum.FOO > can only be defined once.",
                    locations=[
                        Location(line=3, column=15, line_end=3, column_end=18),
                        Location(line=5, column=15, line_end=5, column_end=18),
                    ],
                )
            ],
        ),
        (
            """
            enum SomeEnum {
              FOO
            }
            extend enum SomeEnum {
              BAR
            }
            extend enum SomeEnum {
              BAZ
            }
            """,
            [],
        ),
        (
            """
            extend enum SomeEnum {
              FOO
            }
            enum SomeEnum {
              FOO
            }
            """,
            [
                TartifletteError(
                    message="Enum value < SomeEnum.FOO > can only be defined once.",
                    locations=[
                        Location(line=3, column=15, line_end=3, column_end=18),
                        Location(line=6, column=15, line_end=6, column_end=18),
                    ],
                )
            ],
        ),
        (
            """
            enum SomeEnum
            extend enum SomeEnum {
              FOO
              BAR
              FOO
            }
            """,
            [
                TartifletteError(
                    message="Enum value < SomeEnum.FOO > can only be defined once.",
                    locations=[
                        Location(line=4, column=15, line_end=4, column_end=18),
                        Location(line=6, column=15, line_end=6, column_end=18),
                    ],
                )
            ],
        ),
        (
            """
            enum SomeEnum
            extend enum SomeEnum {
              FOO
            }
            extend enum SomeEnum {
              FOO
            }
            """,
            [
                TartifletteError(
                    message="Enum value < SomeEnum.FOO > can only be defined once.",
                    locations=[
                        Location(line=4, column=15, line_end=4, column_end=18),
                        Location(line=7, column=15, line_end=7, column_end=18),
                    ],
                )
            ],
        ),
    ],
)
async def test_unique_enum_value_names(sdl, expected):
    assert (
        validate_sdl(parse_to_document(sdl), rules=[UniqueEnumValueNamesRule])
        == expected
    )
