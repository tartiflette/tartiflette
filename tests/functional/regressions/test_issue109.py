import pytest


@pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query {
                dog {
                    name {
                        a
                    }
                }
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "field < name > is a leaf and thus can't have a selection set",
                        "path": ["dog", "name"],
                        "locations": [{"line": 4, "column": 21}],
                    }
                ],
            },
        ),
        (
            """
            query {
                dog
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "field < dog > is not a leaf and thus must have a selection set",
                        "path": ["dog"],
                        "locations": [{"line": 3, "column": 17}],
                    }
                ],
            },
        ),
        (
            """
            fragment doggy on Dog {
                name {
                    a
                }
            }
            query {
                dog {
                    ... doggy
                }
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "field < name > is a leaf and thus can't have a selection set",
                        "path": ["dog", "name"],
                        "locations": [{"line": 3, "column": 17}],
                    }
                ],
            },
        ),
        (
            """
            query {
                dog {
                    ... on Dog {
                        name {
                            a
                        }
                    }
                }
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "field < name > is a leaf and thus can't have a selection set",
                        "path": ["dog", "name"],
                        "locations": [{"line": 5, "column": 25}],
                    }
                ],
            },
        ),
    ],
)
@pytest.mark.ttftt_engine()
async def test_issue109(query, expected, engine):
    assert await engine.execute(query) == expected
