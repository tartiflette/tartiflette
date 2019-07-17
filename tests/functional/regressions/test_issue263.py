import pytest

from tartiflette import Resolver, create_engine

_SDL = """
type Query {
  aField(ids: [String]): String
}
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Resolver("Query.aField", schema_name="test_issuexxx")
    async def resolve_query_sections(parent, args, ctx, info):
        return str(args.get("ids"))

    return await create_engine(sdl=_SDL, schema_name="test_issuexxx")


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
                        "message": "Variable < ids > is not known",
                        "path": None,
                        "locations": [],
                    },
                    {
                        "message": "Variable < ids > is not known",
                        "path": None,
                        "locations": [],
                    },
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
                        "message": "Variable < ids > is not known",
                        "path": None,
                        "locations": [],
                    },
                    {
                        "message": "Variable < ids > is not known",
                        "path": None,
                        "locations": [],
                    },
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
                        "message": "Variable < ids > is not known",
                        "path": None,
                        "locations": [],
                    },
                    {
                        "message": "Variable < ids > is not known",
                        "path": None,
                        "locations": [],
                    },
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
                        "message": "Variable < ids > is not known",
                        "path": None,
                        "locations": [],
                    },
                    {
                        "message": "Variable < ids > is not known",
                        "path": None,
                        "locations": [],
                    },
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
                        "message": "Value can't be null or contain a null value",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Given value for < ids > is not type < <class 'str'> >",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
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
                        "message": "Value can't be null or contain a null value",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Given value for < ids > is not type < <class 'str'> >",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                ],
            },
        ),
        # String variable value
        (
            "query ($ids: [String]) { aField(ids: $ids) }",
            {"ids": "anId"},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expecting List for < ids > values",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            "query ($ids: [String!]) { aField(ids: $ids) }",
            {"ids": "anId"},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expecting List for < ids > values",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            "query ($ids: [String]!) { aField(ids: $ids) }",
            {"ids": "anId"},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expecting List for < ids > values",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            "query ($ids: [String!]!) { aField(ids: $ids) }",
            {"ids": "anId"},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expecting List for < ids > values",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
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
                        "message": "Value can't be null or contain a null value",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Given value for < ids > is not type < <class 'str'> >",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
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
                        "message": "Value can't be null or contain a null value",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Given value for < ids > is not type < <class 'str'> >",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
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
    ],
)
async def test_issuexxx(ttftt_engine, query, variables, expected):
    assert await ttftt_engine.execute(query, variables=variables) == expected
