import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import KnownArgumentNamesOnDirectivesRule
from tartiflette.validation.validate import validate_sdl

_SKIP_DIRECTIVE = """
directive @skip(if: Boolean!) on FIELD_DEFINITION
"""
_TEST_DIRECTIVE = """
directive @test(arg: String) on FIELD_DEFINITION
"""


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            f"""
            {_SKIP_DIRECTIVE}
            type Query {{
              dog: String @skip(if: true)
            }}
            """,
            [],
        ),
        (
            f"""
            {_SKIP_DIRECTIVE}
            type Query {{
              dog: String @skip(unless: true)
            }}
            """,
            [
                TartifletteError(
                    message="Unknown argument < unless > on directive < @skip >.",
                    locations=[
                        Location(line=6, column=33, line_end=6, column_end=45)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
                    },
                )
            ],
        ),
        (
            f"""
            {_SKIP_DIRECTIVE}
            type Query {{
              dog: String @skip(iff: true)
            }}
            """,
            [
                TartifletteError(
                    message="Unknown argument < iff > on directive < @skip >. Did you mean if?",
                    locations=[
                        Location(line=6, column=33, line_end=6, column_end=42)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
                    },
                )
            ],
        ),
        (
            """
            type Query {
              foo: String @test(arg: "")
            }
            """
            + _TEST_DIRECTIVE,
            [],
        ),
        (
            """
            type Query {
              foo: String @test(unknown: "")
            }
            """
            + _TEST_DIRECTIVE,
            [
                TartifletteError(
                    message="Unknown argument < unknown > on directive < @test >.",
                    locations=[
                        Location(line=3, column=33, line_end=3, column_end=44)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
                    },
                )
            ],
        ),
        (
            """
            type Query {
              foo: String @test(agr: "")
            }
            """
            + _TEST_DIRECTIVE,
            [
                TartifletteError(
                    message="Unknown argument < agr > on directive < @test >. Did you mean arg?",
                    locations=[
                        Location(line=3, column=33, line_end=3, column_end=40)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
                    },
                )
            ],
        ),
        (
            """
            type Query {
              foo: String @deprecated(unknown: "")
            }
            directive @deprecated(reason: String) on FIELD_DEFINITION
            """,
            [
                TartifletteError(
                    message="Unknown argument < unknown > on directive < @deprecated >.",
                    locations=[
                        Location(line=3, column=39, line_end=3, column_end=50)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
                    },
                )
            ],
        ),
        (
            """
            type Query {
              foo: String @deprecated(reason: "")
            }
            directive @deprecated(arg: String) on FIELD
            """,
            [
                TartifletteError(
                    message="Unknown argument < reason > on directive < @deprecated >.",
                    locations=[
                        Location(line=3, column=39, line_end=3, column_end=49)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
                    },
                )
            ],
        ),
    ],
)
async def test_known_argument_names_on_directives(sdl, expected):
    assert (
        validate_sdl(
            parse_to_document(sdl), rules=[KnownArgumentNamesOnDirectivesRule]
        )
        == expected
    )
