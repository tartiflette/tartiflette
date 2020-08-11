import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.validation.rules import LoneAnonymousOperationRule
from tartiflette.validation.validate import validate_query
from tests.functional.utils import assert_unordered_lists


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(name="harness")
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            fragment fragA on Type {
              field
            }
            """,
            [],
        ),
        (
            """
            {
              field
            }
            """,
            [],
        ),
        (
            """
            query Foo {
              field
            }

            query Bar {
              field
            }
            """,
            [],
        ),
        (
            """
            fragment Foo on Type {
              field
            }
            {
              ...Foo
            }
            """,
            [],
        ),
        (
            """
            {
              fieldA
            }
            {
              fieldB
            }
            """,
            [
                TartifletteError(
                    message="This anonymous operation must be the only defined operation.",
                    locations=[
                        Location(line=2, column=13, line_end=4, column_end=14)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.2.2.1",
                        "tag": "lone-anonymous-operation",
                        "details": "https://spec.graphql.org/June2018/#sec-Lone-Anonymous-Operation",
                    },
                ),
                TartifletteError(
                    message="This anonymous operation must be the only defined operation.",
                    locations=[
                        Location(line=5, column=13, line_end=7, column_end=14)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.2.2.1",
                        "tag": "lone-anonymous-operation",
                        "details": "https://spec.graphql.org/June2018/#sec-Lone-Anonymous-Operation",
                    },
                ),
            ],
        ),
        (
            """
            {
              fieldA
            }
            mutation Foo {
              fieldB
            }
            """,
            [
                TartifletteError(
                    message="This anonymous operation must be the only defined operation.",
                    locations=[
                        Location(line=2, column=13, line_end=4, column_end=14)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.2.2.1",
                        "tag": "lone-anonymous-operation",
                        "details": "https://spec.graphql.org/June2018/#sec-Lone-Anonymous-Operation",
                    },
                )
            ],
        ),
        (
            """
            {
              fieldA
            }
            subscription Foo {
              fieldB
            }
            """,
            [
                TartifletteError(
                    message="This anonymous operation must be the only defined operation.",
                    locations=[
                        Location(line=2, column=13, line_end=4, column_end=14)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.2.2.1",
                        "tag": "lone-anonymous-operation",
                        "details": "https://spec.graphql.org/June2018/#sec-Lone-Anonymous-Operation",
                    },
                )
            ],
        ),
    ],
)
async def test_lone_anonymous_operation(engine, query, expected):
    assert_unordered_lists(
        validate_query(
            engine._schema,
            parse_to_document(query, engine._schema),
            rules=[LoneAnonymousOperationRule],
        ),
        expected,
    )
