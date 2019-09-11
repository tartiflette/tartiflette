import pytest

from tartiflette import Resolver, create_engine


@Resolver("Query.viewer", schema_name="test_issue82")
async def resolver_query_viewer(*_, **__):
    return {"name": "N1"}


_SDL = """
type User {
    name: String
}

type Query {
    viewer: User
}
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    return await create_engine(sdl=_SDL, schema_name="test_issue82")


@pytest.mark.asyncio
async def test_issue82(ttftt_engine):
    query = """
    query {
        viewer {
            name
            ...UndefinedFragment
        }
    }
    """

    results = await ttftt_engine.execute(query)

    assert results == {
        "data": None,
        "errors": [
            {
                "message": "Unknown Fragment for Spread < UndefinedFragment >.",
                "path": None,
                "locations": [{"line": 5, "column": 13}],
                "extensions": {
                    "rule": "5.5.2.1",
                    "spec": "June 2018",
                    "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-spread-target-defined",
                    "tag": "fragment-spread-target-defined",
                },
            }
        ],
    }
