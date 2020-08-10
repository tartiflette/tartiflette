import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules.valid_input_value_types import (
    ValidInputValueTypesRule,
)
from tartiflette.validation.validate import validate_sdl


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            scalar String
            enum Foo {
              BAR
            }
            input Baz {
              arg: String!
            }
            interface Qux {
              field(arg1: String, arg2: Foo, arg3: Baz): String
            }
            directive @qux(arg1: String, arg2: Foo, arg3: Baz) on FIELD
            type Quux implements Qux {
              field(arg1: String, arg2: Foo, arg3: Baz): String
            }
            type Query {
              field: Quux
            }
            """,
            [],
        ),
        (
            """
            scalar String
            enum Foo {
              BAR
            }
            input Baz {
              arg: [[String!]]!
            }
            interface Qux {
              field(arg1: [[String!]]!, arg2: [[Foo!]]!, arg3: [[Baz!]]!): String
            }
            directive @qux(arg1: [[String!]]!, arg2: [[Foo!]]!, arg3: [[Baz!]]!) on FIELD
            type Quux implements Qux {
              field(arg1: [[String!]]!, arg2: [[Foo!]]!, arg3: [[Baz!]]!): String
            }
            type Query {
              field: Quux
            }
            """,
            [],
        ),
        (
            """
            scalar String
            enum Foo {
              BAR
            }
            input Baz {
              arg: Unknown1
            }
            interface Qux {
              field(arg1: Unknown2, arg2: Unknown3, arg3: Unknown4): String
            }
            directive @qux(arg1: Unknown2, arg2: Unknown3, arg3: Unknown4) on FIELD
            type Quux implements Qux {
              field(arg1: Unknown2, arg2: Unknown3, arg3: Unknown4): String
            }
            type Query {
              field: Quux
            }
            """,
            [
                TartifletteError(
                    message="The type of Baz.arg must be Input type but got: Unknown1.",
                    locations=[
                        Location(line=7, column=20, line_end=7, column_end=28)
                    ],
                ),
                TartifletteError(
                    message="The type of Qux.field(arg1:) must be Input type but got: Unknown2.",
                    locations=[
                        Location(
                            line=10, column=27, line_end=10, column_end=35
                        )
                    ],
                ),
                TartifletteError(
                    message="The type of Qux.field(arg2:) must be Input type but got: Unknown3.",
                    locations=[
                        Location(
                            line=10, column=43, line_end=10, column_end=51
                        )
                    ],
                ),
                TartifletteError(
                    message="The type of Qux.field(arg3:) must be Input type but got: Unknown4.",
                    locations=[
                        Location(
                            line=10, column=59, line_end=10, column_end=67
                        )
                    ],
                ),
                TartifletteError(
                    message="The type of @qux(arg1:) must be Input type but got: Unknown2.",
                    locations=[
                        Location(
                            line=12, column=34, line_end=12, column_end=42
                        )
                    ],
                ),
                TartifletteError(
                    message="The type of @qux(arg2:) must be Input type but got: Unknown3.",
                    locations=[
                        Location(
                            line=12, column=50, line_end=12, column_end=58
                        )
                    ],
                ),
                TartifletteError(
                    message="The type of @qux(arg3:) must be Input type but got: Unknown4.",
                    locations=[
                        Location(
                            line=12, column=66, line_end=12, column_end=74
                        )
                    ],
                ),
                TartifletteError(
                    message="The type of Quux.field(arg1:) must be Input type but got: Unknown2.",
                    locations=[
                        Location(
                            line=14, column=27, line_end=14, column_end=35
                        )
                    ],
                ),
                TartifletteError(
                    message="The type of Quux.field(arg2:) must be Input type but got: Unknown3.",
                    locations=[
                        Location(
                            line=14, column=43, line_end=14, column_end=51
                        )
                    ],
                ),
                TartifletteError(
                    message="The type of Quux.field(arg3:) must be Input type but got: Unknown4.",
                    locations=[
                        Location(
                            line=14, column=59, line_end=14, column_end=67
                        )
                    ],
                ),
            ],
        ),
        (
            """
            type Foo {
              field: String
            }
            input Baz {
              arg: Foo
            }
            interface Qux {
              field(arg: Foo): String
            }
            directive @qux(arg: Foo) on FIELD
            type Quux implements Qux {
              field(arg: Foo): String
            }
            type Query {
              field: Quux
            }
            """,
            [
                TartifletteError(
                    message="The type of Baz.arg must be Input type but got: Foo.",
                    locations=[
                        Location(line=6, column=20, line_end=6, column_end=23)
                    ],
                ),
                TartifletteError(
                    message="The type of Qux.field(arg:) must be Input type but got: Foo.",
                    locations=[
                        Location(line=9, column=26, line_end=9, column_end=29)
                    ],
                ),
                TartifletteError(
                    message="The type of @qux(arg:) must be Input type but got: Foo.",
                    locations=[
                        Location(
                            line=11, column=33, line_end=11, column_end=36
                        )
                    ],
                ),
                TartifletteError(
                    message="The type of Quux.field(arg:) must be Input type but got: Foo.",
                    locations=[
                        Location(
                            line=13, column=26, line_end=13, column_end=29
                        )
                    ],
                ),
            ],
        ),
        (
            """
            type Foo {
              field: String
            }
            input Baz {
              arg: [[Foo!]]!
            }
            interface Qux {
              field(arg: [[Foo!]]!): String
            }
            directive @qux(arg: [[Foo!]]!) on FIELD
            type Quux implements Qux {
              field(arg: [[Foo!]]!): String
            }
            type Query {
              field: Quux
            }
            """,
            [
                TartifletteError(
                    message="The type of Baz.arg must be Input type but got: [[Foo!]]!.",
                    locations=[
                        Location(line=6, column=20, line_end=6, column_end=29)
                    ],
                ),
                TartifletteError(
                    message="The type of Qux.field(arg:) must be Input type but got: [[Foo!]]!.",
                    locations=[
                        Location(line=9, column=26, line_end=9, column_end=35)
                    ],
                ),
                TartifletteError(
                    message="The type of @qux(arg:) must be Input type but got: [[Foo!]]!.",
                    locations=[
                        Location(
                            line=11, column=33, line_end=11, column_end=42
                        )
                    ],
                ),
                TartifletteError(
                    message="The type of Quux.field(arg:) must be Input type but got: [[Foo!]]!.",
                    locations=[
                        Location(
                            line=13, column=26, line_end=13, column_end=35
                        )
                    ],
                ),
            ],
        ),
    ],
)
async def test_valid_input_value_types(sdl, expected):
    assert (
        validate_sdl(parse_to_document(sdl), rules=[ValidInputValueTypesRule])
        == expected
    )
