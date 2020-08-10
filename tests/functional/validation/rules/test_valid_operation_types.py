import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import ValidOperationTypesRule
from tartiflette.validation.validate import validate_sdl


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            type Query
            """,
            [],
        ),
        (
            """
            type Foo
            schema {
              query: Foo
            }
            """,
            [],
        ),
        (
            """
            type Foo
            """,
            [
                TartifletteError(
                    message="Query root type must be provided.",
                    locations=[
                        Location(line=2, column=13, line_end=2, column_end=21)
                    ],
                )
            ],
        ),
        (
            """
            schema {
              query: Query
            }
            """,
            [
                TartifletteError(
                    message="Query root type must be Object type.",
                    locations=[
                        Location(line=3, column=22, line_end=3, column_end=27)
                    ],
                )
            ],
        ),
        (
            """
            input Query
            schema {
              query: Query
            }
            """,
            [
                TartifletteError(
                    message="Query root type must be Object type.",
                    locations=[
                        Location(line=4, column=22, line_end=4, column_end=27)
                    ],
                )
            ],
        ),
        (
            """
            scalar Foo
            schema {
              query: Foo
            }
            """,
            [
                TartifletteError(
                    message="Query root type must be Object type.",
                    locations=[
                        Location(line=4, column=22, line_end=4, column_end=25)
                    ],
                )
            ],
        ),
        (
            """
            directive @foo on FIELD
            schema {
              query: foo
            }
            """,
            [
                TartifletteError(
                    message="Query root type must be Object type.",
                    locations=[
                        Location(line=4, column=22, line_end=4, column_end=25)
                    ],
                )
            ],
        ),
        (
            """
            type Foo
            schema {
              query: Unknown
            }
            """,
            [
                TartifletteError(
                    message="Query root type must be Object type.",
                    locations=[
                        Location(line=4, column=22, line_end=4, column_end=29)
                    ],
                )
            ],
        ),
        (
            """
            type Query
            type Mutation
            """,
            [],
        ),
        (
            """
            type Query
            type Foo
            schema {
              mutation: Foo
            }
            """,
            [],
        ),
        (
            """
            type Query
            type Foo
            """,
            [],
        ),
        (
            """
            type Query
            schema {
              mutation: Mutation
            }
            """,
            [
                TartifletteError(
                    message="Mutation root type must be Object type.",
                    locations=[
                        Location(line=4, column=25, line_end=4, column_end=33)
                    ],
                )
            ],
        ),
        (
            """
            type Query
            input Mutation
            schema {
              mutation: Mutation
            }
            """,
            [
                TartifletteError(
                    message="Mutation root type must be Object type.",
                    locations=[
                        Location(line=5, column=25, line_end=5, column_end=33)
                    ],
                )
            ],
        ),
        (
            """
            type Query
            scalar Foo
            schema {
              mutation: Foo
            }
            """,
            [
                TartifletteError(
                    message="Mutation root type must be Object type.",
                    locations=[
                        Location(line=5, column=25, line_end=5, column_end=28)
                    ],
                )
            ],
        ),
        (
            """
            type Query
            directive @foo on FIELD
            schema {
              mutation: foo
            }
            """,
            [
                TartifletteError(
                    message="Mutation root type must be Object type.",
                    locations=[
                        Location(line=5, column=25, line_end=5, column_end=28)
                    ],
                )
            ],
        ),
        (
            """
            type Query
            type Foo
            schema {
              mutation: Unknown
            }
            """,
            [
                TartifletteError(
                    message="Mutation root type must be Object type.",
                    locations=[
                        Location(line=5, column=25, line_end=5, column_end=32)
                    ],
                )
            ],
        ),
        (
            """
            type Query
            type Subscription
            """,
            [],
        ),
        (
            """
            type Query
            type Foo
            schema {
              subscription: Foo
            }
            """,
            [],
        ),
        (
            """
            type Query
            type Foo
            """,
            [],
        ),
        (
            """
            type Query
            schema {
              subscription: Subscription
            }
            """,
            [
                TartifletteError(
                    message="Subscription root type must be Object type.",
                    locations=[
                        Location(line=4, column=29, line_end=4, column_end=41)
                    ],
                )
            ],
        ),
        (
            """
            type Query
            input Subscription
            schema {
              subscription: Subscription
            }
            """,
            [
                TartifletteError(
                    message="Subscription root type must be Object type.",
                    locations=[
                        Location(line=5, column=29, line_end=5, column_end=41)
                    ],
                )
            ],
        ),
        (
            """
            type Query
            scalar Foo
            schema {
              subscription: Foo
            }
            """,
            [
                TartifletteError(
                    message="Subscription root type must be Object type.",
                    locations=[
                        Location(line=5, column=29, line_end=5, column_end=32)
                    ],
                )
            ],
        ),
        (
            """
            type Query
            directive @foo on FIELD
            schema {
              subscription: foo
            }
            """,
            [
                TartifletteError(
                    message="Subscription root type must be Object type.",
                    locations=[
                        Location(line=5, column=29, line_end=5, column_end=32)
                    ],
                )
            ],
        ),
        (
            """
            type Query
            type Foo
            schema {
              subscription: Unknown
            }
            """,
            [
                TartifletteError(
                    message="Subscription root type must be Object type.",
                    locations=[
                        Location(line=5, column=29, line_end=5, column_end=36)
                    ],
                )
            ],
        ),
    ],
)
async def test_valid_operation_types(sdl, expected):
    assert (
        validate_sdl(parse_to_document(sdl), rules=[ValidOperationTypesRule])
        == expected
    )
