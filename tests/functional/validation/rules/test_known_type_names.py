import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.language.parsers.libgraphqlparser import (
    parse_to_document as parse_query_to_document,
)
from tartiflette.validation.rules import KnownTypeNamesRule
from tartiflette.validation.validate import validate_query, validate_sdl
from tests.functional.utils import assert_unordered_lists


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            scalar String
            scalar Int
            scalar Float
            scalar Boolean
            scalar ID

            type Query {
              string: String
              int: Int
              float: Float
              boolean: Boolean
              id: ID
            }
            """,
            [],
        ),
        (
            """
            scalar String

            union SomeUnion = SomeObject | AnotherObject

            type SomeObject implements SomeInterface {
              someScalar(arg: SomeInputObject): SomeScalar
            }

            type AnotherObject {
              foo(arg: SomeInputObject): String
            }

            type SomeInterface {
              someScalar(arg: SomeInputObject): SomeScalar
            }

            input SomeInputObject {
              someScalar: SomeScalar
            }

            scalar SomeScalar

            type RootQuery {
              someInterface: SomeInterface
              someUnion: SomeUnion
              someScalar: SomeScalar
              someObject: SomeObject
            }

            schema {
              query: RootQuery
            }
            """,
            [],
        ),
        (
            """
            union SomeUnion = SomeObject | AnotherObject

            type SomeObject implements SomeInterface {
              someScalar(arg: SomeInputObject): SomeScalar
            }

            type AnotherObject {
              foo(arg: SomeInputObject): String
            }

            type SomeInterface {
              someScalar(arg: SomeInputObject): SomeScalar
            }

            input SomeInputObject {
              someScalar: SomeScalar
            }

            scalar SomeScalar

            type RootQuery {
              someInterface: SomeInterface
              someUnion: SomeUnion
              someScalar: SomeScalar
              someObject: SomeObject
            }

            schema {
              query: RootQuery
            }
            """,
            [],
        ),
        (
            """
            union SomeUnion = SomeObject | AnotherObject

            type SomeObject implements SomeInterface {
              someScalar(arg: SomeInputObject): SomeScalar
            }

            type AnotherObject {
              foo(arg: SomeInputObject): UnknownScalar
            }

            type SomeInterface {
              someScalar(arg: SomeInputObject): SomeScalar
            }

            input SomeInputObject {
              someScalar: SomeScalar
            }

            scalar SomeScalar

            type RootQuery {
              someInterface: SomeInterface
              someUnion: SomeUnion
              someScalar: SomeScalar
              someObject: SomeObject
            }

            schema {
              query: RootQuery
            }
            """,
            [
                TartifletteError(
                    message="Unknown type < UnknownScalar >. Did you mean SomeScalar?",
                    locations=[
                        Location(line=9, column=42, line_end=9, column_end=55)
                    ],
                )
            ],
        ),
        (
            """
            type A
            type B

            type SomeObject implements C {
              e(d: D): E
            }

            union SomeUnion = F | G

            interface SomeInterface {
              i(h: H): I
            }

            input SomeInput {
              j: J
            }

            directive @SomeDirective(k: K) on QUERY

            schema {
              query: L
              mutation: M
              subscription: N
            }
            """,
            [
                TartifletteError(
                    message="Unknown type < C >.",
                    locations=[
                        Location(line=5, column=40, line_end=5, column_end=41)
                    ],
                ),
                TartifletteError(
                    message="Unknown type < D >. Did you mean ID?",
                    locations=[
                        Location(line=6, column=20, line_end=6, column_end=21)
                    ],
                ),
                TartifletteError(
                    message="Unknown type < E >.",
                    locations=[
                        Location(line=6, column=24, line_end=6, column_end=25)
                    ],
                ),
                TartifletteError(
                    message="Unknown type < F >.",
                    locations=[
                        Location(line=9, column=31, line_end=9, column_end=32)
                    ],
                ),
                TartifletteError(
                    message="Unknown type < G >.",
                    locations=[
                        Location(line=9, column=35, line_end=9, column_end=36)
                    ],
                ),
                TartifletteError(
                    message="Unknown type < H >.",
                    locations=[
                        Location(
                            line=12, column=20, line_end=12, column_end=21
                        )
                    ],
                ),
                TartifletteError(
                    message="Unknown type < I >. Did you mean ID?",
                    locations=[
                        Location(
                            line=12, column=24, line_end=12, column_end=25
                        )
                    ],
                ),
                TartifletteError(
                    message="Unknown type < J >.",
                    locations=[
                        Location(
                            line=16, column=18, line_end=16, column_end=19
                        )
                    ],
                ),
                TartifletteError(
                    message="Unknown type < K >.",
                    locations=[
                        Location(
                            line=19, column=41, line_end=19, column_end=42
                        )
                    ],
                ),
                TartifletteError(
                    message="Unknown type < L >.",
                    locations=[
                        Location(
                            line=22, column=22, line_end=22, column_end=23
                        )
                    ],
                ),
                TartifletteError(
                    message="Unknown type < M >.",
                    locations=[
                        Location(
                            line=23, column=25, line_end=23, column_end=26
                        )
                    ],
                ),
                TartifletteError(
                    message="Unknown type < N >.",
                    locations=[
                        Location(
                            line=24, column=29, line_end=24, column_end=30
                        )
                    ],
                ),
            ],
        ),
        (
            """
            directive @Foo on QUERY

            type Query {
              foo: Foo
            }
            """,
            [
                TartifletteError(
                    message="Unknown type < Foo >.",
                    locations=[
                        Location(line=5, column=20, line_end=5, column_end=23)
                    ],
                )
            ],
        ),
    ],
)
async def test_known_type_names(sdl, expected):
    assert (
        validate_sdl(parse_to_document(sdl), rules=[KnownTypeNamesRule])
        == expected
    )


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(name="harness")
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query Foo(
              $var: String
              $required: [Int!]!
              $introspectionType: __EnumValue
            ) {
              user(id: 4) {
                pets { ... on Pet { name }, ...PetFields, ... { name } }
              }
            }

            fragment PetFields on Pet {
              name
            }
            """,
            [],
        ),
        (
            """
            query Foo($var: JumbledUpLetters) {
              user(id: 4) {
                name
                pets { ... on Badger { name }, ...PetFields }
              }
            }
            fragment PetFields on Peat {
              name
            }
            """,
            [
                TartifletteError(
                    message="Unknown type < JumbledUpLetters >.",
                    locations=[
                        Location(line=2, column=29, line_end=2, column_end=45)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.1.2",
                        "tag": "fragment-spread-type-existence",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-Spread-Type-Existence",
                    },
                ),
                TartifletteError(
                    message="Unknown type < Badger >.",
                    locations=[
                        Location(line=5, column=31, line_end=5, column_end=37)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.1.2",
                        "tag": "fragment-spread-type-existence",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-Spread-Type-Existence",
                    },
                ),
                TartifletteError(
                    message="Unknown type < Peat >. Did you mean Pet?",
                    locations=[
                        Location(line=8, column=35, line_end=8, column_end=39)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.1.2",
                        "tag": "fragment-spread-type-existence",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-Spread-Type-Existence",
                    },
                ),
            ],
        ),
    ],
)
async def test_known_type_names_query(engine, query, expected):
    assert_unordered_lists(
        validate_query(
            engine._schema,
            parse_query_to_document(query, engine._schema),
            rules=[KnownTypeNamesRule],
        ),
        expected,
    )
