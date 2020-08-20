import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.validation.rules import VariablesAreInputTypesRule
from tartiflette.validation.validate import validate_query
from tests.functional.utils import assert_unordered_lists


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="harness")
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query Foo($a: String, $b: [Boolean!]!, $c: ComplexInput) {
              field(a: $a, b: $b, c: $c)
            }
            """,
            [],
        ),
        (
            """
            query Foo($a: Dog, $b: [[CatOrDog!]]!, $c: Pet) {
              field(a: $a, b: $b, c: $c)
            }
            """,
            [
                TartifletteError(
                    message="Variable < a > cannot be non-input type < Dog >.",
                    locations=[
                        Location(line=2, column=27, line_end=2, column_end=30)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.2",
                        "tag": "variables-are-input-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Variables-Are-Input-Types",
                    },
                ),
                TartifletteError(
                    message="Variable < b > cannot be non-input type < [[CatOrDog!]]! >.",
                    locations=[
                        Location(line=2, column=36, line_end=2, column_end=50)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.2",
                        "tag": "variables-are-input-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Variables-Are-Input-Types",
                    },
                ),
                TartifletteError(
                    message="Variable < c > cannot be non-input type < Pet >.",
                    locations=[
                        Location(line=2, column=56, line_end=2, column_end=59)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.2",
                        "tag": "variables-are-input-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Variables-Are-Input-Types",
                    },
                ),
            ],
        ),
    ],
)
async def test_variables_are_input_types(schema_stack, query, expected):
    assert_unordered_lists(
        validate_query(
            schema_stack.schema,
            parse_to_document(query),
            rules=[VariablesAreInputTypesRule],
        ),
        expected,
    )
