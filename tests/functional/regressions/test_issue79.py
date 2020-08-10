import pytest

from tartiflette import Resolver, create_engine


@Resolver("Query.viewer", schema_name="test_issue79")
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
    return await create_engine(sdl=_SDL, schema_name="test_issue79")


@pytest.mark.asyncio
async def test_issue79(ttftt_engine):
    query = """
    fragment UnknownFields on UnknownType {
        name
    }

    query {
        viewer {
            ...UnknownFields
        }
    }
    """

    assert await ttftt_engine.execute(query) == {
        "data": None,
        "errors": [
            {
                "message": "Unknown type < UnknownType >.",
                "path": None,
                "locations": [{"line": 2, "column": 31}],
                "extensions": {
                    "spec": "June 2018",
                    "rule": "5.5.1.2",
                    "tag": "fragment-spread-type-existence",
                    "details": "https://spec.graphql.org/June2018/#sec-Fragment-Spread-Type-Existence",
                },
            }
        ],
    }
