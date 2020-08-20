import pytest

from tartiflette import Resolver


def bakery(schema_name):
    @Resolver("Query.viewer", schema_name=schema_name)
    async def resolver_query_viewer(*_, **__):
        return {
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
                                    "d": {"e": 0.66, "petaleColor": "Purple"},
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


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
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
    bakery=bakery,
)
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
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
            """,
            {
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
                                                "d": {
                                                    "e": 3.6,
                                                    "petaleColor": "Blue",
                                                },
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
            },
        ),
        (
            """
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
            """,
            {
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
                                                "d": {
                                                    "petaleColor": "Blue",
                                                    "e": 3.6,
                                                },
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
            },
        ),
        (
            """
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
            """,
            {
                "data": {
                    "viewer": {
                        "repositories": {
                            "edges": [
                                {
                                    "node": {
                                        "name": "N1",
                                        "owner": {
                                            "bob": {
                                                "d": {
                                                    "petaleColor": "Blue",
                                                    "e": 3.6,
                                                }
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
            },
        ),
        (
            """
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
            """,
            {
                "data": {
                    "viewer": {
                        "repositories": {
                            "edges": [
                                {
                                    "node": {
                                        "name": "N1",
                                        "owner": {
                                            "bob": {
                                                "d": {
                                                    "petaleColor": "Blue",
                                                    "e": 3.6,
                                                }
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
            },
        ),
        (
            """
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
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot query field < e > on type < Rascal >.",
                        "path": None,
                        "locations": [{"line": 3, "column": 17}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
                    },
                    {
                        "message": "Cannot query field < petaleColor > on type < Rascal >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 17}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
                    },
                    {
                        "message": "Fragment < FleurFragment > cannot be spread here as objects of type < Fleur > can never be of type < Rascal >.",
                        "path": None,
                        "locations": [{"line": 12, "column": 29}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.5.2.3",
                            "tag": "fragment-spread-is-possible",
                            "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-is-possible",
                        },
                    },
                ],
            },
        ),
    ],
)
async def test_issue70(schema_stack, query, expected):
    assert await schema_stack.execute(query) == expected
