import pytest


@pytest.mark.skip(
    reason=(
        "OverlappingFieldsCanBeMergedRule is raising recursion exception due "
        "to fragment cycles. Should be unskipped once "
        "OverlappingFieldsCanBeMergedRule patched."
    )
)
@pytest.mark.asyncio
@pytest.mark.ttftt_engine
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
                        "message": "Cannot spread fragment < DogFragment > within itself via < aFragment >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 13},
                            {"line": 7, "column": 13},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.5.2.2",
                            "tag": "fragment-spreads-must-not-form-cycles",
                            "details": "https://spec.graphql.org/June2018/#sec-Fragment-spreads-must-not-form-cycles",
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
                        "message": "Cannot spread fragment < DogFragment > within itself via < AnotherFragment >, < aFragment >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 13},
                            {"line": 7, "column": 13},
                            {"line": 11, "column": 13},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.5.2.2",
                            "tag": "fragment-spreads-must-not-form-cycles",
                            "details": "https://spec.graphql.org/June2018/#sec-Fragment-spreads-must-not-form-cycles",
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
                        "message": "Cannot spread fragment < a > within itself via < b >, < c >, < d >, < e >, < f >, < g >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 13},
                            {"line": 7, "column": 13},
                            {"line": 11, "column": 13},
                            {"line": 16, "column": 13},
                            {"line": 21, "column": 13},
                            {"line": 26, "column": 13},
                            {"line": 31, "column": 13},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.5.2.2",
                            "tag": "fragment-spreads-must-not-form-cycles",
                            "details": "https://spec.graphql.org/June2018/#sec-Fragment-spreads-must-not-form-cycles",
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
                            "spec": "June 2018",
                            "rule": "5.5.1.4",
                            "tag": "fragment-must-be-used",
                            "details": "https://spec.graphql.org/June2018/#sec-Fragments-Must-Be-Used",
                        },
                    },
                    {
                        "message": "Fragment < f > is never used.",
                        "path": None,
                        "locations": [{"line": 18, "column": 9}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.5.1.4",
                            "tag": "fragment-must-be-used",
                            "details": "https://spec.graphql.org/June2018/#sec-Fragments-Must-Be-Used",
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
                        "message": "Cannot spread fragment < e > within itself via < f >.",
                        "path": None,
                        "locations": [
                            {"line": 16, "column": 17},
                            {"line": 20, "column": 17},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.5.2.2",
                            "tag": "fragment-spreads-must-not-form-cycles",
                            "details": "https://spec.graphql.org/June2018/#sec-Fragment-spreads-must-not-form-cycles",
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
