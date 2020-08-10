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

    assert await ttftt_engine.execute(query) == {
        "data": None,
        "errors": [
            {
                "message": "Unknown fragment < UndefinedFragment >.",
                "path": None,
                "locations": [{"line": 5, "column": 16}],
                "extensions": {
                    "spec": "June 2018",
                    "rule": "5.5.2.1",
                    "tag": "fragment-spread-target-defined",
                    "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-target-defined",
                },
            }
        ],
    }
