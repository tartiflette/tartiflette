import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import ValidObjectImplementsRule
from tartiflette.validation.validate import validate_sdl
from tests.functional.utils import assert_unordered_lists


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            scalar String
            interface Foo {
              fooField1(arg1: String): String
              fooField2(arg1: String): String
            }
            type Bar implements Foo {
              fooField1(arg1: String): String
              fooField2(arg1: String): String
            }
            """,
            [],
        ),
        (
            """
            scalar String
            interface Foo
            extend interface Foo {
              fooField1(arg1: String): String
              fooField2(arg1: String): String
            }
            type Bar implements Foo
            extend type Bar {
              fooField1(arg1: String): String
              fooField2(arg1: String): String
            }
            """,
            [],
        ),
        (
            """
            scalar String
            interface Foo {
              fooField1(arg1: String): String
            }
            extend interface Foo {
              fooField2(arg1: String): String
            }
            type Bar implements Foo {
              fooField1(arg1: String): String
            }
            extend type Bar {
              fooField2(arg1: String): String
            }
            """,
            [],
        ),
        (
            """
            scalar String
            interface Foo {
              fooField1(arg1: String): String
              fooField2(arg1: String): String
            }
            interface Bar {
              barField1(arg1: String): String
              barField2(arg1: String): String
            }
            type Baz implements Foo & Bar {
              fooField1(arg1: String): String
              fooField2(arg1: String): String
              barField1(arg1: String): String
              barField2(arg1: String): String
            }
            """,
            [],
        ),
        (
            """
            scalar String
            interface Foo
            extend interface Foo {
              fooField1(arg1: String): String
              fooField2(arg1: String): String
            }
            interface Bar
            extend interface Bar {
              barField1(arg1: String): String
              barField2(arg1: String): String
            }
            type Baz implements Foo & Bar
            extend type Baz {
              fooField1(arg1: String): String
              fooField2(arg1: String): String
              barField1(arg1: String): String
              barField2(arg1: String): String
            }
            """,
            [],
        ),
        (
            """
            scalar String
            interface Foo {
              fooField1(arg1: String): String
            }
            extend interface Foo {
              fooField2(arg1: String): String
            }
            interface Bar {
              barField1(arg1: String): String
            }
            extend interface Bar {
              barField2(arg1: String): String
            }
            type Baz implements Foo {
              barField1(arg1: String): String
              barField2(arg1: String): String
            }
            extend type Baz implements Bar {
              fooField1(arg1: String): String
              fooField2(arg1: String): String
            }
            """,
            [],
        ),
        (
            """
            scalar String
            interface Foo {
              fooField1(arg1: String): String
              fooField2(arg1: String): String
            }
            type Bar implements Foo
            """,
            [
                TartifletteError(
                    message="Interface field < Foo.fooField1 > expected but < Bar > does not provide it.",
                    locations=[
                        Location(line=4, column=15, line_end=4, column_end=46)
                    ],
                ),
                TartifletteError(
                    message="Interface field < Foo.fooField2 > expected but < Bar > does not provide it.",
                    locations=[
                        Location(line=5, column=15, line_end=5, column_end=46)
                    ],
                ),
            ],
        ),
        (
            """
            scalar String
            interface Foo
            extend interface Foo {
              fooField1(arg1: String): String
              fooField2(arg1: String): String
            }
            type Bar implements Foo
            extend type Bar @noop
            """,
            [
                TartifletteError(
                    message="Interface field < Foo.fooField1 > expected but < Bar > does not provide it.",
                    locations=[
                        Location(line=5, column=15, line_end=5, column_end=46)
                    ],
                ),
                TartifletteError(
                    message="Interface field < Foo.fooField2 > expected but < Bar > does not provide it.",
                    locations=[
                        Location(line=6, column=15, line_end=6, column_end=46)
                    ],
                ),
            ],
        ),
        (
            """
            scalar String
            interface Foo {
              fooField1(arg1: String): String
            }
            extend interface Foo {
              fooField2(arg1: String): String
            }
            type Bar implements Foo
            extend type Bar @noop
            """,
            [
                TartifletteError(
                    message="Interface field < Foo.fooField1 > expected but < Bar > does not provide it.",
                    locations=[
                        Location(line=4, column=15, line_end=4, column_end=46)
                    ],
                ),
                TartifletteError(
                    message="Interface field < Foo.fooField2 > expected but < Bar > does not provide it.",
                    locations=[
                        Location(line=7, column=15, line_end=7, column_end=46)
                    ],
                ),
            ],
        ),
        (
            """
            scalar String
            interface Foo {
              fooField1(arg1: String): String
              fooField2(arg1: String): String
            }
            interface Bar {
              barField1(arg1: String): String
              barField2(arg1: String): String
            }
            type Baz implements Foo & Bar
            """,
            [
                TartifletteError(
                    message="Interface field < Foo.fooField1 > expected but < Baz > does not provide it.",
                    locations=[
                        Location(line=4, column=15, line_end=4, column_end=46)
                    ],
                ),
                TartifletteError(
                    message="Interface field < Foo.fooField2 > expected but < Baz > does not provide it.",
                    locations=[
                        Location(line=5, column=15, line_end=5, column_end=46)
                    ],
                ),
                TartifletteError(
                    message="Interface field < Bar.barField1 > expected but < Baz > does not provide it.",
                    locations=[
                        Location(line=8, column=15, line_end=8, column_end=46)
                    ],
                ),
                TartifletteError(
                    message="Interface field < Bar.barField2 > expected but < Baz > does not provide it.",
                    locations=[
                        Location(line=9, column=15, line_end=9, column_end=46)
                    ],
                ),
            ],
        ),
        (
            """
            scalar String
            interface Foo
            extend interface Foo {
              fooField1(arg1: String): String
              fooField2(arg1: String): String
            }
            interface Bar
            extend interface Bar {
              barField1(arg1: String): String
              barField2(arg1: String): String
            }
            type Baz implements Foo & Bar
            extend type Baz @noop
            """,
            [
                TartifletteError(
                    message="Interface field < Foo.fooField1 > expected but < Baz > does not provide it.",
                    locations=[
                        Location(line=5, column=15, line_end=5, column_end=46)
                    ],
                ),
                TartifletteError(
                    message="Interface field < Foo.fooField2 > expected but < Baz > does not provide it.",
                    locations=[
                        Location(line=6, column=15, line_end=6, column_end=46)
                    ],
                ),
                TartifletteError(
                    message="Interface field < Bar.barField1 > expected but < Baz > does not provide it.",
                    locations=[
                        Location(
                            line=10, column=15, line_end=10, column_end=46
                        )
                    ],
                ),
                TartifletteError(
                    message="Interface field < Bar.barField2 > expected but < Baz > does not provide it.",
                    locations=[
                        Location(
                            line=11, column=15, line_end=11, column_end=46
                        )
                    ],
                ),
            ],
        ),
        (
            """
            scalar String
            interface Foo {
              fooField1(arg1: String): String
            }
            extend interface Foo {
              fooField2(arg1: String): String
            }
            interface Bar {
              barField1(arg1: String): String
            }
            extend interface Bar {
              barField2(arg1: String): String
            }
            type Baz implements Foo
            extend type Baz implements Bar
            """,
            [
                TartifletteError(
                    message="Interface field < Foo.fooField1 > expected but < Baz > does not provide it.",
                    locations=[
                        Location(line=4, column=15, line_end=4, column_end=46)
                    ],
                ),
                TartifletteError(
                    message="Interface field < Foo.fooField2 > expected but < Baz > does not provide it.",
                    locations=[
                        Location(line=7, column=15, line_end=7, column_end=46)
                    ],
                ),
                TartifletteError(
                    message="Interface field < Bar.barField1 > expected but < Baz > does not provide it.",
                    locations=[
                        Location(
                            line=10, column=15, line_end=10, column_end=46
                        )
                    ],
                ),
                TartifletteError(
                    message="Interface field < Bar.barField2 > expected but < Baz > does not provide it.",
                    locations=[
                        Location(
                            line=13, column=15, line_end=13, column_end=46
                        )
                    ],
                ),
            ],
        ),
        (
            """
            scalar String
            interface Foo {
              fooField1(arg1: String): String
              fooField2(arg1: String): String!
              fooField3(arg1: String): [String]
              fooField4(arg1: String): [String]!
              fooField5(arg1: String): [String!]!
              fooField6(arg1: String): [[String!]]!
            }
            type Bar implements Foo {
              fooField1(arg1: String): String!
              fooField2(arg1: String): String!
              fooField3(arg1: String): [String!]!
              fooField4(arg1: String): [String!]!
              fooField5(arg1: String): [String!]!
              fooField6(arg1: String): [[String!]]!
            }
            """,
            [],
        ),
        (
            """
            scalar String
            interface Foo {
              fooField1(arg1: String): String
              fooField2(arg1: String): String!
              fooField3(arg1: String): [String]
              fooField4(arg1: String): [String]!
              fooField5(arg1: String): [String!]!
              fooField6(arg1: String): [[String!]]!
            }
            type Bar implements Foo {
              fooField1(arg1: String): String!
              fooField2(arg1: String): String
              fooField3(arg1: String): [String]
              fooField4(arg1: String): [String]
              fooField5(arg1: String): [String]
              fooField6(arg1: String): [[String]]
            }
            """,
            [
                TartifletteError(
                    message="Interface field < Foo.fooField2 > expects type < String! > but < Bar.fooField2 > is type < String >.",
                    locations=[
                        Location(line=5, column=40, line_end=5, column_end=47),
                        Location(
                            line=13, column=40, line_end=13, column_end=46
                        ),
                    ],
                ),
                TartifletteError(
                    message="Interface field < Foo.fooField4 > expects type < [String]! > but < Bar.fooField4 > is type < [String] >.",
                    locations=[
                        Location(line=7, column=40, line_end=7, column_end=49),
                        Location(
                            line=15, column=40, line_end=15, column_end=48
                        ),
                    ],
                ),
                TartifletteError(
                    message="Interface field < Foo.fooField5 > expects type < [String!]! > but < Bar.fooField5 > is type < [String] >.",
                    locations=[
                        Location(line=8, column=40, line_end=8, column_end=50),
                        Location(
                            line=16, column=40, line_end=16, column_end=48
                        ),
                    ],
                ),
                TartifletteError(
                    message="Interface field < Foo.fooField6 > expects type < [[String!]]! > but < Bar.fooField6 > is type < [[String]] >.",
                    locations=[
                        Location(line=9, column=40, line_end=9, column_end=52),
                        Location(
                            line=17, column=40, line_end=17, column_end=50
                        ),
                    ],
                ),
            ],
        ),
        (
            """
            scalar String
            scalar Int
            interface Foo {
              fooField1(arg1: String): String
              fooField2(arg1: String): String!
              fooField3(arg1: String): [String]
              fooField4(arg1: String): [String]!
              fooField5(arg1: String): [String!]!
              fooField6(arg1: String): [[String!]]!
            }
            type Bar implements Foo {
              fooField1(arg1: String): Int
              fooField2(arg1: String): Int!
              fooField3(arg1: String): [Int]
              fooField4(arg1: String): [Int]!
              fooField5(arg1: String): [Int!]!
              fooField6(arg1: String): [[Int!]]!
            }
            """,
            [
                TartifletteError(
                    message="Interface field < Foo.fooField1 > expects type < String > but < Bar.fooField1 > is type < Int >.",
                    locations=[
                        Location(line=5, column=40, line_end=5, column_end=46),
                        Location(
                            line=13, column=40, line_end=13, column_end=43
                        ),
                    ],
                ),
                TartifletteError(
                    message="Interface field < Foo.fooField2 > expects type < String! > but < Bar.fooField2 > is type < Int! >.",
                    locations=[
                        Location(line=6, column=40, line_end=6, column_end=47),
                        Location(
                            line=14, column=40, line_end=14, column_end=44
                        ),
                    ],
                ),
                TartifletteError(
                    message="Interface field < Foo.fooField3 > expects type < [String] > but < Bar.fooField3 > is type < [Int] >.",
                    locations=[
                        Location(line=7, column=40, line_end=7, column_end=48),
                        Location(
                            line=15, column=40, line_end=15, column_end=45
                        ),
                    ],
                ),
                TartifletteError(
                    message="Interface field < Foo.fooField4 > expects type < [String]! > but < Bar.fooField4 > is type < [Int]! >.",
                    locations=[
                        Location(line=8, column=40, line_end=8, column_end=49),
                        Location(
                            line=16, column=40, line_end=16, column_end=46
                        ),
                    ],
                ),
                TartifletteError(
                    message="Interface field < Foo.fooField5 > expects type < [String!]! > but < Bar.fooField5 > is type < [Int!]! >.",
                    locations=[
                        Location(line=9, column=40, line_end=9, column_end=50),
                        Location(
                            line=17, column=40, line_end=17, column_end=47
                        ),
                    ],
                ),
                TartifletteError(
                    message="Interface field < Foo.fooField6 > expects type < [[String!]]! > but < Bar.fooField6 > is type < [[Int!]]! >.",
                    locations=[
                        Location(
                            line=10, column=40, line_end=10, column_end=52
                        ),
                        Location(
                            line=18, column=40, line_end=18, column_end=49
                        ),
                    ],
                ),
            ],
        ),
        (
            """
            scalar String
            interface Foo {
              fooField1(arg1: String, arg2: String): String
              fooField2(arg1: String, arg2: String): String
            }
            type Bar implements Foo {
              fooField1(arg1: String, arg2: String): String
              fooField2(arg1: String, arg2: String): String
            }
            """,
            [],
        ),
        (
            """
            scalar String
            interface Foo
            extend interface Foo {
              fooField1(arg1: String, arg2: String): String
              fooField2(arg1: String, arg2: String): String
            }
            type Bar implements Foo
            extend type Bar {
              fooField1(arg1: String): String
              fooField2: String
            }
            """,
            [
                TartifletteError(
                    message="Interface field argument < Foo.fooField1(arg2:) > expected but < Bar.fooField1 > does not provide it.",
                    locations=[
                        Location(line=5, column=39, line_end=5, column_end=51),
                        Location(
                            line=10, column=15, line_end=10, column_end=46
                        ),
                    ],
                ),
                TartifletteError(
                    message="Interface field argument < Foo.fooField2(arg1:) > expected but < Bar.fooField2 > does not provide it.",
                    locations=[
                        Location(line=6, column=25, line_end=6, column_end=37),
                        Location(
                            line=11, column=15, line_end=11, column_end=32
                        ),
                    ],
                ),
                TartifletteError(
                    message="Interface field argument < Foo.fooField2(arg2:) > expected but < Bar.fooField2 > does not provide it.",
                    locations=[
                        Location(line=6, column=39, line_end=6, column_end=51),
                        Location(
                            line=11, column=15, line_end=11, column_end=32
                        ),
                    ],
                ),
            ],
        ),
        (
            """
            scalar String
            interface Foo {
              fooField1(arg1: String): String
              fooField2(arg1: String!): String!
              fooField3(arg1: [String]): [String]
              fooField4(arg1: [String]!): [String]!
              fooField5(arg1: [String!]!): [String!]!
              fooField6(arg1: [[String!]]!): [[String!]]!
            }
            type Bar implements Foo {
              fooField1(arg1: String): String
              fooField2(arg1: String!): String!
              fooField3(arg1: [String]): [String]
              fooField4(arg1: [String]!): [String]!
              fooField5(arg1: [String!]!): [String!]!
              fooField6(arg1: [[String!]]!): [[String!]]!
            }
            """,
            [],
        ),
        (
            """
            scalar String
            interface Foo {
              fooField1(arg1: String): String
              fooField2(arg1: String!): String!
              fooField3(arg1: [String]): [String]
              fooField4(arg1: [String]!): [String]!
              fooField5(arg1: [String!]!): [String!]!
              fooField6(arg1: [[String!]]!): [[String!]]!
            }
            type Bar implements Foo {
              fooField1(arg1: String!): String
              fooField2(arg1: String): String!
              fooField3(arg1: [String]!): [String]
              fooField4(arg1: [String!]!): [String]!
              fooField5(arg1: [String]): [String!]!
              fooField6(arg1: [[String]]): [[String!]]!
            }
            """,
            [
                TartifletteError(
                    message="Interface field argument < Foo.fooField1(arg1:) > expects type < String > but < Bar.fooField1(arg1:) > is type < String! >.",
                    locations=[
                        Location(line=4, column=25, line_end=4, column_end=37),
                        Location(
                            line=12, column=25, line_end=12, column_end=38
                        ),
                    ],
                ),
                TartifletteError(
                    message="Interface field argument < Foo.fooField2(arg1:) > expects type < String! > but < Bar.fooField2(arg1:) > is type < String >.",
                    locations=[
                        Location(line=5, column=25, line_end=5, column_end=38),
                        Location(
                            line=13, column=25, line_end=13, column_end=37
                        ),
                    ],
                ),
                TartifletteError(
                    message="Interface field argument < Foo.fooField3(arg1:) > expects type < [String] > but < Bar.fooField3(arg1:) > is type < [String]! >.",
                    locations=[
                        Location(line=6, column=25, line_end=6, column_end=39),
                        Location(
                            line=14, column=25, line_end=14, column_end=40
                        ),
                    ],
                ),
                TartifletteError(
                    message="Interface field argument < Foo.fooField4(arg1:) > expects type < [String]! > but < Bar.fooField4(arg1:) > is type < [String!]! >.",
                    locations=[
                        Location(line=7, column=25, line_end=7, column_end=40),
                        Location(
                            line=15, column=25, line_end=15, column_end=41
                        ),
                    ],
                ),
                TartifletteError(
                    message="Interface field argument < Foo.fooField5(arg1:) > expects type < [String!]! > but < Bar.fooField5(arg1:) > is type < [String] >.",
                    locations=[
                        Location(line=8, column=25, line_end=8, column_end=41),
                        Location(
                            line=16, column=25, line_end=16, column_end=39
                        ),
                    ],
                ),
                TartifletteError(
                    message="Interface field argument < Foo.fooField6(arg1:) > expects type < [[String!]]! > but < Bar.fooField6(arg1:) > is type < [[String]] >.",
                    locations=[
                        Location(line=9, column=25, line_end=9, column_end=43),
                        Location(
                            line=17, column=25, line_end=17, column_end=41
                        ),
                    ],
                ),
            ],
        ),
        (
            """
            scalar String
            scalar Int
            interface Foo {
              fooField1(arg1: String): String
              fooField2(arg1: String!): String!
              fooField3(arg1: [String]): [String]
              fooField4(arg1: [String]!): [String]!
              fooField5(arg1: [String!]!): [String!]!
              fooField6(arg1: [[String!]]!): [[String!]]!
            }
            type Bar implements Foo {
              fooField1(arg1: Int): String
              fooField2(arg1: Int!): String!
              fooField3(arg1: [Int]): [String]
              fooField4(arg1: [Int]!): [String]!
              fooField5(arg1: [Int!]!): [String!]!
              fooField6(arg1: [[Int!]]!): [[String!]]!
            }
            """,
            [
                TartifletteError(
                    message="Interface field argument < Foo.fooField1(arg1:) > expects type < String > but < Bar.fooField1(arg1:) > is type < Int >.",
                    locations=[
                        Location(line=5, column=25, line_end=5, column_end=37),
                        Location(
                            line=13, column=25, line_end=13, column_end=34
                        ),
                    ],
                ),
                TartifletteError(
                    message="Interface field argument < Foo.fooField2(arg1:) > expects type < String! > but < Bar.fooField2(arg1:) > is type < Int! >.",
                    locations=[
                        Location(line=6, column=25, line_end=6, column_end=38),
                        Location(
                            line=14, column=25, line_end=14, column_end=35
                        ),
                    ],
                ),
                TartifletteError(
                    message="Interface field argument < Foo.fooField3(arg1:) > expects type < [String] > but < Bar.fooField3(arg1:) > is type < [Int] >.",
                    locations=[
                        Location(line=7, column=25, line_end=7, column_end=39),
                        Location(
                            line=15, column=25, line_end=15, column_end=36
                        ),
                    ],
                ),
                TartifletteError(
                    message="Interface field argument < Foo.fooField4(arg1:) > expects type < [String]! > but < Bar.fooField4(arg1:) > is type < [Int]! >.",
                    locations=[
                        Location(line=8, column=25, line_end=8, column_end=40),
                        Location(
                            line=16, column=25, line_end=16, column_end=37
                        ),
                    ],
                ),
                TartifletteError(
                    message="Interface field argument < Foo.fooField5(arg1:) > expects type < [String!]! > but < Bar.fooField5(arg1:) > is type < [Int!]! >.",
                    locations=[
                        Location(line=9, column=25, line_end=9, column_end=41),
                        Location(
                            line=17, column=25, line_end=17, column_end=38
                        ),
                    ],
                ),
                TartifletteError(
                    message="Interface field argument < Foo.fooField6(arg1:) > expects type < [[String!]]! > but < Bar.fooField6(arg1:) > is type < [[Int!]]! >.",
                    locations=[
                        Location(
                            line=10, column=25, line_end=10, column_end=43
                        ),
                        Location(
                            line=18, column=25, line_end=18, column_end=40
                        ),
                    ],
                ),
            ],
        ),
        (
            """
            scalar String
            interface Foo {
              fooField1(arg1: String): String
              fooField2(arg1: String!): String!
            }
            type Bar implements Foo {
              fooField1(arg1: String, arg2: String!): String
              fooField2(arg1: String!, arg2: [String!]!): String!
            }
            """,
            [
                TartifletteError(
                    message="Object field < Bar.fooField1 > includes required argument arg2 that is missing from the Interface field < Foo.fooField1 >.",
                    locations=[
                        Location(line=8, column=39, line_end=8, column_end=52),
                        Location(line=4, column=15, line_end=4, column_end=46),
                    ],
                ),
                TartifletteError(
                    message="Object field < Bar.fooField2 > includes required argument arg2 that is missing from the Interface field < Foo.fooField2 >.",
                    locations=[
                        Location(line=9, column=40, line_end=9, column_end=56),
                        Location(line=5, column=15, line_end=5, column_end=48),
                    ],
                ),
            ],
        ),
    ],
)
async def test_valid_object_implements(sdl, expected):
    assert_unordered_lists(
        validate_sdl(
            parse_to_document(sdl), rules=[ValidObjectImplementsRule]
        ),
        expected,
    )
