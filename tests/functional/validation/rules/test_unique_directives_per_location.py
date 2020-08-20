import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.language.parsers.libgraphqlparser import (
    parse_to_document as parse_query_to_document,
)
from tartiflette.validation.rules import UniqueDirectivesPerLocationRule
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
            schema { query: Dummy }
            scalar TestScalar
            type TestObject
            interface TestInterface
            union TestUnion
            input TestInput
            """,
            [],
        ),
        (
            """
            schema @directiveA { query: Dummy }
            extend schema @directiveB
            scalar TestScalar @directiveC
            extend scalar TestScalar @directiveD
            type TestObject @directiveE
            extend type TestObject @directiveF
            interface TestInterface @directiveG
            extend interface TestInterface @directiveH
            union TestUnion @directiveI
            extend union TestUnion @directiveJ
            input TestInput @directiveK
            extend input TestInput @directiveL
            """,
            [],
        ),
        (
            """
            schema @directiveA @directiveB { query: Dummy }
            extend schema @directiveA @directiveB
            scalar TestScalar @directiveA @directiveB
            extend scalar TestScalar @directiveA @directiveB
            type TestObject @directiveA @directiveB
            extend type TestObject @directiveA @directiveB
            interface TestInterface @directiveA @directiveB
            extend interface TestInterface @directiveA @directiveB
            union TestUnion @directiveA @directiveB
            extend union TestUnion @directiveA @directiveB
            input TestInput @directiveA @directiveB
            extend input TestInput @directiveA @directiveB
            """,
            [
                TartifletteError(
                    message="The directive < @directiveA > can only be used once at this location.",
                    locations=[
                        Location(line=2, column=20, line_end=2, column_end=31),
                        Location(line=3, column=27, line_end=3, column_end=38),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directiveB > can only be used once at this location.",
                    locations=[
                        Location(line=2, column=32, line_end=2, column_end=43),
                        Location(line=3, column=39, line_end=3, column_end=50),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directiveA > can only be used once at this location.",
                    locations=[
                        Location(line=4, column=31, line_end=4, column_end=42),
                        Location(line=5, column=38, line_end=5, column_end=49),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directiveB > can only be used once at this location.",
                    locations=[
                        Location(line=4, column=43, line_end=4, column_end=54),
                        Location(line=5, column=50, line_end=5, column_end=61),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directiveA > can only be used once at this location.",
                    locations=[
                        Location(line=6, column=29, line_end=6, column_end=40),
                        Location(line=7, column=36, line_end=7, column_end=47),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directiveB > can only be used once at this location.",
                    locations=[
                        Location(line=6, column=41, line_end=6, column_end=52),
                        Location(line=7, column=48, line_end=7, column_end=59),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directiveA > can only be used once at this location.",
                    locations=[
                        Location(line=8, column=37, line_end=8, column_end=48),
                        Location(line=9, column=44, line_end=9, column_end=55),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directiveB > can only be used once at this location.",
                    locations=[
                        Location(line=8, column=49, line_end=8, column_end=60),
                        Location(line=9, column=56, line_end=9, column_end=67),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directiveA > can only be used once at this location.",
                    locations=[
                        Location(
                            line=10, column=29, line_end=10, column_end=40
                        ),
                        Location(
                            line=11, column=36, line_end=11, column_end=47
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directiveB > can only be used once at this location.",
                    locations=[
                        Location(
                            line=10, column=41, line_end=10, column_end=52
                        ),
                        Location(
                            line=11, column=48, line_end=11, column_end=59
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directiveA > can only be used once at this location.",
                    locations=[
                        Location(
                            line=12, column=29, line_end=12, column_end=40
                        ),
                        Location(
                            line=13, column=36, line_end=13, column_end=47
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directiveB > can only be used once at this location.",
                    locations=[
                        Location(
                            line=12, column=41, line_end=12, column_end=52
                        ),
                        Location(
                            line=13, column=48, line_end=13, column_end=59
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
            ],
        ),
        (
            """
            schema @directive { query: Dummy }
            extend schema @directive
            scalar TestScalar @directive
            extend scalar TestScalar @directive
            type TestObject @directive
            extend type TestObject @directive
            interface TestInterface @directive
            extend interface TestInterface @directive
            union TestUnion @directive
            extend union TestUnion @directive
            input TestInput @directive
            extend input TestInput @directive
            """,
            [
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=2, column=20, line_end=2, column_end=30),
                        Location(line=3, column=27, line_end=3, column_end=37),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=4, column=31, line_end=4, column_end=41),
                        Location(line=5, column=38, line_end=5, column_end=48),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=6, column=29, line_end=6, column_end=39),
                        Location(line=7, column=36, line_end=7, column_end=46),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=8, column=37, line_end=8, column_end=47),
                        Location(line=9, column=44, line_end=9, column_end=54),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(
                            line=10, column=29, line_end=10, column_end=39
                        ),
                        Location(
                            line=11, column=36, line_end=11, column_end=46
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(
                            line=12, column=29, line_end=12, column_end=39
                        ),
                        Location(
                            line=13, column=36, line_end=13, column_end=46
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
            ],
        ),
        (
            """
            type Query {
              fieldA: String @directive
              fieldB: String @directive
            }
            """,
            [],
        ),
        (
            """
            type Query {
              field: String @directive @directive
            }
            """,
            [
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=3, column=29, line_end=3, column_end=39),
                        Location(line=3, column=40, line_end=3, column_end=50),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                )
            ],
        ),
        (
            """
            type Query {
              field: String @directive @directive @directive
            }
            """,
            [
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=3, column=29, line_end=3, column_end=39),
                        Location(line=3, column=40, line_end=3, column_end=50),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=3, column=29, line_end=3, column_end=39),
                        Location(line=3, column=51, line_end=3, column_end=61),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
            ],
        ),
        (
            """
            type Query {
              field: String @directiveA @directiveB @directiveA @directiveB
            }
            """,
            [
                TartifletteError(
                    message="The directive < @directiveA > can only be used once at this location.",
                    locations=[
                        Location(line=3, column=29, line_end=3, column_end=40),
                        Location(line=3, column=53, line_end=3, column_end=64),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directiveB > can only be used once at this location.",
                    locations=[
                        Location(line=3, column=41, line_end=3, column_end=52),
                        Location(line=3, column=65, line_end=3, column_end=76),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
            ],
        ),
        (
            """
            type Query @directive @directive {
              field: String @directive @directive
            }
            """,
            [
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=2, column=24, line_end=2, column_end=34),
                        Location(line=2, column=35, line_end=2, column_end=45),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=3, column=29, line_end=3, column_end=39),
                        Location(line=3, column=40, line_end=3, column_end=50),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
            ],
        ),
        (
            """
            schema @directive @directive { query: Dummy }
            extend schema @directive @directive
            scalar TestScalar @directive @directive
            extend scalar TestScalar @directive @directive
            type TestObject @directive @directive
            extend type TestObject @directive @directive
            interface TestInterface @directive @directive
            extend interface TestInterface @directive @directive
            union TestUnion @directive @directive
            extend union TestUnion @directive @directive
            input TestInput @directive @directive
            extend input TestInput @directive @directive
            """,
            [
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=2, column=20, line_end=2, column_end=30),
                        Location(line=2, column=31, line_end=2, column_end=41),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=2, column=20, line_end=2, column_end=30),
                        Location(line=3, column=27, line_end=3, column_end=37),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=2, column=20, line_end=2, column_end=30),
                        Location(line=3, column=38, line_end=3, column_end=48),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=4, column=31, line_end=4, column_end=41),
                        Location(line=4, column=42, line_end=4, column_end=52),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=4, column=31, line_end=4, column_end=41),
                        Location(line=5, column=38, line_end=5, column_end=48),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=4, column=31, line_end=4, column_end=41),
                        Location(line=5, column=49, line_end=5, column_end=59),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=6, column=29, line_end=6, column_end=39),
                        Location(line=6, column=40, line_end=6, column_end=50),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=6, column=29, line_end=6, column_end=39),
                        Location(line=7, column=36, line_end=7, column_end=46),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=6, column=29, line_end=6, column_end=39),
                        Location(line=7, column=47, line_end=7, column_end=57),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=8, column=37, line_end=8, column_end=47),
                        Location(line=8, column=48, line_end=8, column_end=58),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=8, column=37, line_end=8, column_end=47),
                        Location(line=9, column=44, line_end=9, column_end=54),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=8, column=37, line_end=8, column_end=47),
                        Location(line=9, column=55, line_end=9, column_end=65),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(
                            line=10, column=29, line_end=10, column_end=39
                        ),
                        Location(
                            line=10, column=40, line_end=10, column_end=50
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(
                            line=10, column=29, line_end=10, column_end=39
                        ),
                        Location(
                            line=11, column=36, line_end=11, column_end=46
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(
                            line=10, column=29, line_end=10, column_end=39
                        ),
                        Location(
                            line=11, column=47, line_end=11, column_end=57
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(
                            line=12, column=29, line_end=12, column_end=39
                        ),
                        Location(
                            line=12, column=40, line_end=12, column_end=50
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(
                            line=12, column=29, line_end=12, column_end=39
                        ),
                        Location(
                            line=13, column=36, line_end=13, column_end=46
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(
                            line=12, column=29, line_end=12, column_end=39
                        ),
                        Location(
                            line=13, column=47, line_end=13, column_end=57
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
            ],
        ),
    ],
)
async def test_unique_directives_per_location(sdl, expected):
    assert (
        validate_sdl(
            parse_to_document(sdl), rules=[UniqueDirectivesPerLocationRule]
        )
        == expected
    )


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="harness")
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            fragment Test on Type {
              field
            }
            """,
            [],
        ),
        (
            """
            fragment Test on Type @directiveA {
              field @directiveB
            }
            """,
            [],
        ),
        (
            """
            fragment Test on Type @directiveA @directiveB {
              field @directiveA @directiveB
            }
            """,
            [],
        ),
        (
            """
            fragment Test on Type @directiveA {
              field @directiveA
            }
            """,
            [],
        ),
        (
            """
            fragment Test on Type {
              field @directive
              field @directive
            }
            """,
            [],
        ),
        (
            """
            fragment Test on Type {
              field @directive @directive
            }
            """,
            [
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=3, column=21, line_end=3, column_end=31),
                        Location(line=3, column=32, line_end=3, column_end=42),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                )
            ],
        ),
        (
            """
            fragment Test on Type {
              field @directive @directive @directive
            }
            """,
            [
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=3, column=21, line_end=3, column_end=31),
                        Location(line=3, column=32, line_end=3, column_end=42),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=3, column=21, line_end=3, column_end=31),
                        Location(line=3, column=43, line_end=3, column_end=53),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
            ],
        ),
        (
            """
            fragment Test on Type {
              field @directiveA @directiveB @directiveA @directiveB
            }
            """,
            [
                TartifletteError(
                    message="The directive < @directiveA > can only be used once at this location.",
                    locations=[
                        Location(line=3, column=21, line_end=3, column_end=32),
                        Location(line=3, column=45, line_end=3, column_end=56),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directiveB > can only be used once at this location.",
                    locations=[
                        Location(line=3, column=33, line_end=3, column_end=44),
                        Location(line=3, column=57, line_end=3, column_end=68),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
            ],
        ),
        (
            """
            fragment Test on Type @directive @directive {
              field @directive @directive
            }
            """,
            [
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=2, column=35, line_end=2, column_end=45),
                        Location(line=2, column=46, line_end=2, column_end=56),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
                TartifletteError(
                    message="The directive < @directive > can only be used once at this location.",
                    locations=[
                        Location(line=3, column=21, line_end=3, column_end=31),
                        Location(line=3, column=32, line_end=3, column_end=42),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.3",
                        "tag": "directives-are-unique-per-location",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                    },
                ),
            ],
        ),
    ],
)
async def test_unique_directives_per_location_query(
    schema_stack, query, expected
):
    assert_unordered_lists(
        validate_query(
            schema_stack.schema,
            parse_query_to_document(query),
            rules=[UniqueDirectivesPerLocationRule],
        ),
        expected,
    )
