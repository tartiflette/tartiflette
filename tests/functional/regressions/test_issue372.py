import pytest

from tartiflette import create_schema
from tartiflette.types.exceptions.tartiflette import GraphQLSchemaError
from tests.functional.utils import match_schema_errors


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected_errors",
    [
        (
            """interface MediaMetadata {
                height: Int
                width : Int
            }

            interface Media {
                metadata: MediaMetadata
            }

            type VideoMetadata implements MediaMetadata {
                height: Int
                width : Int
                duration: Int
            }

            type Video implements Media {
                metadata: VideoMetadata
            }

            type Live implements Media {
                metadata: MediaMetadata
            }

            type Query {
                media: Media
            }""",
            False,
        ),
        (
            """interface A {
                b: String!
            }

            type I implements A {
                b: String
            }

            type Query {
                a: I
            }""",
            [
                "Interface field < A.b > expects type < String! > but < I.b > is type < String >."
            ],
        ),
        (
            """interface A {
                c: [String]
            }

            type I implements A {
                c: String
            }
            type Query {
                a: I
            }""",
            [
                "Interface field < A.c > expects type < [String] > but < I.c > is type < String >."
            ],
        ),
        (
            """interface A {
                d: [String!]
            }

            type I implements A {
                d: [String]
            }
            type Query {
                a: I
            }""",
            [
                "Interface field < A.d > expects type < [String!] > but < I.d > is type < [String] >."
            ],
        ),
        (
            """interface A {
                e: [String!]!
            }

            type I implements A {
                e: [String]
            }
            type Query {
                a: I
            }""",
            [
                "Interface field < A.e > expects type < [String!]! > but < I.e > is type < [String] >."
            ],
        ),
        (
            """interface A {
                f: [String]!
            }

            type I implements A {
                f: [String!]
            }
            type Query {
                a: I
            }""",
            [
                "Interface field < A.f > expects type < [String]! > but < I.f > is type < [String!] >."
            ],
        ),
        (
            """interface A {
                g: String
            }

            type I implements A {
                g: Float
            }

            type Query {
                a: I
            }
            """,
            [
                "Interface field < A.g > expects type < String > but < I.g > is type < Float >."
            ],
        ),
        (
            """interface A {
                B: String
            }

            type I implements A {
                B: String!
            }

            type Query {
                a: I
            }
            """,
            False,
        ),
        (
            """
            interface A {
                f(a: String): String
            }

            type B implements A {
                f(a: Float): String
            }

            type Query{
                a: B
            }
            """,
            [
                "Interface field argument < A.f(a:) > expects type < String > but < B.f(a:) > is type < Float >."
            ],
        ),
        (
            """
            interface A {
                f(a: String!): String
            }

            type B implements A {
                f(a: String): String
            }

            type Query{
                a: B
            }
            """,
            [
                "Interface field argument < A.f(a:) > expects type < String! > but < B.f(a:) > is type < String >."
            ],
        ),
        (
            """
            interface A {
                f(a: String): String
            }

            type B implements A {
                f(a: String!): String
            }

            type Query{
                a: B
            }
            """,
            [
                "Interface field argument < A.f(a:) > expects type < String > but < B.f(a:) > is type < String! >."
            ],
        ),
        (
            """
            interface A {
                f(a: String): String
            }

            type B implements A {
                f: String
            }

            type Query{
                a: B
            }
            """,
            [
                "Interface field argument < A.f(a:) > expected but < B.f > does not provide it."
            ],
        ),
        (
            """
            interface A {
                f(a: String): String
            }

            type B implements A {
                f(a: String, b:Int!): String
            }

            type Query{
                a: B
            }
            """,
            [
                "Object field < B.f > includes required argument b that is missing from the Interface field < A.f >."
            ],
        ),
        (
            """
            interface A {
                f(a: String): String
            }

            type B implements A {
                f(a: String, b:Int): String
            }

            type Query{
                a: B
            }
            """,
            False,
        ),
        (
            "interface A { d: String! } type I implements A { d: Float! }",
            [
                "Query root type must be provided.",
                "Interface field < A.d > expects type < String! > but < I.d > is type < Float! >.",
            ],
        ),
        (
            "interface A { d: [String] } type I implements A { d: [Float] }",
            [
                "Query root type must be provided.",
                "Interface field < A.d > expects type < [String] > but < I.d > is type < [Float] >.",
            ],
        ),
        (
            "interface A { f(a: String!): String } type B implements A { f(a: Float!): String }",
            [
                "Query root type must be provided.",
                "Interface field argument < A.f(a:) > expects type < String! > but < B.f(a:) > is type < Float! >.",
            ],
        ),
        (
            "interface A { f(a:[String]): String } type B implements A { f(a: [Float]): String }",
            [
                "Query root type must be provided.",
                "Interface field argument < A.f(a:) > expects type < [String] > but < B.f(a:) > is type < [Float] >.",
            ],
        ),
    ],
)
async def test_issue372(sdl, expected_errors, random_schema_name):
    if expected_errors:
        with pytest.raises(GraphQLSchemaError) as excinfo:
            await create_schema(sdl, name=random_schema_name)
        match_schema_errors(excinfo.value, expected_errors)
    else:
        await create_schema(sdl, name=random_schema_name)
