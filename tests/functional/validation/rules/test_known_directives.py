import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.language.parsers.libgraphqlparser import (
    parse_to_document as parse_query_to_document,
)
from tartiflette.validation.rules import KnownDirectivesRule
from tartiflette.validation.validate import validate_query, validate_sdl
from tests.functional.utils import assert_unordered_lists

_SCHEMA_WITH_SDL_DIRECTIVES = """
directive @onSchema on SCHEMA
directive @onScalar on SCALAR
directive @onObject on OBJECT
directive @onFieldDefinition on FIELD_DEFINITION
directive @onArgumentDefinition on ARGUMENT_DEFINITION
directive @onInterface on INTERFACE
directive @onUnion on UNION
directive @onEnum on ENUM
directive @onEnumValue on ENUM_VALUE
directive @onInputObject on INPUT_OBJECT
directive @onInputFieldDefinition on INPUT_FIELD_DEFINITION
"""


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            type Query {
              foo: String @test
            }

            directive @test on FIELD_DEFINITION
            """,
            [],
        ),
        (
            """
            type Query {
              foo: String @unknown
            }

            directive @test on FIELD_DEFINITION
            """,
            [
                TartifletteError(
                    message="Unknown directive < @unknown >.",
                    locations=[
                        Location(line=3, column=27, line_end=3, column_end=35)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.1",
                        "tag": "directives-are-defined",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Defined",
                    },
                )
            ],
        ),
        (
            """
            type Query {
              foo: String @unknown
            }
            """,
            [
                TartifletteError(
                    message="Unknown directive < @unknown >.",
                    locations=[
                        Location(line=3, column=27, line_end=3, column_end=35)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.1",
                        "tag": "directives-are-defined",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Defined",
                    },
                )
            ],
        ),
        (
            """
            directive @deprecated on FIELD_DEFINITION

            type Query {
              foo: String @deprecated
            }
            """,
            [],
        ),
        (
            """
            schema @deprecated {
              query: Query
            }
            directive @deprecated on SCHEMA
            """,
            [],
        ),
        (
            """
            type MyObj implements MyInterface @onObject {
              myField(myArg: Int @onArgumentDefinition): String @onFieldDefinition
            }

            extend type MyObj @onObject

            scalar MyScalar @onScalar

            extend scalar MyScalar @onScalar

            interface MyInterface @onInterface {
              myField(myArg: Int @onArgumentDefinition): String @onFieldDefinition
            }

            extend interface MyInterface @onInterface

            union MyUnion @onUnion = MyObj | Other

            extend union MyUnion @onUnion

            enum MyEnum @onEnum {
              MY_VALUE @onEnumValue
            }

            extend enum MyEnum @onEnum

            input MyInput @onInputObject {
              myField: Int @onInputFieldDefinition
            }

            extend input MyInput @onInputObject

            schema @onSchema {
              query: MyQuery
            }

            extend schema @onSchema
            """
            + _SCHEMA_WITH_SDL_DIRECTIVES,
            [],
        ),
        (
            """
            type MyObj implements MyInterface @onInterface {
              myField(myArg: Int @onInputFieldDefinition): String @onInputFieldDefinition
            }

            scalar MyScalar @onEnum

            interface MyInterface @onObject {
              myField(myArg: Int @onInputFieldDefinition): String @onInputFieldDefinition
            }

            union MyUnion @onEnumValue = MyObj | Other

            enum MyEnum @onScalar {
              MY_VALUE @onUnion
            }

            input MyInput @onEnum {
              myField: Int @onArgumentDefinition
            }

            schema @onObject {
              query: MyQuery
            }

            extend schema @onObject
            """
            + _SCHEMA_WITH_SDL_DIRECTIVES,
            [
                TartifletteError(
                    message="Directive < @onInterface > may not be used on OBJECT.",
                    locations=[
                        Location(line=2, column=47, line_end=2, column_end=59)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                ),
                TartifletteError(
                    message="Directive < @onInputFieldDefinition > may not be used on ARGUMENT_DEFINITION.",
                    locations=[
                        Location(line=3, column=34, line_end=3, column_end=57)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                ),
                TartifletteError(
                    message="Directive < @onInputFieldDefinition > may not be used on FIELD_DEFINITION.",
                    locations=[
                        Location(line=3, column=67, line_end=3, column_end=90)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                ),
                TartifletteError(
                    message="Directive < @onEnum > may not be used on SCALAR.",
                    locations=[
                        Location(line=6, column=29, line_end=6, column_end=36)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                ),
                TartifletteError(
                    message="Directive < @onObject > may not be used on INTERFACE.",
                    locations=[
                        Location(line=8, column=35, line_end=8, column_end=44)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                ),
                TartifletteError(
                    message="Directive < @onInputFieldDefinition > may not be used on ARGUMENT_DEFINITION.",
                    locations=[
                        Location(line=9, column=34, line_end=9, column_end=57)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                ),
                TartifletteError(
                    message="Directive < @onInputFieldDefinition > may not be used on FIELD_DEFINITION.",
                    locations=[
                        Location(line=9, column=67, line_end=9, column_end=90)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                ),
                TartifletteError(
                    message="Directive < @onEnumValue > may not be used on UNION.",
                    locations=[
                        Location(
                            line=12, column=27, line_end=12, column_end=39
                        )
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                ),
                TartifletteError(
                    message="Directive < @onScalar > may not be used on ENUM.",
                    locations=[
                        Location(
                            line=14, column=25, line_end=14, column_end=34
                        )
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                ),
                TartifletteError(
                    message="Directive < @onUnion > may not be used on ENUM_VALUE.",
                    locations=[
                        Location(
                            line=15, column=24, line_end=15, column_end=32
                        )
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                ),
                TartifletteError(
                    message="Directive < @onEnum > may not be used on INPUT_OBJECT.",
                    locations=[
                        Location(
                            line=18, column=27, line_end=18, column_end=34
                        )
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                ),
                TartifletteError(
                    message="Directive < @onArgumentDefinition > may not be used on INPUT_FIELD_DEFINITION.",
                    locations=[
                        Location(
                            line=19, column=28, line_end=19, column_end=49
                        )
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                ),
                TartifletteError(
                    message="Directive < @onObject > may not be used on SCHEMA.",
                    locations=[
                        Location(
                            line=22, column=20, line_end=22, column_end=29
                        )
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                ),
                TartifletteError(
                    message="Directive < @onObject > may not be used on SCHEMA.",
                    locations=[
                        Location(
                            line=26, column=27, line_end=26, column_end=36
                        )
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                ),
            ],
        ),
    ],
)
async def test_known_directives(sdl, expected):
    assert (
        validate_sdl(parse_to_document(sdl), rules=[KnownDirectivesRule])
        == expected
    )


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="harness")
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query Foo {
              name
              ...Frag
            }

            fragment Frag on Dog {
              name
            }
            """,
            [],
        ),
        (
            """
            {
              dog @include(if: true) {
                name
              }
              human @skip(if: false) {
                name
              }
            }
            """,
            [],
        ),
        (
            """
            {
              dog @unknown(directive: "value") {
                name
              }
            }
            """,
            [
                TartifletteError(
                    message="Unknown directive < @unknown >.",
                    locations=[
                        Location(line=3, column=19, line_end=3, column_end=47)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.1",
                        "tag": "directives-are-defined",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Defined",
                    },
                )
            ],
        ),
        (
            """
            {
              dog @unknown(directive: "value") {
                name
              }
              human @unknown(directive: "value") {
                name
                pets @unknown(directive: "value") {
                  name
                }
              }
            }
            """,
            [
                TartifletteError(
                    message="Unknown directive < @unknown >.",
                    locations=[
                        Location(line=3, column=19, line_end=3, column_end=47)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.1",
                        "tag": "directives-are-defined",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Defined",
                    },
                ),
                TartifletteError(
                    message="Unknown directive < @unknown >.",
                    locations=[
                        Location(line=6, column=21, line_end=6, column_end=49)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.1",
                        "tag": "directives-are-defined",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Defined",
                    },
                ),
                TartifletteError(
                    message="Unknown directive < @unknown >.",
                    locations=[
                        Location(line=8, column=22, line_end=8, column_end=50)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.1",
                        "tag": "directives-are-defined",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Defined",
                    },
                ),
            ],
        ),
        (
            """
            query ($var: Boolean) @onQuery {
              name @include(if: $var)
              ...Frag @include(if: true)
              skippedField @skip(if: true)
              ...SkippedFrag @skip(if: true)

              ... @skip(if: true) {
                skippedField
              }
            }

            mutation @onMutation {
              someField
            }

            subscription @onSubscription {
              someField
            }

            fragment Frag on SomeType @onFragmentDefinition {
              someField
            }
            """,
            [],
        ),
        (
            """
            query Foo($var: Boolean) @include(if: true) {
              name @onQuery @include(if: $var)
              ...Frag @onQuery
            }

            mutation Bar @onQuery {
              someField
            }
            """,
            [
                TartifletteError(
                    message="Directive < @include > may not be used on QUERY.",
                    locations=[
                        Location(line=2, column=38, line_end=2, column_end=56)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                ),
                TartifletteError(
                    message="Directive < @onQuery > may not be used on FIELD.",
                    locations=[
                        Location(line=3, column=20, line_end=3, column_end=28)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                ),
                TartifletteError(
                    message="Directive < @onQuery > may not be used on FRAGMENT_SPREAD.",
                    locations=[
                        Location(line=4, column=23, line_end=4, column_end=31)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                ),
                TartifletteError(
                    message="Directive < @onQuery > may not be used on MUTATION.",
                    locations=[
                        Location(line=7, column=26, line_end=7, column_end=34)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                ),
            ],
        ),
    ],
)
async def test_known_directives_query(schema_stack, query, expected):
    assert_unordered_lists(
        validate_query(
            schema_stack.schema,
            parse_query_to_document(query),
            rules=[KnownDirectivesRule],
        ),
        expected,
    )
