import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.validation.rules import UniqueVariableNamesRule
from tartiflette.validation.validate import validate_query
from tests.functional.utils import assert_unordered_lists


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="harness")
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query A($x: Int, $y: String) { __typename }
            query B($x: String, $y: Int) { __typename }
            """,
            [],
        ),
        (
            """
            query A($x: Int, $x: Int, $x: String) { __typename }
            query B($x: String, $x: Int) { __typename }
            query C($x: Int, $x: Int) { __typename }
            """,
            [
                TartifletteError(
                    message="There can be only one variable named < $x >.",
                    locations=[
                        Location(line=2, column=21, line_end=2, column_end=23),
                        Location(line=2, column=30, line_end=2, column_end=32),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.1",
                        "tag": "variable-uniqueness",
                        "details": "https://spec.graphql.org/June2018/#sec-Variable-Uniqueness",
                    },
                ),
                TartifletteError(
                    message="There can be only one variable named < $x >.",
                    locations=[
                        Location(line=2, column=21, line_end=2, column_end=23),
                        Location(line=2, column=39, line_end=2, column_end=41),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.1",
                        "tag": "variable-uniqueness",
                        "details": "https://spec.graphql.org/June2018/#sec-Variable-Uniqueness",
                    },
                ),
                TartifletteError(
                    message="There can be only one variable named < $x >.",
                    locations=[
                        Location(line=3, column=21, line_end=3, column_end=23),
                        Location(line=3, column=33, line_end=3, column_end=35),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.1",
                        "tag": "variable-uniqueness",
                        "details": "https://spec.graphql.org/June2018/#sec-Variable-Uniqueness",
                    },
                ),
                TartifletteError(
                    message="There can be only one variable named < $x >.",
                    locations=[
                        Location(line=4, column=21, line_end=4, column_end=23),
                        Location(line=4, column=30, line_end=4, column_end=32),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.1",
                        "tag": "variable-uniqueness",
                        "details": "https://spec.graphql.org/June2018/#sec-Variable-Uniqueness",
                    },
                ),
            ],
        ),
    ],
)
async def test_unique_variable_names(schema_stack, query, expected):
    assert_unordered_lists(
        validate_query(
            schema_stack.schema,
            parse_to_document(query),
            rules=[UniqueVariableNamesRule],
        ),
        expected,
    )
