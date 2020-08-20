import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.language.parsers.libgraphqlparser import (
    parse_to_document as parse_query_to_document,
)
from tartiflette.validation.rules import UniqueInputFieldNamesRule
from tartiflette.validation.validate import validate_query, validate_sdl
from tests.functional.utils import assert_unordered_lists


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            input AnInput
            type Query {
              field(arg: AnInput = { f: true }): String
            }
            """,
            [],
        ),
        (
            """
            input AnInput
            type Query {
              field(
                arg1: AnInput = { f: true },
                arg2: AnInput = { f: true },
              ): String
            }
            """,
            [],
        ),
        (
            """
            input AnInput
            type Query {
              field(
                arg: AnInput = { f1: "value", f2: "value", f3: "value" }
              ): String
            }
            """,
            [],
        ),
        (
            """
            input AnInput
            type Query {
              field(arg: AnInput = {
                deep: {
                  deep: {
                    id: 1
                  }
                  id: 1
                }
                id: 1
              }): String
            }
            """,
            [],
        ),
        (
            """
            input AnInput
            type Query {
              field(arg: AnInput = { f1: "value", f1: "value" }): String
            }
            """,
            [
                TartifletteError(
                    message="There can be only one input field named < f1 >.",
                    locations=[
                        Location(line=4, column=38, line_end=4, column_end=40),
                        Location(line=4, column=51, line_end=4, column_end=53),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.3",
                        "tag": "input-object-field-uniqueness",
                        "details": "https://spec.graphql.org/June2018/#sec-Input-Object-Field-Uniqueness",
                    },
                )
            ],
        ),
        (
            """
            input AnInput
            type Query {
              field(
                arg: AnInput = { f1: "value", f1: "value", f1: "value" }
              ): String
            }
            """,
            [
                TartifletteError(
                    message="There can be only one input field named < f1 >.",
                    locations=[
                        Location(line=5, column=34, line_end=5, column_end=36),
                        Location(line=5, column=47, line_end=5, column_end=49),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.3",
                        "tag": "input-object-field-uniqueness",
                        "details": "https://spec.graphql.org/June2018/#sec-Input-Object-Field-Uniqueness",
                    },
                ),
                TartifletteError(
                    message="There can be only one input field named < f1 >.",
                    locations=[
                        Location(line=5, column=34, line_end=5, column_end=36),
                        Location(line=5, column=60, line_end=5, column_end=62),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.3",
                        "tag": "input-object-field-uniqueness",
                        "details": "https://spec.graphql.org/June2018/#sec-Input-Object-Field-Uniqueness",
                    },
                ),
            ],
        ),
        (
            """
            input AnInput
            type Query {
              field(arg: AnInput = { f1: {f2: "value", f2: "value" }}): String
            }
            """,
            [
                TartifletteError(
                    message="There can be only one input field named < f2 >.",
                    locations=[
                        Location(line=4, column=43, line_end=4, column_end=45),
                        Location(line=4, column=56, line_end=4, column_end=58),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.3",
                        "tag": "input-object-field-uniqueness",
                        "details": "https://spec.graphql.org/June2018/#sec-Input-Object-Field-Uniqueness",
                    },
                )
            ],
        ),
        (
            """
            input AnInput
            type Query {
              field(arg: AnInput = { f1: {f2: "value", f2: "value" }}): String
              anotherField(
                arg: AnInput = { fa: {fb: "value", fb: "value" }}
              ): String
            }
            """,
            [
                TartifletteError(
                    message="There can be only one input field named < f2 >.",
                    locations=[
                        Location(line=4, column=43, line_end=4, column_end=45),
                        Location(line=4, column=56, line_end=4, column_end=58),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.3",
                        "tag": "input-object-field-uniqueness",
                        "details": "https://spec.graphql.org/June2018/#sec-Input-Object-Field-Uniqueness",
                    },
                ),
                TartifletteError(
                    message="There can be only one input field named < fb >.",
                    locations=[
                        Location(line=6, column=39, line_end=6, column_end=41),
                        Location(line=6, column=52, line_end=6, column_end=54),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.3",
                        "tag": "input-object-field-uniqueness",
                        "details": "https://spec.graphql.org/June2018/#sec-Input-Object-Field-Uniqueness",
                    },
                ),
            ],
        ),
        (
            """
            input AnInput
            type Query {
              field(arg: AnInput = { f1: {f2: "value", f2: "value" }}): String
              anotherField(
                arg: AnInput = { fa: {fb: "value", fb: "value" }, fa: true }
              ): String
            }
            """,
            [
                TartifletteError(
                    message="There can be only one input field named < f2 >.",
                    locations=[
                        Location(line=4, column=43, line_end=4, column_end=45),
                        Location(line=4, column=56, line_end=4, column_end=58),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.3",
                        "tag": "input-object-field-uniqueness",
                        "details": "https://spec.graphql.org/June2018/#sec-Input-Object-Field-Uniqueness",
                    },
                ),
                TartifletteError(
                    message="There can be only one input field named < fb >.",
                    locations=[
                        Location(line=6, column=39, line_end=6, column_end=41),
                        Location(line=6, column=52, line_end=6, column_end=54),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.3",
                        "tag": "input-object-field-uniqueness",
                        "details": "https://spec.graphql.org/June2018/#sec-Input-Object-Field-Uniqueness",
                    },
                ),
                TartifletteError(
                    message="There can be only one input field named < fa >.",
                    locations=[
                        Location(line=6, column=34, line_end=6, column_end=36),
                        Location(line=6, column=67, line_end=6, column_end=69),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.3",
                        "tag": "input-object-field-uniqueness",
                        "details": "https://spec.graphql.org/June2018/#sec-Input-Object-Field-Uniqueness",
                    },
                ),
            ],
        ),
    ],
)
async def test_unique_input_field_names(sdl, expected):
    assert (
        validate_sdl(parse_to_document(sdl), rules=[UniqueInputFieldNamesRule])
        == expected
    )


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="harness")
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            {
              field(arg: { f: true })
            }
            """,
            [],
        ),
        (
            """
            {
              field(arg1: { f: true }, arg2: { f: true })
            }
            """,
            [],
        ),
        (
            """
            {
              field(arg: { f1: "value", f2: "value", f3: "value" })
            }
            """,
            [],
        ),
        (
            """
            {
              field(arg: {
                deep: {
                  deep: {
                    id: 1
                  }
                  id: 1
                }
                id: 1
              })
            }
            """,
            [],
        ),
        (
            """
            {
              field(arg: { f1: "value", f1: "value" })
            }
            """,
            [
                TartifletteError(
                    message="There can be only one input field named < f1 >.",
                    locations=[
                        Location(line=3, column=28, line_end=3, column_end=30),
                        Location(line=3, column=41, line_end=3, column_end=43),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.3",
                        "tag": "input-object-field-uniqueness",
                        "details": "https://spec.graphql.org/June2018/#sec-Input-Object-Field-Uniqueness",
                    },
                )
            ],
        ),
        (
            """
            {
              field(arg: { f1: "value", f1: "value", f1: "value" })
            }
            """,
            [
                TartifletteError(
                    message="There can be only one input field named < f1 >.",
                    locations=[
                        Location(line=3, column=28, line_end=3, column_end=30),
                        Location(line=3, column=41, line_end=3, column_end=43),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.3",
                        "tag": "input-object-field-uniqueness",
                        "details": "https://spec.graphql.org/June2018/#sec-Input-Object-Field-Uniqueness",
                    },
                ),
                TartifletteError(
                    message="There can be only one input field named < f1 >.",
                    locations=[
                        Location(line=3, column=28, line_end=3, column_end=30),
                        Location(line=3, column=54, line_end=3, column_end=56),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.3",
                        "tag": "input-object-field-uniqueness",
                        "details": "https://spec.graphql.org/June2018/#sec-Input-Object-Field-Uniqueness",
                    },
                ),
            ],
        ),
        (
            """
            {
              field(arg: { f1: {f2: "value", f2: "value" }})
            }
            """,
            [
                TartifletteError(
                    message="There can be only one input field named < f2 >.",
                    locations=[
                        Location(line=3, column=33, line_end=3, column_end=35),
                        Location(line=3, column=46, line_end=3, column_end=48),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.3",
                        "tag": "input-object-field-uniqueness",
                        "details": "https://spec.graphql.org/June2018/#sec-Input-Object-Field-Uniqueness",
                    },
                )
            ],
        ),
    ],
)
async def test_unique_input_field_names_query(schema_stack, query, expected):
    assert_unordered_lists(
        validate_query(
            schema_stack.schema,
            parse_query_to_document(query),
            rules=[UniqueInputFieldNamesRule],
        ),
        expected,
    )
