import pytest

from tartiflette import Engine, Resolver

_A_BOBY = {
    "repositories": {
        "edges": [
            {
                "node": {
                    "name": "N1",
                    "owner": {
                        "login": "LOL",
                        "bob": {
                            "c": 1,
                            "d": {"e": 3.6, "petaleColor": "Blue"},
                        },
                    },
                    "rascal": {
                        "gigi": "GG",
                        "owner": {
                            "login": "OK",
                            "bob": {
                                "c": 9,
                                "d": {"e": 33.6, "petaleColor": "Green"},
                            },
                        },
                    },
                }
            },
            {
                "node": {
                    "name": "N2",
                    "owner": {
                        "login": "AA",
                        "bob": {
                            "c": 17,
                            "d": {"e": 0.66, "petaleColor": "Purple"},
                        },
                    },
                    "rascal": {
                        "gigi": "GGdfs",
                        "owner": {
                            "login": "OssssK",
                            "bob": {
                                "c": 99,
                                "d": {"e": 2.6, "petaleColor": "Black"},
                            },
                        },
                    },
                }
            },
        ]
    },
    "rascal": {
        "gigi": "GGeeeee",
        "owner": {
            "login": "OKssss",
            "bob": {"c": 30, "d": {"e": 54564.3, "petaleColor": "Red"}},
        },
    },
}


@Resolver("Query.viewer", schema_name="test_issue70")
async def resolver_query_viewer(*_, **__):
    return _A_BOBY


_TTFTT_ENGINE = Engine(
    """
        type Fleur {
            e: Float
            petaleColor: String
        }

        type Ninja {
            c: Int
            d: Fleur
        }

        type RepositoryOwner {
            login: String
            bob: Ninja
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
            bob {
                c
                d {
                    e
                    petaleColor
                }
            }
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
                bob {
                    c
                    d {
                        e
                        petaleColor
                    }
                }
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
                        ... RepositoryFields
                        }
                    }
                }
                rascal {
                    ... on Rascal {
                        gigi
                        owner {
                            login
                            bob {
                                c
                                d {
                                    e
                                    petaleColor
                                }
                            }
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
                                "owner": {
                                    "login": "LOL",
                                    "bob": {
                                        "c": 1,
                                        "d": {"e": 3.6, "petaleColor": "Blue"},
                                    },
                                },
                                "rascal": {
                                    "gigi": "GG",
                                    "owner": {
                                        "login": "OK",
                                        "bob": {
                                            "c": 9,
                                            "d": {
                                                "e": 33.6,
                                                "petaleColor": "Green",
                                            },
                                        },
                                    },
                                },
                            }
                        },
                        {
                            "node": {
                                "name": "N2",
                                "owner": {
                                    "login": "AA",
                                    "bob": {
                                        "c": 17,
                                        "d": {
                                            "e": 0.66,
                                            "petaleColor": "Purple",
                                        },
                                    },
                                },
                                "rascal": {
                                    "gigi": "GGdfs",
                                    "owner": {
                                        "login": "OssssK",
                                        "bob": {
                                            "c": 99,
                                            "d": {
                                                "e": 2.6,
                                                "petaleColor": "Black",
                                            },
                                        },
                                    },
                                },
                            }
                        },
                    ]
                },
                "rascal": {
                    "gigi": "GGeeeee",
                    "owner": {
                        "login": "OKssss",
                        "bob": {
                            "c": 30,
                            "d": {"e": 54564.3, "petaleColor": "Red"},
                        },
                    },
                },
            }
        }
    }


@pytest.mark.asyncio
async def test_issue70_fragment_in_inline():
    query = """
    fragment OwnerFields on RepositoryOwner {
        login
        bob {
            c
            d {
                e
                petaleColor
            }
        }
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

    query {
        viewer {
            repositories(first: 10) {
                edges {
                    node {
                        ... on Repository {
                            ...RepositoryBase
                            owner {
                                login
                                bob {
                                    c
                                    d {
                                        e
                                        petaleColor
                                    }
                                }
                            }
                            rascal {
                                ...SchacalFields
                            }
                        }
                    }
                }
            }
            rascal {
                ... on Rascal {
                    gigi
                    owner {
                        login
                        bob {
                            c
                            d {
                                e
                                petaleColor
                            }
                        }
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
                                "rascal": {
                                    "owner": {
                                        "login": "OK",
                                        "bob": {
                                            "d": {
                                                "petaleColor": "Green",
                                                "e": 33.6,
                                            },
                                            "c": 9,
                                        },
                                    },
                                    "gigi": "GG",
                                },
                                "owner": {
                                    "login": "LOL",
                                    "bob": {
                                        "c": 1,
                                        "d": {"petaleColor": "Blue", "e": 3.6},
                                    },
                                },
                                "name": "N1",
                            }
                        },
                        {
                            "node": {
                                "rascal": {
                                    "gigi": "GGdfs",
                                    "owner": {
                                        "bob": {
                                            "d": {
                                                "e": 2.6,
                                                "petaleColor": "Black",
                                            },
                                            "c": 99,
                                        },
                                        "login": "OssssK",
                                    },
                                },
                                "owner": {
                                    "bob": {
                                        "c": 17,
                                        "d": {
                                            "petaleColor": "Purple",
                                            "e": 0.66,
                                        },
                                    },
                                    "login": "AA",
                                },
                                "name": "N2",
                            }
                        },
                    ]
                },
                "rascal": {
                    "gigi": "GGeeeee",
                    "owner": {
                        "login": "OKssss",
                        "bob": {
                            "d": {"e": 54564.3, "petaleColor": "Red"},
                            "c": 30,
                        },
                    },
                },
            }
        }
    }


@pytest.mark.asyncio
async def test_issue70_fragment_in_inline_in_fragment():
    query = """

    fragment FleurFragment on Fleur {
        e
        petaleColor
    }

    fragment OwnerFields on RepositoryOwner {
        login
        bob {
            ... on Ninja {
                d {
                    ...FleurFragment
                }
            }
        }
    }

    query {
        viewer {
            repositories(first: 10) {
                edges {
                    node {
                        name
                        owner {
                            ...OwnerFields
                        }
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
                                "owner": {
                                    "bob": {
                                        "d": {"petaleColor": "Blue", "e": 3.6}
                                    },
                                    "login": "LOL",
                                },
                            }
                        },
                        {
                            "node": {
                                "owner": {
                                    "bob": {
                                        "d": {
                                            "petaleColor": "Purple",
                                            "e": 0.66,
                                        }
                                    },
                                    "login": "AA",
                                },
                                "name": "N2",
                            }
                        },
                    ]
                }
            }
        }
    }


@pytest.mark.asyncio
async def test_issue70_dont_execute_fragment_on_wrong_type():
    query = """

    fragment FleurFragment on Rascal {
        e
        petaleColor
    }

    fragment OwnerFields on RepositoryOwner {
        login
        bob {
            ... on Ninja {
                d {
                    ...FleurFragment
                }
            }
        }
    }

    query {
        viewer {
            repositories(first: 10) {
                edges {
                    node {
                        name
                        owner {
                            ...OwnerFields
                        }
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
                                "owner": {"bob": {"d": {}}, "login": "LOL"},
                            }
                        },
                        {
                            "node": {
                                "owner": {"bob": {"d": {}}, "login": "AA"},
                                "name": "N2",
                            }
                        },
                    ]
                }
            }
        }
    }
