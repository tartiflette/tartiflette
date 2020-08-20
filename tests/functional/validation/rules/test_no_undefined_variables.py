import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.validation.rules import NoUndefinedVariablesRule
from tartiflette.validation.validate import validate_query
from tests.functional.utils import assert_unordered_lists


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="harness")
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query Foo($a: String, $b: String, $c: String) {
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
            query Foo($a: String) {
              ...FragA
            }
            query Bar($a: String) {
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
            query Foo($a: String, $b: String, $c: String) {
              field(a: $a, b: $b, c: $c, d: $d)
            }
            """,
            [
                TartifletteError(
                    message="Variable < $d > is not defined by operation < Foo >.",
                    locations=[
                        Location(line=3, column=45, line_end=3, column_end=47),
                        Location(line=2, column=13, line_end=4, column_end=14),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.3",
                        "tag": "all-variable-uses-defined",
                        "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                    },
                )
            ],
        ),
        (
            """
            {
              field(a: $a)
            }
            """,
            [
                TartifletteError(
                    message="Variable < $a > is not defined.",
                    locations=[
                        Location(line=3, column=24, line_end=3, column_end=26),
                        Location(line=2, column=13, line_end=4, column_end=14),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.3",
                        "tag": "all-variable-uses-defined",
                        "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                    },
                )
            ],
        ),
        (
            """
            query Foo($b: String) {
              field(a: $a, b: $b, c: $c)
            }
            """,
            [
                TartifletteError(
                    message="Variable < $a > is not defined by operation < Foo >.",
                    locations=[
                        Location(line=3, column=24, line_end=3, column_end=26),
                        Location(line=2, column=13, line_end=4, column_end=14),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.3",
                        "tag": "all-variable-uses-defined",
                        "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                    },
                ),
                TartifletteError(
                    message="Variable < $c > is not defined by operation < Foo >.",
                    locations=[
                        Location(line=3, column=38, line_end=3, column_end=40),
                        Location(line=2, column=13, line_end=4, column_end=14),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.3",
                        "tag": "all-variable-uses-defined",
                        "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                    },
                ),
            ],
        ),
        (
            """
            fragment FragA on Type {
              field(a: $a)
            }
            {
              ...FragA
            }
            """,
            [
                TartifletteError(
                    message="Variable < $a > is not defined.",
                    locations=[
                        Location(line=3, column=24, line_end=3, column_end=26),
                        Location(line=5, column=13, line_end=7, column_end=14),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.3",
                        "tag": "all-variable-uses-defined",
                        "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                    },
                )
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
              field(c: $c)
            }
            query Foo($a: String, $b: String) {
              ...FragA
            }
            """,
            [
                TartifletteError(
                    message="Variable < $c > is not defined by operation < Foo >.",
                    locations=[
                        Location(
                            line=13, column=24, line_end=13, column_end=26
                        ),
                        Location(
                            line=15, column=13, line_end=17, column_end=14
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.3",
                        "tag": "all-variable-uses-defined",
                        "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                    },
                )
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
              field(c: $c)
            }
            query Foo($b: String) {
              ...FragA
            }
            """,
            [
                TartifletteError(
                    message="Variable < $a > is not defined by operation < Foo >.",
                    locations=[
                        Location(line=3, column=24, line_end=3, column_end=26),
                        Location(
                            line=15, column=13, line_end=17, column_end=14
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.3",
                        "tag": "all-variable-uses-defined",
                        "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                    },
                ),
                TartifletteError(
                    message="Variable < $c > is not defined by operation < Foo >.",
                    locations=[
                        Location(
                            line=13, column=24, line_end=13, column_end=26
                        ),
                        Location(
                            line=15, column=13, line_end=17, column_end=14
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.3",
                        "tag": "all-variable-uses-defined",
                        "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                    },
                ),
            ],
        ),
        (
            """
            fragment FragAB on Type {
              field(a: $a, b: $b)
            }
            query Foo($a: String) {
              ...FragAB
            }
            query Bar($a: String) {
              ...FragAB
            }
            """,
            [
                TartifletteError(
                    message="Variable < $b > is not defined by operation < Foo >.",
                    locations=[
                        Location(line=3, column=31, line_end=3, column_end=33),
                        Location(line=5, column=13, line_end=7, column_end=14),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.3",
                        "tag": "all-variable-uses-defined",
                        "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                    },
                ),
                TartifletteError(
                    message="Variable < $b > is not defined by operation < Bar >.",
                    locations=[
                        Location(line=3, column=31, line_end=3, column_end=33),
                        Location(
                            line=8, column=13, line_end=10, column_end=14
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.3",
                        "tag": "all-variable-uses-defined",
                        "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                    },
                ),
            ],
        ),
        (
            """
            fragment FragAB on Type {
              field(a: $a, b: $b)
            }
            query Foo($b: String) {
              ...FragAB
            }
            query Bar($a: String) {
              ...FragAB
            }
            """,
            [
                TartifletteError(
                    message="Variable < $a > is not defined by operation < Foo >.",
                    locations=[
                        Location(line=3, column=24, line_end=3, column_end=26),
                        Location(line=5, column=13, line_end=7, column_end=14),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.3",
                        "tag": "all-variable-uses-defined",
                        "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                    },
                ),
                TartifletteError(
                    message="Variable < $b > is not defined by operation < Bar >.",
                    locations=[
                        Location(line=3, column=31, line_end=3, column_end=33),
                        Location(
                            line=8, column=13, line_end=10, column_end=14
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.3",
                        "tag": "all-variable-uses-defined",
                        "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
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
            query Bar($a: String) {
              ...FragB
            }
            """,
            [
                TartifletteError(
                    message="Variable < $a > is not defined by operation < Foo >.",
                    locations=[
                        Location(line=3, column=24, line_end=3, column_end=26),
                        Location(
                            line=8, column=13, line_end=10, column_end=14
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.3",
                        "tag": "all-variable-uses-defined",
                        "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                    },
                ),
                TartifletteError(
                    message="Variable < $b > is not defined by operation < Bar >.",
                    locations=[
                        Location(line=6, column=24, line_end=6, column_end=26),
                        Location(
                            line=11, column=13, line_end=13, column_end=14
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.3",
                        "tag": "all-variable-uses-defined",
                        "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                    },
                ),
            ],
        ),
        (
            """
            fragment FragAB on Type {
              field1(a: $a, b: $b)
              ...FragC
              field3(a: $a, b: $b)
            }
            fragment FragC on Type {
              field2(c: $c)
            }
            query Foo($b: String) {
              ...FragAB
            }
            query Bar($a: String) {
              ...FragAB
            }
            """,
            [
                TartifletteError(
                    message="Variable < $a > is not defined by operation < Foo >.",
                    locations=[
                        Location(line=3, column=25, line_end=3, column_end=27),
                        Location(
                            line=10, column=13, line_end=12, column_end=14
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.3",
                        "tag": "all-variable-uses-defined",
                        "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                    },
                ),
                TartifletteError(
                    message="Variable < $a > is not defined by operation < Foo >.",
                    locations=[
                        Location(line=5, column=25, line_end=5, column_end=27),
                        Location(
                            line=10, column=13, line_end=12, column_end=14
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.3",
                        "tag": "all-variable-uses-defined",
                        "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                    },
                ),
                TartifletteError(
                    message="Variable < $c > is not defined by operation < Foo >.",
                    locations=[
                        Location(line=8, column=25, line_end=8, column_end=27),
                        Location(
                            line=10, column=13, line_end=12, column_end=14
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.3",
                        "tag": "all-variable-uses-defined",
                        "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                    },
                ),
                TartifletteError(
                    message="Variable < $b > is not defined by operation < Bar >.",
                    locations=[
                        Location(line=3, column=32, line_end=3, column_end=34),
                        Location(
                            line=13, column=13, line_end=15, column_end=14
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.3",
                        "tag": "all-variable-uses-defined",
                        "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                    },
                ),
                TartifletteError(
                    message="Variable < $b > is not defined by operation < Bar >.",
                    locations=[
                        Location(line=5, column=32, line_end=5, column_end=34),
                        Location(
                            line=13, column=13, line_end=15, column_end=14
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.3",
                        "tag": "all-variable-uses-defined",
                        "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                    },
                ),
                TartifletteError(
                    message="Variable < $c > is not defined by operation < Bar >.",
                    locations=[
                        Location(line=8, column=25, line_end=8, column_end=27),
                        Location(
                            line=13, column=13, line_end=15, column_end=14
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.3",
                        "tag": "all-variable-uses-defined",
                        "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                    },
                ),
            ],
        ),
    ],
)
async def test_no_undefined_variables(schema_stack, query, expected):
    assert_unordered_lists(
        validate_query(
            schema_stack.schema,
            parse_to_document(query),
            rules=[NoUndefinedVariablesRule],
        ),
        expected,
    )
