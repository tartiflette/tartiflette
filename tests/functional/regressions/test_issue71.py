import pytest


from tartiflette.resolver import Resolver
from tartiflette.engine import Engine


_DATAS = {
    "repositories": {
        "edges": [{"node": {"name": "A"}}, {"node": {"name": "b"}}]
    }
}


@Resolver("Query.viewer", schema_name="test_issue71")
async def resolver_query_viewer(*_, **__):
    return _DATAS


_TTFTT_ENGINE = Engine(
    """
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
    """,
    schema_name="test_issue71",
)


@pytest.mark.asyncio
async def test_issue70_fragment_in_inline():
    query = """
        query { {}
    """

    results = await _TTFTT_ENGINE.execute(query)
    assert results == {
        "data": None,
        "errors": [
            {
                "locations": [],
                "message": "2.16: unrecognized character \\xc2",
                "path": None,
            }
        ],
    }
    query = """
        query { viewer { repositories { edges { node { name } } } } }
    """
    results = await _TTFTT_ENGINE.execute(query)

    assert results == {
        "data": {
            "viewer": {
                "repositories": {
                    "edges": [{"node": {"name": "A"}}, {"node": {"name": "b"}}]
                }
            }
        }
    }
