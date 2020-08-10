import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import InputObjectNoCircularRefRule
from tartiflette.validation.validate import validate_sdl


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            scalar String
            input Foo {
              field1: String
              field2: String
            }
            input Bar {
              field1: Foo
              field2: Bar
            }
            """,
            [],
        ),
        (
            """
            scalar String
            input Foo {
              field1: String
              field2: String
            }
            input Bar {
              field1: Foo!
              field2: Bar
            }
            """,
            [],
        ),
        (
            """
            scalar String
            input Foo {
              field1: String
              field2: Bar
            }
            input Bar {
              field1: Foo!
              field2: Bar
            }
            """,
            [],
        ),
        (
            """
            scalar String
            input Foo {
              field1: Bar!
            }
            input Bar {
              field1: Foo
              field2: Bar!
            }
            input Foobar {
              field1: Bar
            }
            """,
            [
                TartifletteError(
                    message="Cannot reference Input Object < Bar > within itself through a series of non-null fields < field2 >.",
                    locations=[
                        Location(line=8, column=15, line_end=8, column_end=27)
                    ],
                )
            ],
        ),
        (
            """
            scalar String
            input Foo {
              field1: Bar!
            }
            input Bar {
              field1: Foo
              field2: [Bar]!
            }
            input Foobar {
              field1: Bar
            }
            """,
            [],
        ),
        (
            """
            scalar String
            input Foo {
              field1: Bar!
            }
            input Bar {
              field1: Foo!
              field2: [Bar]!
            }
            input Foobar {
              field1: Bar
            }
            """,
            [
                TartifletteError(
                    message="Cannot reference Input Object < Foo > within itself through a series of non-null fields < field1.field1 >.",
                    locations=[
                        Location(line=4, column=15, line_end=4, column_end=27),
                        Location(line=7, column=15, line_end=7, column_end=27),
                    ],
                )
            ],
        ),
        (
            """
            scalar String
            input Foo {
              field1: Foobar!
            }
            input Bar {
              field1: Foo
              field2: [Bar!]!
            }
            input Foobar {
              field1: Bar
            }
            """,
            [],
        ),
        (
            """
            scalar String
            input Foo {
              field1: Foobar!
            }
            input Bar {
              field1: Foo
              field2: [Bar!]!
            }
            input Foobar {
              field1: Bar!
            }
            """,
            [],
        ),
        (
            """
            scalar String
            input Foo {
              field1: Foobar!
            }
            input Bar {
              field1: Foo!
              field2: [Bar!]!
            }
            input Foobar {
              field1: Bar!
            }
            """,
            [
                TartifletteError(
                    message="Cannot reference Input Object < Foo > within itself through a series of non-null fields < field1.field1.field1 >.",
                    locations=[
                        Location(line=4, column=15, line_end=4, column_end=30),
                        Location(
                            line=11, column=15, line_end=11, column_end=27
                        ),
                        Location(line=7, column=15, line_end=7, column_end=27),
                    ],
                )
            ],
        ),
        (
            """
            type Query {
              field(arg: SomeInputObject): String
            }

            input SomeInputObject {
              self: SomeInputObject
              arrayOfSelf: [SomeInputObject]
              nonNullArrayOfSelf: [SomeInputObject]!
              nonNullArrayOfNonNullSelf: [SomeInputObject!]!
              intermediateSelf: AnotherInputObject
            }

            input AnotherInputObject {
              parent: SomeInputObject
            }
            """,
            [],
        ),
        (
            """
            type Query {
              field(arg: SomeInputObject): String
            }

            input SomeInputObject {
              nonNullSelf: SomeInputObject!
            }
            """,
            [
                TartifletteError(
                    message="Cannot reference Input Object < SomeInputObject > within itself through a series of non-null fields < nonNullSelf >.",
                    locations=[
                        Location(line=7, column=15, line_end=7, column_end=44)
                    ],
                )
            ],
        ),
        (
            """
            type Query {
              field(arg: SomeInputObject): String
            }

            input SomeInputObject {
              startLoop: AnotherInputObject!
            }

            input AnotherInputObject {
              nextInLoop: YetAnotherInputObject!
            }

            input YetAnotherInputObject {
              closeLoop: SomeInputObject!
            }
            """,
            [
                TartifletteError(
                    message="Cannot reference Input Object < SomeInputObject > within itself through a series of non-null fields < startLoop.nextInLoop.closeLoop >.",
                    locations=[
                        Location(line=7, column=15, line_end=7, column_end=45),
                        Location(
                            line=11, column=15, line_end=11, column_end=49
                        ),
                        Location(
                            line=15, column=15, line_end=15, column_end=42
                        ),
                    ],
                )
            ],
        ),
        (
            """
            type Query {
              field(arg: SomeInputObject): String
            }

            input SomeInputObject {
              startLoop: AnotherInputObject!
            }

            input AnotherInputObject {
              closeLoop: SomeInputObject!
              startSecondLoop: YetAnotherInputObject!
            }

            input YetAnotherInputObject {
              closeSecondLoop: AnotherInputObject!
              nonNullSelf: YetAnotherInputObject!
            }
            """,
            [
                TartifletteError(
                    message="Cannot reference Input Object < SomeInputObject > within itself through a series of non-null fields < startLoop.closeLoop >.",
                    locations=[
                        Location(line=7, column=15, line_end=7, column_end=45),
                        Location(
                            line=11, column=15, line_end=11, column_end=42
                        ),
                    ],
                ),
                TartifletteError(
                    message="Cannot reference Input Object < AnotherInputObject > within itself through a series of non-null fields < startSecondLoop.closeSecondLoop >.",
                    locations=[
                        Location(
                            line=12, column=15, line_end=12, column_end=54
                        ),
                        Location(
                            line=16, column=15, line_end=16, column_end=51
                        ),
                    ],
                ),
                TartifletteError(
                    message="Cannot reference Input Object < YetAnotherInputObject > within itself through a series of non-null fields < nonNullSelf >.",
                    locations=[
                        Location(
                            line=17, column=15, line_end=17, column_end=50
                        )
                    ],
                ),
            ],
        ),
    ],
)
async def test_input_object_no_circular_ref(sdl, expected):
    assert (
        validate_sdl(
            parse_to_document(sdl), rules=[InputObjectNoCircularRefRule]
        )
        == expected
    )
