import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.validation.rules import NoFragmentCyclesRule
from tartiflette.validation.validate import validate_query
from tests.functional.utils import assert_unordered_lists


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="harness")
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            fragment fragA on Dog { ...fragB }
            fragment fragB on Dog { name }
            """,
            [],
        ),
        (
            """
            fragment fragA on Dog { ...fragB, ...fragB }
            fragment fragB on Dog { name }
            """,
            [],
        ),
        (
            """
            fragment fragA on Dog { ...fragB, ...fragC }
            fragment fragB on Dog { ...fragC }
            fragment fragC on Dog { name }
            """,
            [],
        ),
        (
            """
            fragment nameFragment on Pet {
              ... on Dog { name }
              ... on Cat { name }
            }

            fragment spreadsInAnon on Pet {
              ... on Dog { ...nameFragment }
              ... on Cat { ...nameFragment }
            }
            """,
            [],
        ),
        (
            """
            fragment nameFragment on Pet {
              ...UnknownFragment
            }
            """,
            [],
        ),
        (
            """
            fragment fragA on Human { relatives { ...fragA } },
            """,
            [
                TartifletteError(
                    message="Cannot spread fragment < fragA > within itself.",
                    locations=[
                        Location(line=2, column=51, line_end=2, column_end=59)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.2",
                        "tag": "fragment-spreads-must-not-form-cycles",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spreads-must-not-form-cycles",
                    },
                )
            ],
        ),
        (
            """
            fragment fragA on Dog { ...fragA }
            """,
            [
                TartifletteError(
                    message="Cannot spread fragment < fragA > within itself.",
                    locations=[
                        Location(line=2, column=37, line_end=2, column_end=45)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.2",
                        "tag": "fragment-spreads-must-not-form-cycles",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spreads-must-not-form-cycles",
                    },
                )
            ],
        ),
        (
            """
            fragment fragA on Pet {
              ... on Dog {
                ...fragA
              }
            }
            """,
            [
                TartifletteError(
                    message="Cannot spread fragment < fragA > within itself.",
                    locations=[
                        Location(line=4, column=17, line_end=4, column_end=25)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.2",
                        "tag": "fragment-spreads-must-not-form-cycles",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spreads-must-not-form-cycles",
                    },
                )
            ],
        ),
        (
            """
            fragment fragA on Dog { ...fragB }
            fragment fragB on Dog { ...fragA }
            """,
            [
                TartifletteError(
                    message="Cannot spread fragment < fragA > within itself via < fragB >.",
                    locations=[
                        Location(line=2, column=37, line_end=2, column_end=45),
                        Location(line=3, column=37, line_end=3, column_end=45),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.2",
                        "tag": "fragment-spreads-must-not-form-cycles",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spreads-must-not-form-cycles",
                    },
                )
            ],
        ),
        (
            """
            fragment fragB on Dog { ...fragA }
            fragment fragA on Dog { ...fragB }
            """,
            [
                TartifletteError(
                    message="Cannot spread fragment < fragB > within itself via < fragA >.",
                    locations=[
                        Location(line=2, column=37, line_end=2, column_end=45),
                        Location(line=3, column=37, line_end=3, column_end=45),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.2",
                        "tag": "fragment-spreads-must-not-form-cycles",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spreads-must-not-form-cycles",
                    },
                )
            ],
        ),
        (
            """
            fragment fragA on Pet {
              ... on Dog {
                ...fragB
              }
            }
            fragment fragB on Pet {
              ... on Dog {
                ...fragA
              }
            }
            """,
            [
                TartifletteError(
                    message="Cannot spread fragment < fragA > within itself via < fragB >.",
                    locations=[
                        Location(line=4, column=17, line_end=4, column_end=25),
                        Location(line=9, column=17, line_end=9, column_end=25),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.2",
                        "tag": "fragment-spreads-must-not-form-cycles",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spreads-must-not-form-cycles",
                    },
                )
            ],
        ),
        (
            """
            fragment fragA on Dog { ...fragB }
            fragment fragB on Dog { ...fragC }
            fragment fragC on Dog { ...fragO }
            fragment fragX on Dog { ...fragY }
            fragment fragY on Dog { ...fragZ }
            fragment fragZ on Dog { ...fragO }
            fragment fragO on Dog { ...fragP }
            fragment fragP on Dog { ...fragA, ...fragX }
            """,
            [
                TartifletteError(
                    message="Cannot spread fragment < fragA > within itself via < fragB >, < fragC >, < fragO >, < fragP >.",
                    locations=[
                        Location(line=2, column=37, line_end=2, column_end=45),
                        Location(line=3, column=37, line_end=3, column_end=45),
                        Location(line=4, column=37, line_end=4, column_end=45),
                        Location(line=8, column=37, line_end=8, column_end=45),
                        Location(line=9, column=37, line_end=9, column_end=45),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.2",
                        "tag": "fragment-spreads-must-not-form-cycles",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spreads-must-not-form-cycles",
                    },
                ),
                TartifletteError(
                    message="Cannot spread fragment < fragO > within itself via < fragP >, < fragX >, < fragY >, < fragZ >.",
                    locations=[
                        Location(line=8, column=37, line_end=8, column_end=45),
                        Location(line=9, column=47, line_end=9, column_end=55),
                        Location(line=5, column=37, line_end=5, column_end=45),
                        Location(line=6, column=37, line_end=6, column_end=45),
                        Location(line=7, column=37, line_end=7, column_end=45),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.2",
                        "tag": "fragment-spreads-must-not-form-cycles",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spreads-must-not-form-cycles",
                    },
                ),
            ],
        ),
        (
            """
            fragment fragA on Dog { ...fragB, ...fragC }
            fragment fragB on Dog { ...fragA }
            fragment fragC on Dog { ...fragA }
            """,
            [
                TartifletteError(
                    message="Cannot spread fragment < fragA > within itself via < fragB >.",
                    locations=[
                        Location(line=2, column=37, line_end=2, column_end=45),
                        Location(line=3, column=37, line_end=3, column_end=45),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.2",
                        "tag": "fragment-spreads-must-not-form-cycles",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spreads-must-not-form-cycles",
                    },
                ),
                TartifletteError(
                    message="Cannot spread fragment < fragA > within itself via < fragC >.",
                    locations=[
                        Location(line=2, column=47, line_end=2, column_end=55),
                        Location(line=4, column=37, line_end=4, column_end=45),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.2",
                        "tag": "fragment-spreads-must-not-form-cycles",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spreads-must-not-form-cycles",
                    },
                ),
            ],
        ),
        (
            """
            fragment fragA on Dog { ...fragC }
            fragment fragB on Dog { ...fragC }
            fragment fragC on Dog { ...fragA, ...fragB }
            """,
            [
                TartifletteError(
                    message="Cannot spread fragment < fragA > within itself via < fragC >.",
                    locations=[
                        Location(line=2, column=37, line_end=2, column_end=45),
                        Location(line=4, column=37, line_end=4, column_end=45),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.2",
                        "tag": "fragment-spreads-must-not-form-cycles",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spreads-must-not-form-cycles",
                    },
                ),
                TartifletteError(
                    message="Cannot spread fragment < fragC > within itself via < fragB >.",
                    locations=[
                        Location(line=4, column=47, line_end=4, column_end=55),
                        Location(line=3, column=37, line_end=3, column_end=45),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.2",
                        "tag": "fragment-spreads-must-not-form-cycles",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spreads-must-not-form-cycles",
                    },
                ),
            ],
        ),
        (
            """
            fragment fragA on Dog { ...fragB }
            fragment fragB on Dog { ...fragB, ...fragC }
            fragment fragC on Dog { ...fragA, ...fragB }
            """,
            [
                TartifletteError(
                    message="Cannot spread fragment < fragB > within itself.",
                    locations=[
                        Location(line=3, column=37, line_end=3, column_end=45)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.2",
                        "tag": "fragment-spreads-must-not-form-cycles",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spreads-must-not-form-cycles",
                    },
                ),
                TartifletteError(
                    message="Cannot spread fragment < fragA > within itself via < fragB >, < fragC >.",
                    locations=[
                        Location(line=2, column=37, line_end=2, column_end=45),
                        Location(line=3, column=47, line_end=3, column_end=55),
                        Location(line=4, column=37, line_end=4, column_end=45),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.2",
                        "tag": "fragment-spreads-must-not-form-cycles",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spreads-must-not-form-cycles",
                    },
                ),
                TartifletteError(
                    message="Cannot spread fragment < fragB > within itself via < fragC >.",
                    locations=[
                        Location(line=3, column=47, line_end=3, column_end=55),
                        Location(line=4, column=47, line_end=4, column_end=55),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.2",
                        "tag": "fragment-spreads-must-not-form-cycles",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spreads-must-not-form-cycles",
                    },
                ),
            ],
        ),
    ],
)
async def test_no_fragment_cycles(schema_stack, query, expected):
    assert_unordered_lists(
        validate_query(
            schema_stack.schema,
            parse_to_document(query),
            rules=[NoFragmentCyclesRule],
        ),
        expected,
    )
