import pytest

from tartiflette import Engine, Resolver


@Resolver("Query.hello", schema_name="test_issue213")
async def resolve_query_hello(parent, args, ctx, info):
    return args.get("name")


@Resolver("Query.bye", schema_name="test_issue213")
async def resolve_query_bye(parent, args, ctx, info):
    return args.get("name")


_SDL = """
type Query {
  hello(name: String = "Unknown"): String
  bye(name: String! = "Unknown"): String
}
"""


_TTFTT_ENGINE = Engine(_SDL, schema_name="test_issue213")


@pytest.mark.asyncio
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
                "data": {"bye": None},
                "errors": [
                    {
                        "message": "Argument < name > of non-null type < String! > must not be null.",
                        "path": ["bye"],
                        "locations": [{"line": 3, "column": 15}],
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
                        "locations": [{"line": 3, "column": 15}],
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
async def test_issue213(query, variables, expected):
    assert await _TTFTT_ENGINE.execute(query, variables=variables) == expected
