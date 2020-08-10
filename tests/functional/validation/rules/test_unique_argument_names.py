import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.language.parsers.libgraphqlparser import (
    parse_to_document as parse_query_to_document,
)
from tartiflette.validation.rules import UniqueArgumentNamesRule
from tartiflette.validation.validate import validate_query, validate_sdl
from tests.functional.utils import assert_unordered_lists


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            type Query {
              field: String @directive
            }
            """,
            [],
        ),
        (
            """
            type Query {
              field: String @directive(arg: "value")
            }
            """,
            [],
        ),
        (
            """
            type Query {
              field(arg: String = "value"): String @directive(arg: "value")
            }
            """,
            [],
        ),
        (
            """
            type Query {
              field: String @directive1(arg: "value") @directive2(arg: "value")
            }
            """,
            [],
        ),
        (
            """
            type Query {
              field: String @directive(arg1: "value", arg2: "value", arg3: "value")
            }
            """,
            [],
        ),
        (
            """
            type Query {
              field: String @directive(arg1: "value", arg1: "value")
            }
            """,
            [
                TartifletteError(
                    message="There can be only one argument named < arg1 >.",
                    locations=[
                        Location(line=3, column=40, line_end=3, column_end=44),
                        Location(line=3, column=55, line_end=3, column_end=59),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.2",
                        "tag": "argument-uniqueness",
                        "details": "http://spec.graphql.org/June2018/#sec-Argument-Uniqueness",
                    },
                )
            ],
        ),
        (
            """
            type Query {
              field: String @directive(arg1: "value", arg1: "value", arg1: "value")
            }
            """,
            [
                TartifletteError(
                    message="There can be only one argument named < arg1 >.",
                    locations=[
                        Location(line=3, column=40, line_end=3, column_end=44),
                        Location(line=3, column=55, line_end=3, column_end=59),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.2",
                        "tag": "argument-uniqueness",
                        "details": "http://spec.graphql.org/June2018/#sec-Argument-Uniqueness",
                    },
                ),
                TartifletteError(
                    message="There can be only one argument named < arg1 >.",
                    locations=[
                        Location(line=3, column=40, line_end=3, column_end=44),
                        Location(line=3, column=70, line_end=3, column_end=74),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.2",
                        "tag": "argument-uniqueness",
                        "details": "http://spec.graphql.org/June2018/#sec-Argument-Uniqueness",
                    },
                ),
            ],
        ),
    ],
)
async def test_unique_argument_names(sdl, expected):
    assert (
        validate_sdl(parse_to_document(sdl), rules=[UniqueArgumentNamesRule])
        == expected
    )


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(name="harness")
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
              field @directive
            }
            """,
            [],
        ),
        (
            """
            {
              field(arg: "value")
            }
            """,
            [],
        ),
        (
            """
            {
              field @directive(arg: "value")
            }
            """,
            [],
        ),
        (
            """
            {
              one: field(arg: "value")
              two: field(arg: "value")
            }
            """,
            [],
        ),
        (
            """
            {
              field(arg: "value") @directive(arg: "value")
            }
            """,
            [],
        ),
        (
            """
            {
              field @directive1(arg: "value") @directive2(arg: "value")
            }
            """,
            [],
        ),
        (
            """
            {
              field(arg1: "value", arg2: "value", arg3: "value")
            }
            """,
            [],
        ),
        (
            """
            {
              field @directive(arg1: "value", arg2: "value", arg3: "value")
            }
            """,
            [],
        ),
        (
            """
            {
              field(arg1: "value", arg1: "value")
            }
            """,
            [
                TartifletteError(
                    message="There can be only one argument named < arg1 >.",
                    locations=[
                        Location(line=3, column=21, line_end=3, column_end=25),
                        Location(line=3, column=36, line_end=3, column_end=40),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.2",
                        "tag": "argument-uniqueness",
                        "details": "http://spec.graphql.org/June2018/#sec-Argument-Uniqueness",
                    },
                )
            ],
        ),
        (
            """
            {
              field(arg1: "value", arg1: "value", arg1: "value")
            }
            """,
            [
                TartifletteError(
                    message="There can be only one argument named < arg1 >.",
                    locations=[
                        Location(line=3, column=21, line_end=3, column_end=25),
                        Location(line=3, column=36, line_end=3, column_end=40),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.2",
                        "tag": "argument-uniqueness",
                        "details": "http://spec.graphql.org/June2018/#sec-Argument-Uniqueness",
                    },
                ),
                TartifletteError(
                    message="There can be only one argument named < arg1 >.",
                    locations=[
                        Location(line=3, column=21, line_end=3, column_end=25),
                        Location(line=3, column=51, line_end=3, column_end=55),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.2",
                        "tag": "argument-uniqueness",
                        "details": "http://spec.graphql.org/June2018/#sec-Argument-Uniqueness",
                    },
                ),
            ],
        ),
        (
            """
            {
              field @directive(arg1: "value", arg1: "value")
            }
            """,
            [
                TartifletteError(
                    message="There can be only one argument named < arg1 >.",
                    locations=[
                        Location(line=3, column=32, line_end=3, column_end=36),
                        Location(line=3, column=47, line_end=3, column_end=51),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.2",
                        "tag": "argument-uniqueness",
                        "details": "http://spec.graphql.org/June2018/#sec-Argument-Uniqueness",
                    },
                )
            ],
        ),
        (
            """
            {
              field @directive(arg1: "value", arg1: "value", arg1: "value")
            }
            """,
            [
                TartifletteError(
                    message="There can be only one argument named < arg1 >.",
                    locations=[
                        Location(line=3, column=32, line_end=3, column_end=36),
                        Location(line=3, column=47, line_end=3, column_end=51),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.2",
                        "tag": "argument-uniqueness",
                        "details": "http://spec.graphql.org/June2018/#sec-Argument-Uniqueness",
                    },
                ),
                TartifletteError(
                    message="There can be only one argument named < arg1 >.",
                    locations=[
                        Location(line=3, column=32, line_end=3, column_end=36),
                        Location(line=3, column=62, line_end=3, column_end=66),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.4.2",
                        "tag": "argument-uniqueness",
                        "details": "http://spec.graphql.org/June2018/#sec-Argument-Uniqueness",
                    },
                ),
            ],
        ),
    ],
)
async def test_unique_argument_names_query(engine, query, expected):
    assert_unordered_lists(
        validate_query(
            engine._schema,
            parse_query_to_document(query, engine._schema),
            rules=[UniqueArgumentNamesRule],
        ),
        expected,
    )
