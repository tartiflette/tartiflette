import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.validation.rules import KnownArgumentNamesRule
from tartiflette.validation.validate import validate_query
from tests.functional.utils import assert_unordered_lists


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(name="harness")
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            fragment argOnRequiredArg on Dog {
              doesKnowCommand(dogCommand: SIT)
            }
            """,
            [],
        ),
        (
            """
            fragment multipleArgs on ComplicatedArgs {
              multipleReqs(req1: 1, req2: 2)
            }
            """,
            [],
        ),
        (
            """
            fragment argOnUnknownField on Dog {
              unknownField(unknownArg: SIT)
            }
            """,
            [],
        ),
        (
            """
            fragment multipleArgsReverseOrder on ComplicatedArgs {
              multipleReqs(req2: 2, req1: 1)
            }
            """,
            [],
        ),
        (
            """
            fragment noArgOnOptionalArg on Dog {
              isHouseTrained
            }
            """,
            [],
        ),
        (
            """
            {
              dog {
                doesKnowCommand(dogCommand: SIT)
              }
              human {
                pet {
                  ... on Dog {
                    doesKnowCommand(dogCommand: SIT)
                  }
                }
              }
            }
            """,
            [],
        ),
        (
            """
            {
              dog @skip(if: true)
            }
            """,
            [],
        ),
        (
            """
            {
              dog @skip(unless: true)
            }
            """,
            [
                TartifletteError(
                    message="Unknown argument < unless > on directive < @skip >.",
                    locations=[
                        Location(line=3, column=25, line_end=3, column_end=37)
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
            {
              dog @onField
            }
            """,
            [],
        ),
        (
            """
            {
              dog @onField(if: true)
            }
            """,
            [
                TartifletteError(
                    message="Unknown argument < if > on directive < @onField >.",
                    locations=[
                        Location(line=3, column=28, line_end=3, column_end=36)
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
            {
              dog @skip(iff: true)
            }
            """,
            [
                TartifletteError(
                    message="Unknown argument < iff > on directive < @skip >. Did you mean if?",
                    locations=[
                        Location(line=3, column=25, line_end=3, column_end=34)
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
            fragment invalidArgName on Dog {
              doesKnowCommand(unknown: true)
            }
            """,
            [
                TartifletteError(
                    message="Unknown argument < unknown > on field < Dog.doesKnowCommand >.",
                    locations=[
                        Location(line=3, column=31, line_end=3, column_end=44)
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
            fragment invalidArgName on Dog {
              doesKnowCommand(DogCommand: true)
            }
            """,
            [
                TartifletteError(
                    message="Unknown argument < DogCommand > on field < Dog.doesKnowCommand >. Did you mean dogCommand?",
                    locations=[
                        Location(line=3, column=31, line_end=3, column_end=47)
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
            fragment oneGoodArgOneInvalidArg on Dog {
              doesKnowCommand(whoKnows: 1, dogCommand: SIT, unknown: true)
            }
            """,
            [
                TartifletteError(
                    message="Unknown argument < whoKnows > on field < Dog.doesKnowCommand >.",
                    locations=[
                        Location(line=3, column=31, line_end=3, column_end=42)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
                    },
                ),
                TartifletteError(
                    message="Unknown argument < unknown > on field < Dog.doesKnowCommand >.",
                    locations=[
                        Location(line=3, column=61, line_end=3, column_end=74)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
                    },
                ),
            ],
        ),
        (
            """
            {
              dog {
                doesKnowCommand(unknown: true)
              }
              human {
                pet {
                  ... on Dog {
                    doesKnowCommand(unknown: true)
                  }
                }
              }
            }
            """,
            [
                TartifletteError(
                    message="Unknown argument < unknown > on field < Dog.doesKnowCommand >.",
                    locations=[
                        Location(line=4, column=33, line_end=4, column_end=46)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
                    },
                ),
                TartifletteError(
                    message="Unknown argument < unknown > on field < Dog.doesKnowCommand >.",
                    locations=[
                        Location(line=9, column=37, line_end=9, column_end=50)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
                    },
                ),
            ],
        ),
    ],
)
async def test_known_argument_names(engine, query, expected):
    assert_unordered_lists(
        validate_query(
            engine._schema,
            parse_to_document(query, engine._schema),
            rules=[KnownArgumentNamesRule],
        ),
        expected,
    )
