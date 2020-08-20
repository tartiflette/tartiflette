import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.validation.rules import NoUnusedVariablesRule
from tartiflette.validation.validate import validate_query
from tests.functional.utils import assert_unordered_lists


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="harness")
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query ($a: String, $b: String, $c: String) {
              field(a: $a, b: $b, c: $c)
            }
            """,
            [],
        ),
        (
            """
            query Foo($a: String, $b: String, $c: String) {
              field(a: $a) {
                field(b: $b) {
                  field(c: $c)
                }
              }
            }
            """,
            [],
        ),
        (
            """
            query Foo($a: String, $b: String, $c: String) {
              ... on Type {
                field(a: $a) {
                  field(b: $b) {
                    ... on Type {
                      field(c: $c)
                    }
                  }
                }
              }
            }
            """,
            [],
        ),
        (
            """
            fragment FragA on Type {
              field(a: $a) {
                ...FragB
              }
            }
            fragment FragB on Type {
              field(b: $b) {
                ...FragC
              }
            }
            fragment FragC on Type {
              field(c: $c)
            }
            query Foo($a: String, $b: String, $c: String) {
              ...FragA
            }
            """,
            [],
        ),
        (
            """
            fragment FragA on Type {
              field(a: $a)
            }
            fragment FragB on Type {
              field(b: $b)
            }
            query Foo($a: String) {
              ...FragA
            }
            query Bar($b: String) {
              ...FragB
            }
            """,
            [],
        ),
        (
            """
            fragment FragA on Type {
              field(a: $a) {
                ...FragA
              }
            }
            query Foo($a: String) {
              ...FragA
            }
            """,
            [],
        ),
        (
            """
            query ($a: String, $b: String, $c: String) {
              field(a: $a, b: $b)
            }
            """,
            [
                TartifletteError(
                    message="Variable < $c > is never used.",
                    locations=[
                        Location(line=2, column=44, line_end=2, column_end=54)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.4",
                        "tag": "all-variables-used",
                        "details": "https://spec.graphql.org/June2018/#sec-All-Variables-Used",
                    },
                )
            ],
        ),
        (
            """
            query Foo($a: String, $b: String, $c: String) {
              field(b: $b)
            }
            """,
            [
                TartifletteError(
                    message="Variable < $a > is never used in operation < Foo >.",
                    locations=[
                        Location(line=2, column=23, line_end=2, column_end=33)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.4",
                        "tag": "all-variables-used",
                        "details": "https://spec.graphql.org/June2018/#sec-All-Variables-Used",
                    },
                ),
                TartifletteError(
                    message="Variable < $c > is never used in operation < Foo >.",
                    locations=[
                        Location(line=2, column=47, line_end=2, column_end=57)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.4",
                        "tag": "all-variables-used",
                        "details": "https://spec.graphql.org/June2018/#sec-All-Variables-Used",
                    },
                ),
            ],
        ),
        (
            """
            fragment FragA on Type {
              field(a: $a) {
                ...FragB
              }
            }
            fragment FragB on Type {
              field(b: $b) {
                ...FragC
              }
            }
            fragment FragC on Type {
              field
            }
            query Foo($a: String, $b: String, $c: String) {
              ...FragA
            }
            """,
            [
                TartifletteError(
                    message="Variable < $c > is never used in operation < Foo >.",
                    locations=[
                        Location(
                            line=15, column=47, line_end=15, column_end=57
                        )
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.4",
                        "tag": "all-variables-used",
                        "details": "https://spec.graphql.org/June2018/#sec-All-Variables-Used",
                    },
                )
            ],
        ),
        (
            """
            fragment FragA on Type {
              field {
                ...FragB
              }
            }
            fragment FragB on Type {
              field(b: $b) {
                ...FragC
              }
            }
            fragment FragC on Type {
              field
            }
            query Foo($a: String, $b: String, $c: String) {
              ...FragA
            }
            """,
            [
                TartifletteError(
                    message="Variable < $a > is never used in operation < Foo >.",
                    locations=[
                        Location(
                            line=15, column=23, line_end=15, column_end=33
                        )
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.4",
                        "tag": "all-variables-used",
                        "details": "https://spec.graphql.org/June2018/#sec-All-Variables-Used",
                    },
                ),
                TartifletteError(
                    message="Variable < $c > is never used in operation < Foo >.",
                    locations=[
                        Location(
                            line=15, column=47, line_end=15, column_end=57
                        )
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.4",
                        "tag": "all-variables-used",
                        "details": "https://spec.graphql.org/June2018/#sec-All-Variables-Used",
                    },
                ),
            ],
        ),
        (
            """
            fragment FragA on Type {
              field(a: $a)
            }
            fragment FragB on Type {
              field(b: $b)
            }
            query Foo($b: String) {
              ...FragA
            }
            """,
            [
                TartifletteError(
                    message="Variable < $b > is never used in operation < Foo >.",
                    locations=[
                        Location(line=8, column=23, line_end=8, column_end=33)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.4",
                        "tag": "all-variables-used",
                        "details": "https://spec.graphql.org/June2018/#sec-All-Variables-Used",
                    },
                )
            ],
        ),
        (
            """
            fragment FragA on Type {
              field(a: $a)
            }
            fragment FragB on Type {
              field(b: $b)
            }
            query Foo($b: String) {
              ...FragA
            }
            query Bar($a: String) {
              ...FragB
            }
            """,
            [
                TartifletteError(
                    message="Variable < $b > is never used in operation < Foo >.",
                    locations=[
                        Location(line=8, column=23, line_end=8, column_end=33)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.4",
                        "tag": "all-variables-used",
                        "details": "https://spec.graphql.org/June2018/#sec-All-Variables-Used",
                    },
                ),
                TartifletteError(
                    message="Variable < $a > is never used in operation < Bar >.",
                    locations=[
                        Location(
                            line=11, column=23, line_end=11, column_end=33
                        )
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.4",
                        "tag": "all-variables-used",
                        "details": "https://spec.graphql.org/June2018/#sec-All-Variables-Used",
                    },
                ),
            ],
        ),
    ],
)
async def test_no_unused_variables(schema_stack, query, expected):
    assert_unordered_lists(
        validate_query(
            schema_stack.schema,
            parse_to_document(query),
            rules=[NoUnusedVariablesRule],
        ),
        expected,
    )
