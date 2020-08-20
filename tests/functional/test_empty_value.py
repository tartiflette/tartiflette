import pytest

from tartiflette import Resolver


def bakery(schema_name):
    @Resolver("Query.string1", schema_name=schema_name)
    @Resolver("Query.stringList", schema_name=schema_name)
    @Resolver("Query.stringListNonNull", schema_name=schema_name)
    @Resolver("Query.nonNullStringList", schema_name=schema_name)
    @Resolver("Query.nonNullStringListNonNull", schema_name=schema_name)
    @Resolver("bobby.c", schema_name=schema_name)
    @Resolver("boby.b", schema_name=schema_name)
    async def resolver_x(_pr, _args, _ctx, _info):
        return None

    @Resolver("Query.anObject", schema_name=schema_name)
    @Resolver("bob.a", schema_name=schema_name)
    async def resolver_y(_pr, _args, _ctx, _info):
        return {}


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
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
    """,
    bakery=bakery,
)
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
                        "message": "Cannot return null for non-nullable field Query.string1.",
                        "path": ["string1"],
                        "locations": [{"column": 17, "line": 3}],
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
                        "message": "Cannot return null for non-nullable field Query.stringListNonNull.",
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
                        "message": "Cannot return null for non-nullable field Query.nonNullStringListNonNull.",
                        "path": ["nonNullStringListNonNull"],
                        "locations": [{"line": 3, "column": 17}],
                    }
                ],
            },
        ),
        (
            """
            query {
                string1
                stringList
                nonNullStringList
                stringListNonNull
                nonNullStringListNonNull
            }""",
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.string1.",
                        "path": ["string1"],
                        "locations": [{"line": 3, "column": 17}],
                    },
                    {
                        "message": "Cannot return null for non-nullable field Query.stringListNonNull.",
                        "path": ["stringListNonNull"],
                        "locations": [{"line": 6, "column": 17}],
                    },
                    {
                        "message": "Cannot return null for non-nullable field Query.nonNullStringListNonNull.",
                        "path": ["nonNullStringListNonNull"],
                        "locations": [{"line": 7, "column": 17}],
                    },
                ],
            },
        ),
        (
            """
            query {
                anObject { a {b { c}}}
            }
            """,
            {
                "data": {"anObject": {"a": None}},
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field boby.b.",
                        "path": ["anObject", "a", "b"],
                        "locations": [{"line": 3, "column": 31}],
                    }
                ],
            },
        ),
    ],
)
async def test_empty_values(schema_stack, query, expected):
    assert await schema_stack.execute(query) == expected
