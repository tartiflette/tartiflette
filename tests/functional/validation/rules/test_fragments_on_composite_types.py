import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.validation.rules import FragmentsOnCompositeTypesRule
from tartiflette.validation.validate import validate_query
from tests.functional.utils import assert_unordered_lists


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="harness")
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            fragment validFragment on Dog {
              barks
            }
            """,
            [],
        ),
        (
            """
            {
              ... on Dog {
                barks
              }
            }
            """,
            [],
        ),
        (
            """
            fragment validFragment on Pet {
              name
            }
            """,
            [],
        ),
        (
            """
            {
              ... on Pet {
                name
              }
            }
            """,
            [],
        ),
        (
            """
            fragment validFragment on Pet {
              ... on Dog {
                barks
              }
            }
            """,
            [],
        ),
        (
            """
            {
              ... on Pet {
                ... on Dog {
                  barks
                }
              }
            }
            """,
            [],
        ),
        (
            """
            fragment validFragment on Mammal {
              ... on Canine {
                name
              }
            }
            """,
            [],
        ),
        (
            """
            {
              ... on Mammal {
                ... on Canine {
                  name
                }
              }
            }
            """,
            [],
        ),
        (
            """
            fragment validFragment on Pet {
              ... {
                name
              }
            }
            """,
            [],
        ),
        (
            """
            fragment validFragment on CatOrDog {
              __typename
            }
            """,
            [],
        ),
        (
            """
            {
              ... on CatOrDog {
                __typename
              }
            }
            """,
            [],
        ),
        (
            """
            fragment scalarFragment on Boolean {
              bad
            }
            """,
            [
                TartifletteError(
                    message="Fragment < scalarFragment > cannot condition on non composite type < Boolean >.",
                    locations=[
                        Location(line=2, column=40, line_end=2, column_end=47)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.1.3",
                        "tag": "fragments-on-composite-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragments-On-Composite-Types",
                    },
                )
            ],
        ),
        (
            """
            {
              ... on Boolean {
                bad
              }
            }
            """,
            [
                TartifletteError(
                    message="Fragment cannot condition on non composite type < Boolean >.",
                    locations=[
                        Location(line=3, column=22, line_end=3, column_end=29)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.1.3",
                        "tag": "fragments-on-composite-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragments-On-Composite-Types",
                    },
                )
            ],
        ),
        (
            """
            fragment scalarFragment on FurColor {
              bad
            }
            """,
            [
                TartifletteError(
                    message="Fragment < scalarFragment > cannot condition on non composite type < FurColor >.",
                    locations=[
                        Location(line=2, column=40, line_end=2, column_end=48)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.1.3",
                        "tag": "fragments-on-composite-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragments-On-Composite-Types",
                    },
                )
            ],
        ),
        (
            """
            {
              ... on FurColor {
                bad
              }
            }
            """,
            [
                TartifletteError(
                    message="Fragment cannot condition on non composite type < FurColor >.",
                    locations=[
                        Location(line=3, column=22, line_end=3, column_end=30)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.1.3",
                        "tag": "fragments-on-composite-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragments-On-Composite-Types",
                    },
                )
            ],
        ),
        (
            """
            fragment inputFragment on ComplexInput {
              stringField
            }
            """,
            [
                TartifletteError(
                    message="Fragment < inputFragment > cannot condition on non composite type < ComplexInput >.",
                    locations=[
                        Location(line=2, column=39, line_end=2, column_end=51)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.1.3",
                        "tag": "fragments-on-composite-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragments-On-Composite-Types",
                    },
                )
            ],
        ),
        (
            """
            {
              ... on ComplexInput {
                stringField
              }
            }
            """,
            [
                TartifletteError(
                    message="Fragment cannot condition on non composite type < ComplexInput >.",
                    locations=[
                        Location(line=3, column=22, line_end=3, column_end=34)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.1.3",
                        "tag": "fragments-on-composite-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragments-On-Composite-Types",
                    },
                )
            ],
        ),
        (
            """
            fragment invalidFragment on Pet {
              ... on String {
                barks
              }
            }
            """,
            [
                TartifletteError(
                    message="Fragment cannot condition on non composite type < String >.",
                    locations=[
                        Location(line=3, column=22, line_end=3, column_end=28)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.1.3",
                        "tag": "fragments-on-composite-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragments-On-Composite-Types",
                    },
                )
            ],
        ),
        (
            """
            {
              ... on Pet {
                ... on String {
                  barks
                }
              }
            }
            """,
            [
                TartifletteError(
                    message="Fragment cannot condition on non composite type < String >.",
                    locations=[
                        Location(line=4, column=24, line_end=4, column_end=30)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.1.3",
                        "tag": "fragments-on-composite-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragments-On-Composite-Types",
                    },
                )
            ],
        ),
    ],
)
async def test_fragments_on_composite_types(schema_stack, query, expected):
    assert_unordered_lists(
        validate_query(
            schema_stack.schema,
            parse_to_document(query),
            rules=[FragmentsOnCompositeTypesRule],
        ),
        expected,
    )
