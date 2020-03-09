import pytest

from tartiflette import create_engine
from tartiflette.types.exceptions.tartiflette import GraphQLSchemaError


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,should_except,match",
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
            None,
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
            True,
            r".*Field < I\.b > should be of Type < String! > as defined in the < A > Interface\..*",
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
            True,
            r".*Field < I\.c > should be of Type < \[String\] > as defined in the < A > Interface\..*",
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
            True,
            r".*Field < I\.d > should be of Type < \[String!\] > as defined in the < A > Interface\..*",
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
            True,
            r".*Field < I\.e > should be of Type < \[String!\]! > as defined in the < A > Interface\..*",
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
            True,
            r".*Field < I\.f > should be of Type < \[String\]! > as defined in the < A > Interface\..*",
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
            True,
            r".*Field < I\.g > should be of Type < String > as defined in the < A > Interface\..*",
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
            None,
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
            True,
            r".*Field argument < B\.f\(a\) > is not of type < String > as required by the interface < A >\..*",
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
            True,
            r".*Field argument < B\.f\(a\) > is not of type < String! > as required by the interface < A >\..*",
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
            True,
            r".*Field argument < B\.f\(a\) > is not of type < String > as required by the interface < A >\..*",
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
            True,
            r".*Field < B\.f > is missing interface field argument < A\.f\(a\) >\..*",
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
            True,
            r".*Field < B\.f\(b\) > isn't required in interface field < A\.f >, so it cannot be NonNullable\..*",
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
            None,
        ),
        (
            "interface A { d: String! } type I implements A { d: Float! }",
            True,
            r".*Field < I\.d > should be of Type < String! > as defined in the < A > Interface\..*",
        ),
        (
            "interface A { d: [String] } type I implements A { d: [Float] }",
            True,
            r".*Field < I\.d > should be of Type < \[String\] > as defined in the < A > Interface\..*",
        ),
        (
            "interface A { f(a: String!): String } type B implements A { f(a: Float!): String }",
            True,
            r".*Field argument < B\.f\(a\) > is not of type < String! > as required by the interface < A >\..*",
        ),
        (
            "interface A { f(a:[String]): String } type B implements A { f(a: [Float]): String }",
            True,
            r".*Field argument < B\.f\(a\) > is not of type < \[String\] > as required by the interface < A >\..*",
        ),
    ],
)
async def test_issue372(sdl, should_except, match, random_schema_name):
    if not should_except:
        assert (
            await create_engine(sdl, schema_name=random_schema_name,)
            is not None
        )
    else:
        with pytest.raises(GraphQLSchemaError, match=match):
            await create_engine(
                sdl, schema_name=random_schema_name,
            )
