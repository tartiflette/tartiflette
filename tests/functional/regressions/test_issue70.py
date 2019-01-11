import pytest


from tartiflette.resolver import Resolver
from tartiflette.engine import Engine


_A_BOBY = {
    "repositories": {
        "edges": [
            {
                "node": {
                    "name": "N1",
                    "owner": {"login": "LOL"},
                    "rascal": {"gigi": "GG", "owner": {"login": "OK"}},
                }
            },
            {
                "node": {
                    "name": "N2",
                    "owner": {"login": "AA"},
                    "rascal": {"gigi": "GGdfs", "owner": {"login": "OssssK"}},
                }
            },
        ]
    },
    "rascal": {"gigi": "GGeeeee", "owner": {"login": "OKssss"}},
}


@Resolver("Query.viewer", schema_name="test_issue70")
async def resolver_query_viewer(*_, **__):
    return _A_BOBY


_TTFTT_ENGINE = Engine(
    """
        type RepositoryOwner {
            login: String
        }

        type Rascal {
            gigi: String
            owner: RepositoryOwner
        }

        type Repository {
            name: String
            owner: RepositoryOwner
            rascal: Rascal
        }

        type RepositoryEdge {
            node: Repository
        }

        type RepositoryConnection {
            edges: [RepositoryEdge]!
        }

        type Viewer {
            repositories(first: Int = 10): RepositoryConnection
            rascal: Rascal
        }

        type Query {
            viewer: Viewer
        }
    """,
    schema_name="test_issue70",
)


@pytest.mark.asyncio
async def test_issue70_okayquery():
    query = """
        fragment OwnerFields on RepositoryOwner {
            login
        }


        fragment SchacalFields on Rascal {
            gigi
            owner {
                ...OwnerFields
            }
        }

        fragment RepositoryBase on Repository {
            name
        }

        fragment RepositoryFields on Repository {
            ...RepositoryBase
            owner {
                login
            }
            rascal {
                ...SchacalFields
            }
        }

        query {
            viewer {
                repositories(first: 10) {
                    edges {
                        node {
                        ...RepositoryFields
                        }
                    }
                }
                rascal {
                    ... on Rascal {
                        gigi
                        owner {
                            login
                        }
                    }
                }
            }
        }
    """

    results = await _TTFTT_ENGINE.execute(query)

    assert results == {
        "data": {
            "viewer": {
                "repositories": {
                    "edges": [
                        {
                            "node": {
                                "name": "N1",
                                "owner": {"login": "LOL"},
                                "rascal": {
                                    "gigi": "GG",
                                    "owner": {"login": "OK"},
                                },
                            }
                        },
                        {
                            "node": {
                                "name": "N2",
                                "owner": {"login": "AA"},
                                "rascal": {
                                    "gigi": "GGdfs",
                                    "owner": {"login": "OssssK"},
                                },
                            }
                        },
                    ]
                },
                "rascal": {"gigi": "GGeeeee", "owner": {"login": "OKssss"}},
            }
        }
    }
