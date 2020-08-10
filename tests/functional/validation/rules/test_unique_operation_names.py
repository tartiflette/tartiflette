import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.validation.rules import UniqueOperationNamesRule
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
            query Foo {
              field
            }

            mutation Bar {
              field
            }

            subscription Baz {
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
            query Foo {
              ...Foo
            }
            """,
            [],
        ),
        (
            """
            query Foo {
              fieldA
            }
            query Foo {
              fieldB
            }
            """,
            [
                TartifletteError(
                    message="There can be only one operation named < Foo >.",
                    locations=[
                        Location(line=2, column=19, line_end=2, column_end=22),
                        Location(line=5, column=19, line_end=5, column_end=22),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.2.1.1",
                        "tag": "operation-name-uniqueness",
                        "details": "https://spec.graphql.org/June2018/#sec-Operation-Name-Uniqueness",
                    },
                )
            ],
        ),
        (
            """
            query Foo {
              fieldA
            }
            mutation Foo {
              fieldB
            }
            """,
            [
                TartifletteError(
                    message="There can be only one operation named < Foo >.",
                    locations=[
                        Location(line=2, column=19, line_end=2, column_end=22),
                        Location(line=5, column=22, line_end=5, column_end=25),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.2.1.1",
                        "tag": "operation-name-uniqueness",
                        "details": "https://spec.graphql.org/June2018/#sec-Operation-Name-Uniqueness",
                    },
                )
            ],
        ),
        (
            """
            query Foo {
              fieldA
            }
            subscription Foo {
              fieldB
            }
            """,
            [
                TartifletteError(
                    message="There can be only one operation named < Foo >.",
                    locations=[
                        Location(line=2, column=19, line_end=2, column_end=22),
                        Location(line=5, column=26, line_end=5, column_end=29),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.2.1.1",
                        "tag": "operation-name-uniqueness",
                        "details": "https://spec.graphql.org/June2018/#sec-Operation-Name-Uniqueness",
                    },
                )
            ],
        ),
        (
            """
            query Foo {
              fieldA
            }
            mutation Foo {
              fieldB
            }
            subscription Foo {
              fieldC
            }
            """,
            [
                TartifletteError(
                    message="There can be only one operation named < Foo >.",
                    locations=[
                        Location(line=2, column=19, line_end=2, column_end=22),
                        Location(line=5, column=22, line_end=5, column_end=25),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.2.1.1",
                        "tag": "operation-name-uniqueness",
                        "details": "https://spec.graphql.org/June2018/#sec-Operation-Name-Uniqueness",
                    },
                ),
                TartifletteError(
                    message="There can be only one operation named < Foo >.",
                    locations=[
                        Location(line=2, column=19, line_end=2, column_end=22),
                        Location(line=8, column=26, line_end=8, column_end=29),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.2.1.1",
                        "tag": "operation-name-uniqueness",
                        "details": "https://spec.graphql.org/June2018/#sec-Operation-Name-Uniqueness",
                    },
                ),
            ],
        ),
    ],
)
async def test_unique_operation_names(engine, query, expected):
    assert_unordered_lists(
        validate_query(
            engine._schema,
            parse_to_document(query, engine._schema),
            rules=[UniqueOperationNamesRule],
        ),
        expected,
    )
