import pytest

from tartiflette import Resolver

_DATAS = {
    "repositories": {
        "edges": [{"node": {"name": "A"}}, {"node": {"name": "b"}}]
    }
}


def bakery(schema_name):
    @Resolver("Query.viewer", schema_name=schema_name)
    async def resolver_query_viewer(*_, **__):
        return _DATAS


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
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
    bakery=bakery,
)
async def test_issue71(schema_stack):
    assert await schema_stack.execute("query {{}") == {
        "data": None,
        "errors": [
            {
                "locations": [],
                "message": "1.8: syntax error, unexpected {",
                "path": None,
            }
        ],
    }

    assert (
        await schema_stack.execute(
            """
            query { viewer { repositories { edges { node { name } } } } }
            """
        )
        == {
            "data": {
                "viewer": {
                    "repositories": {
                        "edges": [
                            {"node": {"name": "A"}},
                            {"node": {"name": "b"}},
                        ]
                    }
                }
            }
        }
    )
