import pytest


@pytest.mark.asyncio
@pytest.mark.ttftt_engine()
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
        fragment DogFragment on Dog {
            ...aFragment
        }

        fragment aFragment on Dog {
            ...DogFragment
            name
        }

        query lol {
            dog {
                ...DogFragment
            }
        }
        """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Fragment Cylcle Detected",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 9},
                            {"line": 6, "column": 9},
                        ],
                        "extensions": {
                            "rule": "5.5.2.2",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-spreads-must-not-form-cycles",
                            "tag": "fragment-spreads-must-not-form-cycles",
                        },
                    }
                ],
            },
        ),
        (
            """
        fragment DogFragment on Dog {
            ...AnotherFragment
        }

        fragment AnotherFragment on Dog {
            ...aFragment
        }

        fragment aFragment on Dog {
            ...DogFragment
            name
        }

        query lol {
            dog {
                ...DogFragment
            }
        }
        """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Fragment Cylcle Detected",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 9},
                            {"line": 6, "column": 9},
                            {"line": 10, "column": 9},
                        ],
                        "extensions": {
                            "rule": "5.5.2.2",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-spreads-must-not-form-cycles",
                            "tag": "fragment-spreads-must-not-form-cycles",
                        },
                    }
                ],
            },
        ),
        (
            """
        fragment a on Dog {
            ...b
        }

        fragment b on Dog {
            ...c
        }

        fragment c on Dog {
            ...d
            name
        }

        fragment d on Dog {
            ...e
            name
        }

        fragment e on Dog {
            ...f
            name
        }

        fragment f on Dog {
            ...g
            name
        }

        fragment g on Dog {
            ...a
            name
        }

        query lol {
            dog {
                ...a
            }
        }
        """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Fragment Cylcle Detected",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 9},
                            {"line": 6, "column": 9},
                            {"line": 10, "column": 9},
                            {"line": 15, "column": 9},
                            {"line": 20, "column": 9},
                            {"line": 25, "column": 9},
                            {"line": 30, "column": 9},
                        ],
                        "extensions": {
                            "rule": "5.5.2.2",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-spreads-must-not-form-cycles",
                            "tag": "fragment-spreads-must-not-form-cycles",
                        },
                    }
                ],
            },
        ),
        (
            """
        fragment a on Dog {
            ...b
        }

        fragment b on Dog {
            ...c
        }

        fragment c on Dog {
            name
        }

        fragment e on Dog {
            ...b
        }

        fragment f on Dog {
            ...c
        }

        query lol {
            dog {
                ...a
            }
        }
        """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Fragment < e > is never used.",
                        "path": None,
                        "locations": [{"line": 14, "column": 9}],
                        "extensions": {
                            "rule": "5.5.1.4",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Fragments-Must-Be-Used",
                            "tag": "fragment-must-be-used",
                        },
                    },
                    {
                        "message": "Fragment < f > is never used.",
                        "path": None,
                        "locations": [{"line": 18, "column": 9}],
                        "extensions": {
                            "rule": "5.5.1.4",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Fragments-Must-Be-Used",
                            "tag": "fragment-must-be-used",
                        },
                    },
                ],
            },
        ),
        (
            """
            fragment a on Dog {
                ...b
            }

            fragment b on Dog {
                ...c
            }

            fragment c on Dog {
                name
                ...e
            }

            fragment e on Dog {
                ...f
            }

            fragment f on Dog {
                ...e
            }

            query lol {
                dog {
                    ...a
                }
            }
        """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Fragment Cylcle Detected",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 13},
                            {"line": 6, "column": 13},
                            {"line": 10, "column": 13},
                            {"line": 15, "column": 13},
                            {"line": 19, "column": 13},
                        ],
                        "extensions": {
                            "rule": "5.5.2.2",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-spreads-must-not-form-cycles",
                            "tag": "fragment-spreads-must-not-form-cycles",
                        },
                    }
                ],
            },
        ),
    ],
)
async def test_validators_fragment_spreads_must_not_form_cycles(
    query, expected, engine
):
    assert await engine.execute(query) == expected
