import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.validation.rules import ProvidedRequiredArgumentsRule
from tartiflette.validation.validate import validate_query
from tests.functional.utils import assert_unordered_lists


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="harness")
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            {
              dog {
                isHouseTrained(unknownArgument: true)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              dog {
                isHouseTrained(atOtherHomes: true)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              dog {
                isHouseTrained
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                nonNullFieldWithDefault
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                multipleReqs(req1: 1, req2: 2)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                multipleReqs(req2: 2, req1: 1)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                multipleOpts
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                multipleOpts(opt1: 1)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                multipleOpts(opt2: 1)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                multipleOptAndReq(req1: 3, req2: 4)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                multipleOptAndReq(req1: 3, req2: 4, opt1: 5)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                multipleOptAndReq(req1: 3, req2: 4, opt1: 5, opt2: 6)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                multipleReqs(req2: 2)
              }
            }
            """,
            [
                TartifletteError(
                    message="Field < multipleReqs > argument < req1 > of type < Int! > is required, but it was not provided.",
                    locations=[
                        Location(line=4, column=17, line_end=4, column_end=38)
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
            {
              complicatedArgs {
                multipleReqs
              }
            }
            """,
            [
                TartifletteError(
                    message="Field < multipleReqs > argument < req1 > of type < Int! > is required, but it was not provided.",
                    locations=[
                        Location(line=4, column=17, line_end=4, column_end=29)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.2.1",
                        "tag": "required-arguments",
                        "details": "https://spec.graphql.org/June2018/#sec-Required-Arguments",
                    },
                ),
                TartifletteError(
                    message="Field < multipleReqs > argument < req2 > of type < Int! > is required, but it was not provided.",
                    locations=[
                        Location(line=4, column=17, line_end=4, column_end=29)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.2.1",
                        "tag": "required-arguments",
                        "details": "https://spec.graphql.org/June2018/#sec-Required-Arguments",
                    },
                ),
            ],
        ),
        (
            """
            {
              complicatedArgs {
                multipleReqs(req1: "one")
              }
            }
            """,
            [
                TartifletteError(
                    message="Field < multipleReqs > argument < req2 > of type < Int! > is required, but it was not provided.",
                    locations=[
                        Location(line=4, column=17, line_end=4, column_end=42)
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
            {
              dog @unknown
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
              dog @include {
                name @skip
              }
            }
            """,
            [
                TartifletteError(
                    message="Directive < @include > argument < if > of type < Boolean! > required, but it was not provided.",
                    locations=[
                        Location(line=3, column=19, line_end=3, column_end=27)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.2.1",
                        "tag": "required-arguments",
                        "details": "https://spec.graphql.org/June2018/#sec-Required-Arguments",
                    },
                ),
                TartifletteError(
                    message="Directive < @skip > argument < if > of type < Boolean! > required, but it was not provided.",
                    locations=[
                        Location(line=4, column=22, line_end=4, column_end=27)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.2.1",
                        "tag": "required-arguments",
                        "details": "https://spec.graphql.org/June2018/#sec-Required-Arguments",
                    },
                ),
            ],
        ),
    ],
)
async def test_provided_required_arguments(schema_stack, query, expected):
    assert_unordered_lists(
        validate_query(
            schema_stack.schema,
            parse_to_document(query),
            rules=[ProvidedRequiredArgumentsRule],
        ),
        expected,
    )
