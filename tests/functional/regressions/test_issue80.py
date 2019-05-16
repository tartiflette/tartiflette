import pytest

from tartiflette import Resolver, create_engine


@Resolver("Query.viewer", schema_name="test_issue80")
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
    return await create_engine(sdl=_SDL, schema_name="test_issue80")


@pytest.mark.asyncio
async def test_issue80(ttftt_engine):
    query = """
    fragment UserFields on User {
        name
    }

    query {
        viewer {
            name
        }
    }
    """

    results = await ttftt_engine.execute(query)

    assert results == {
        "data": None,
        "errors": [
            {
                "message": "Fragment < UserFields > is never used.",
                "path": None,
                "locations": [{"line": 2, "column": 5}],
                "extensions": {
                    "rule": "5.5.1.4",
                    "spec": "June 2018",
                    "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Fragments-Must-Be-Used",
                    "tag": "fragment-must-be-used",
                },
            }
        ],
    }
