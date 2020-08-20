import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.validation.rules import UniqueFragmentNamesRule
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
              field
            }
            """,
            [],
        ),
        (
            """
            {
              ...fragA
            }

            fragment fragA on Type {
              field
            }
            """,
            [],
        ),
        (
            """
            {
              ...fragA
              ...fragB
              ...fragC
            }
            fragment fragA on Type {
              fieldA
            }
            fragment fragB on Type {
              fieldB
            }
            fragment fragC on Type {
              fieldC
            }
            """,
            [],
        ),
        (
            """
            {
              ...on Type {
                fieldA
              }
              ...on Type {
                fieldB
              }
            }
            """,
            [],
        ),
        (
            """
            query Foo {
              ...Foo
            }
            fragment Foo on Type {
              field
            }
            """,
            [],
        ),
        (
            """
            {
              ...fragA
            }
            fragment fragA on Type {
              fieldA
            }
            fragment fragA on Type {
              fieldB
            }
            """,
            [
                TartifletteError(
                    message="There can be only one fragment named < fragA >.",
                    locations=[
                        Location(line=5, column=22, line_end=5, column_end=27),
                        Location(line=8, column=22, line_end=8, column_end=27),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.1.1",
                        "tag": "fragment-name-uniqueness",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-Name-Uniqueness",
                    },
                )
            ],
        ),
        (
            """
            fragment fragA on Type {
              fieldA
            }
            fragment fragA on Type {
              fieldB
            }
            """,
            [
                TartifletteError(
                    message="There can be only one fragment named < fragA >.",
                    locations=[
                        Location(line=2, column=22, line_end=2, column_end=27),
                        Location(line=5, column=22, line_end=5, column_end=27),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.1.1",
                        "tag": "fragment-name-uniqueness",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-Name-Uniqueness",
                    },
                )
            ],
        ),
    ],
)
async def test_unique_fragment_names(schema_stack, query, expected):
    assert_unordered_lists(
        validate_query(
            schema_stack.schema,
            parse_to_document(query),
            rules=[UniqueFragmentNamesRule],
        ),
        expected,
    )
