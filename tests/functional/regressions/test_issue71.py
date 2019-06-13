import pytest

from tartiflette import Resolver, create_engine

_DATAS = {
    "repositories": {
        "edges": [{"node": {"name": "A"}}, {"node": {"name": "b"}}]
    }
}

_SDL = """
type RepositoryOwner {
    login: String
}

type Repository {
    name: String
    owner: RepositoryOwner
}

type RepositoryEdge {
    node: Repository
}

type RepositoryConnection {
    edges: [RepositoryEdge]!
}

type Viewer {
    repositories(first: Int = 10): RepositoryConnection
}

type Query {
    viewer: Viewer
}
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Resolver("Query.viewer", schema_name="test_issue71")
    async def resolver_query_viewer(*_, **__):
        return _DATAS

    return await create_engine(sdl=_SDL, schema_name="test_issue71")


@pytest.mark.asyncio
async def test_issue71(ttftt_engine):
    query = """
        query {{}
    """

    results = await ttftt_engine.execute(query)
    assert results == {
        "data": None,
        "errors": [
            {
                "locations": [],
                "message": "2.16: syntax error, unexpected {",
                "path": None,
            }
        ],
    }
    query = """
        query { viewer { repositories { edges { node { name } } } } }
    """
    results = await ttftt_engine.execute(query)

    assert results == {
        "data": {
            "viewer": {
                "repositories": {
                    "edges": [{"node": {"name": "A"}}, {"node": {"name": "b"}}]
                }
            }
        }
    }
