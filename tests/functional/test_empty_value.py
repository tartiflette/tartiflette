import pytest

from tartiflette import Resolver, create_engine

_SDL = """

type bobby {
    c: String
}

type boby {
    b: bobby!
}

type bob {
    a: boby
}

type Query {
    string1: String!
    stringList: [String]
    stringListNonNull: [String]!
    nonNullStringList: [String!]
    nonNullStringListNonNull: [String!]!
    anObject: bob
}

"""


@Resolver("Query.string1", schema_name="test_empty_values")
@Resolver("Query.stringList", schema_name="test_empty_values")
@Resolver("Query.stringListNonNull", schema_name="test_empty_values")
@Resolver("Query.nonNullStringList", schema_name="test_empty_values")
@Resolver("Query.nonNullStringListNonNull", schema_name="test_empty_values")
@Resolver("bobby.c", schema_name="test_empty_values")
@Resolver("boby.b", schema_name="test_empty_values")
async def resolver_x(_pr, _args, _ctx, _info):
    return None


@Resolver("Query.anObject", schema_name="test_empty_values")
@Resolver("bob.a", schema_name="test_empty_values")
async def resolver_y(_pr, _args, _ctx, _info):
    return {}


@pytest.fixture(scope="module")
async def ttftt_engine():
    return await create_engine(sdl=_SDL, schema_name="test_empty_values")


@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query {
                string1
            }""",
            {
                "data": None,
                "errors": [
                    {
                        "message": "Invalid value (value: None) for field `string1` of type `String!`",
                        "path": ["string1"],
                        "locations": [{"line": 3, "column": 17}],
                    }
                ],
            },
        ),
        (
            """
            query {
                stringList
            }
            """,
            {"data": {"stringList": None}},
        ),
        (
            """
            query {
                nonNullStringList
            }
            """,
            {"data": {"nonNullStringList": None}},
        ),
        (
            """
            query {
                stringListNonNull
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Invalid value (value: None) for field `stringListNonNull` of type `[String]!`",
                        "path": ["stringListNonNull"],
                        "locations": [{"line": 3, "column": 17}],
                    }
                ],
            },
        ),
        (
            """
            query {
                nonNullStringListNonNull
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Invalid value (value: None) for field `nonNullStringListNonNull` of type `[String!]!`",
                        "path": ["nonNullStringListNonNull"],
                        "locations": [{"line": 3, "column": 17}],
                    }
                ],
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_empty_values_1(query, expected, ttftt_engine):
    assert await ttftt_engine.execute(query) == expected


@pytest.mark.asyncio
async def test_empty_values_2(ttftt_engine):
    assert (
        await ttftt_engine.execute(
            """
        query {
            anObject { a {b { c}}}
        }
        """
        )
        == {
            "data": {"anObject": {"a": None}},
            "errors": [
                {
                    "message": "Invalid value (value: None) for field `b` of type `bobby!`",
                    "path": ["anObject", "a", "b"],
                    "locations": [{"line": 3, "column": 27}],
                }
            ],
        }
    )
