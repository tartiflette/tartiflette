import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import (
    ProvidedRequiredArgumentsOnDirectivesRule,
)
from tartiflette.validation.validate import validate_sdl


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            type Query {
              foo: String @test
            }

            directive @test(arg1: String, arg2: String! = "") on FIELD_DEFINITION
            """,
            [],
        ),
        (
            """
            type Query {
              foo: String @test
            }

            directive @test(arg: String!) on FIELD_DEFINITION
            """,
            [
                TartifletteError(
                    message="Directive < @test > argument < arg > of type < String! > required, but it was not provided.",
                    locations=[
                        Location(line=3, column=27, line_end=3, column_end=32)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.2.1",
                        "tag": "required-arguments",
                        "details": "https://spec.graphql.org/June2018/#sec-Required-Arguments",
                    },
                )
            ],
        ),
        (
            """
            type Query {
              foo: String @include
            }
            directive @include(if: Boolean!) on FIELD | FRAGMENT_SPREAD | INLINE_FRAGMENT
            """,
            [
                TartifletteError(
                    message="Directive < @include > argument < if > of type < Boolean! > required, but it was not provided.",
                    locations=[
                        Location(line=3, column=27, line_end=3, column_end=35)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.2.1",
                        "tag": "required-arguments",
                        "details": "https://spec.graphql.org/June2018/#sec-Required-Arguments",
                    },
                )
            ],
        ),
        (
            """
            type Query {
              foo: String @deprecated
            }
            directive @deprecated(reason: String!) on FIELD
            """,
            [
                TartifletteError(
                    message="Directive < @deprecated > argument < reason > of type < String! > required, but it was not provided.",
                    locations=[
                        Location(line=3, column=27, line_end=3, column_end=38)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.2.1",
                        "tag": "required-arguments",
                        "details": "https://spec.graphql.org/June2018/#sec-Required-Arguments",
                    },
                )
            ],
        ),
    ],
)
async def test_provided_required_arguments_on_directives(sdl, expected):
    assert (
        validate_sdl(
            parse_to_document(sdl),
            rules=[ProvidedRequiredArgumentsOnDirectivesRule],
        )
        == expected
    )
