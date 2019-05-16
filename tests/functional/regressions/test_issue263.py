import pytest

from tartiflette import Resolver, create_engine

_SDL = """
type Query {
  aField(ids: [String]): String
}
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Resolver("Query.aField", schema_name="test_issue263")
    async def resolve_query_sections(parent, args, ctx, info):
        return str(args.get("ids"))

    return await create_engine(sdl=_SDL, schema_name="test_issue263")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        # No variables
        (
            "query ($ids: [String]) { aField(ids: $ids) }",
            None,
            {"data": {"aField": "None"}},
        ),
        (
            "query ($ids: [String!]) { aField(ids: $ids) }",
            None,
            {"data": {"aField": "None"}},
        ),
        (
            "query ($ids: [String]!) { aField(ids: $ids) }",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $ids > of required type < [String]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            "query ($ids: [String!]!) { aField(ids: $ids) }",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $ids > of required type < [String!]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        # Empty variables
        (
            "query ($ids: [String]) { aField(ids: $ids) }",
            {},
            {"data": {"aField": "None"}},
        ),
        (
            "query ($ids: [String!]) { aField(ids: $ids) }",
            {},
            {"data": {"aField": "None"}},
        ),
        (
            "query ($ids: [String]!) { aField(ids: $ids) }",
            {},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $ids > of required type < [String]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            "query ($ids: [String!]!) { aField(ids: $ids) }",
            {},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $ids > of required type < [String!]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        # `null` variable value
        (
            "query ($ids: [String]) { aField(ids: $ids) }",
            {"ids": None},
            {"data": {"aField": "None"}},
        ),
        (
            "query ($ids: [String!]) { aField(ids: $ids) }",
            {"ids": None},
            {"data": {"aField": "None"}},
        ),
        (
            "query ($ids: [String]!) { aField(ids: $ids) }",
            {"ids": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $ids > of non-null type < [String]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            "query ($ids: [String!]!) { aField(ids: $ids) }",
            {"ids": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $ids > of non-null type < [String!]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        # String variable value
        (
            "query ($ids: [String]) { aField(ids: $ids) }",
            {"ids": "anId"},
            {"data": {"aField": "['anId']"}},
        ),
        (
            "query ($ids: [String!]) { aField(ids: $ids) }",
            {"ids": "anId"},
            {"data": {"aField": "['anId']"}},
        ),
        (
            "query ($ids: [String]!) { aField(ids: $ids) }",
            {"ids": "anId"},
            {"data": {"aField": "['anId']"}},
        ),
        (
            "query ($ids: [String!]!) { aField(ids: $ids) }",
            {"ids": "anId"},
            {"data": {"aField": "['anId']"}},
        ),
        # List with `null` item variable value
        (
            "query ($ids: [String]) { aField(ids: $ids) }",
            {"ids": [None]},
            {"data": {"aField": "[None]"}},
        ),
        (
            "query ($ids: [String!]) { aField(ids: $ids) }",
            {"ids": [None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $ids > got invalid value < [None] >; Expected non-nullable type < String! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            "query ($ids: [String]!) { aField(ids: $ids) }",
            {"ids": [None]},
            {"data": {"aField": "[None]"}},
        ),
        (
            "query ($ids: [String!]!) { aField(ids: $ids) }",
            {"ids": [None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $ids > got invalid value < [None] >; Expected non-nullable type < String! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        # List with string item variable value
        (
            "query ($ids: [String]) { aField(ids: $ids) }",
            {"ids": ["anId"]},
            {"data": {"aField": "['anId']"}},
        ),
        (
            "query ($ids: [String!]) { aField(ids: $ids) }",
            {"ids": ["anId"]},
            {"data": {"aField": "['anId']"}},
        ),
        (
            "query ($ids: [String]!) { aField(ids: $ids) }",
            {"ids": ["anId"]},
            {"data": {"aField": "['anId']"}},
        ),
        (
            "query ($ids: [String!]!) { aField(ids: $ids) }",
            {"ids": ["anId"]},
            {"data": {"aField": "['anId']"}},
        ),
        (
            "query ($ids: [String!]) { aField(ids: $ids) }",
            {"ids": []},
            {"data": {"aField": "[]"}},
        ),
    ],
)
async def test_issue263(ttftt_engine, query, variables, expected):
    assert await ttftt_engine.execute(query, variables=variables) == expected
