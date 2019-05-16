import pytest


async def _resolver(*args, **kwargs):
    return {
        "name": "a",
        "nickname": "n",
        "barkVolume": 25,
        "owner": {"name": "owen"},
    }


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(resolvers={"Query.dog": _resolver})
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
    query {
            dog {
                name @skip(if: true)
                nickname @include(if: true)
                barkVolume
            }
        }
    """,
            {"data": {"dog": {"barkVolume": 25, "nickname": "n"}}},
        ),
        (
            """
    query {
            dog {
                name @skip(if: true)
                nickname @include(if: false)
                barkVolume @skip(if: true)
            }
        }
    """,
            {"data": {"dog": {}}},
        ),
        (
            """
    query {
            dog {
                name @skip(if: false)
                nickname @include(if: false)
                barkVolume
            }
        }
    """,
            {"data": {"dog": {"barkVolume": 25, "name": "a"}}},
        ),
        (
            """
    query {
            dog {
                name @skip(if: false) @include(if: true)
                nickname
                barkVolume
            }
        }
    """,
            {
                "data": {
                    "dog": {"barkVolume": 25, "name": "a", "nickname": "n"}
                }
            },
        ),
        (
            """
    query {
            dog {
                name @skip(if: false) @include(if: false)
                nickname
                barkVolume
            }
        }
    """,
            {"data": {"dog": {"barkVolume": 25, "nickname": "n"}}},
        ),
        (
            """
    query {
            dog {
                name @skip(if: true) @include(if: false)
                nickname
                barkVolume
            }
        }
    """,
            {"data": {"dog": {"barkVolume": 25, "nickname": "n"}}},
        ),
        (
            """
    query {
            dog {
                name @skip(if: true) @include(if: true)
                nickname
                barkVolume
            }
        }
    """,
            {"data": {"dog": {"barkVolume": 25, "nickname": "n"}}},
        ),
        (
            """
    query {
            dog @skip(if: true) {
                name
                nickname
                barkVolume
            }
        }
    """,
            {"data": {}},
        ),
        (
            """
    query {
            dog @skip(if: false) {
                name
                nickname
                barkVolume
            }
        }
    """,
            {
                "data": {
                    "dog": {"name": "a", "nickname": "n", "barkVolume": 25}
                }
            },
        ),
        (
            """
    query {
            dog @include(if: false) {
                name
                nickname
                barkVolume
            }
        }
    """,
            {"data": {}},
        ),
        (
            """
    query {
            dog @include(if: true) {
                name
                nickname
                barkVolume
            }
        }
    """,
            {
                "data": {
                    "dog": {"name": "a", "nickname": "n", "barkVolume": 25}
                }
            },
        ),
        (
            """
    query {
        dog {
            ... @include(if: true) {
                name
                nickname
                barkVolume
            }
            owner {
                name
            }
        }
    }
    """,
            {
                "data": {
                    "dog": {
                        "owner": {"name": "owen"},
                        "name": "a",
                        "nickname": "n",
                        "barkVolume": 25,
                    }
                }
            },
        ),
        (
            """
    query {
        dog {
            ... @include(if: false) {
                name
                nickname
                barkVolume
            }
            owner {
                name
            }
        }
    }
    """,
            {"data": {"dog": {"owner": {"name": "owen"}}}},
        ),
        (
            """
    fragment DogFragment on Dog {
        name
        nickname
        barkVolume
    }

    query {
        dog {
            ... DogFragment @include(if: true)
            owner {
                name
            }
        }
    }
    """,
            {
                "data": {
                    "dog": {
                        "owner": {"name": "owen"},
                        "name": "a",
                        "nickname": "n",
                        "barkVolume": 25,
                    }
                }
            },
        ),
        (
            """
    fragment DogFragment on Dog {
        name
        nickname
        barkVolume
    }

    query {
        dog {
            ... DogFragment @include(if: false)
            owner {
                name
            }
        }
    }
    """,
            {"data": {"dog": {"owner": {"name": "owen"}}}},
        ),
        (
            """
    fragment DogFragment on Dog {
        name
        nickname @skip(if: true)
        barkVolume
    }

    query {
        dog {
            ... @include(if: true) {
                ... DogFragment @include(if: true)
            }
            owner {
                name
            }
        }
    }
    """,
            {
                "data": {
                    "dog": {
                        "owner": {"name": "owen"},
                        "name": "a",
                        "barkVolume": 25,
                    }
                }
            },
        ),
        (
            """
    fragment DogFragment on Dog {
        name
        nickname @skip(if: true)
        barkVolume
    }

    query {
        dog {
            ... @include(if: true) {
                ... DogFragment @include(if: false)
            }
            owner {
                name
            }
        }
    }
    """,
            {"data": {"dog": {"owner": {"name": "owen"}}}},
        ),
        (
            """
    fragment DogFragment on Dog {
        name
        nickname @skip(if: true)
        barkVolume
    }

    query {
        dog {
            ... @include(if: false) {
                ... DogFragment @include(if: true)
            }
            owner {
                name
            }
        }
    }
    """,
            {"data": {"dog": {"owner": {"name": "owen"}}}},
        ),
    ],
)
async def test_issue158(engine, query, expected):
    assert await engine.execute(query) == expected
