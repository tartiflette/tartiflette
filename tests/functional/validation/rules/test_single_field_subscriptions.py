import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.validation.rules import SingleFieldSubscriptionsRule
from tartiflette.validation.validate import validate_query
from tests.functional.utils import assert_unordered_lists


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(name="harness")
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            subscription ImportantEmails {
              importantEmails
            }
            """,
            [],
        ),
        (
            """
            subscription ImportantEmails {
              importantEmails
              notImportantEmails
            }
            """,
            [
                TartifletteError(
                    message="Subscription < ImportantEmails > must select only one top level field.",
                    locations=[
                        Location(line=4, column=15, line_end=4, column_end=33)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.2.3.1",
                        "tag": "single-root-field",
                        "details": "https://spec.graphql.org/June2018/#sec-Single-root-field",
                    },
                )
            ],
        ),
        (
            """
            subscription ImportantEmails {
              importantEmails
              __typename
            }
            """,
            [
                TartifletteError(
                    message="Subscription < ImportantEmails > must select only one top level field.",
                    locations=[
                        Location(line=4, column=15, line_end=4, column_end=25)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.2.3.1",
                        "tag": "single-root-field",
                        "details": "https://spec.graphql.org/June2018/#sec-Single-root-field",
                    },
                )
            ],
        ),
        (
            """
            subscription ImportantEmails {
              importantEmails
              notImportantEmails
              spamEmails
            }
            """,
            [
                TartifletteError(
                    message="Subscription < ImportantEmails > must select only one top level field.",
                    locations=[
                        Location(line=4, column=15, line_end=4, column_end=33),
                        Location(line=5, column=15, line_end=5, column_end=25),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.2.3.1",
                        "tag": "single-root-field",
                        "details": "https://spec.graphql.org/June2018/#sec-Single-root-field",
                    },
                )
            ],
        ),
        (
            """
            subscription {
              importantEmails
              notImportantEmails
            }
            """,
            [
                TartifletteError(
                    message="Anonymous Subscription must select only one top level field.",
                    locations=[
                        Location(line=4, column=15, line_end=4, column_end=33)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.2.3.1",
                        "tag": "single-root-field",
                        "details": "https://spec.graphql.org/June2018/#sec-Single-root-field",
                    },
                )
            ],
        ),
    ],
)
async def test_single_field_subscriptions(engine, query, expected):
    assert_unordered_lists(
        validate_query(
            engine._schema,
            parse_to_document(query, engine._schema),
            rules=[SingleFieldSubscriptionsRule],
        ),
        expected,
    )
