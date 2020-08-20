import pytest

from tartiflette import Resolver


def bakery(schema_name):
    @Resolver("Query.hello", schema_name=schema_name)
    async def resolve_query_hello(parent, args, ctx, info):
        return args.get("name")

    class QueryByResolver:
        async def __call__(self, parent, args, ctx, info):
            return args.get("name")

    Resolver("Query.bye", schema_name=schema_name)(QueryByResolver())


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    type Query {
      hello(name: String = "Unknown"): String
      bye(name: String! = "Unknown"): String
    }
    """,
    bakery=bakery,
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        # Without variables
        (
            """
            query {
              hello
            }
            """,
            None,
            {"data": {"hello": "Unknown"}},
        ),
        (
            """
            query {
              hello(name: "Name")
            }
            """,
            None,
            {"data": {"hello": "Name"}},
        ),
        (
            """
            query {
              hello(name: null)
            }
            """,
            None,
            {"data": {"hello": None}},
        ),
        (
            """
            query {
              bye
            }
            """,
            None,
            {"data": {"bye": "Unknown"}},
        ),
        (
            """
            query {
              bye(name: "Name")
            }
            """,
            None,
            {"data": {"bye": "Name"}},
        ),
        (
            """
            query {
              bye(name: null)
            }
            """,
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < String! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 3, "column": 25}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    }
                ],
            },
        ),
        # With variables
        (
            """
            query ($name: String) {
              hello(name: $name)
            }
            """,
            {},
            {"data": {"hello": "Unknown"}},
        ),
        (
            """
            query ($name: String) {
              hello(name: $name)
            }
            """,
            {"name": "Name"},
            {"data": {"hello": "Name"}},
        ),
        (
            """
            query ($name: String) {
              hello(name: $name)
            }
            """,
            {"name": None},
            {"data": {"hello": None}},
        ),
        (
            """
            query ($name: String) {
              bye(name: $name)
            }
            """,
            {},
            {"data": {"bye": "Unknown"}},
        ),
        (
            """
            query ($name: String) {
              bye(name: $name)
            }
            """,
            {"name": "Name"},
            {"data": {"bye": "Name"}},
        ),
        (
            """
            query ($name: String) {
              bye(name: $name)
            }
            """,
            {"name": None},
            {
                "data": {"bye": None},
                "errors": [
                    {
                        "message": "Argument < name > of non-null type < String! > must not be null.",
                        "path": ["bye"],
                        "locations": [{"line": 3, "column": 25}],
                    }
                ],
            },
        ),
        (
            """
            query ($name: String!) {
              bye(name: $name)
            }
            """,
            {"name": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $name > of non-null type < String! > must not be null.",
                        "path": None,
                        "locations": [{"line": 2, "column": 20}],
                    }
                ],
            },
        ),
    ],
)
async def test_issue213(schema_stack, query, variables, expected):
    assert await schema_stack.execute(query, variables=variables) == expected
