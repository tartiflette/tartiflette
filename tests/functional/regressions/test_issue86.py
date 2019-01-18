import pytest


async def resolver_query_viewer(*_, **__):
    return {"dog": {"name": "Dog", "owner": {"name": "Human"}}}


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(resolvers={"Query.dog": resolver_query_viewer})
@pytest.mark.parametrize(
    "query,errors",
    [
        (
            """
            {
              dog {
                name
              }
            }
            
            query getName {
              dog {
                owner {
                  name
                }
              }
            }
            """,
            [
                {
                    "message": "Anonymous operation must be the only defined operation.",
                    "path": None,
                    "locations": [{"line": 2, "column": 13}],
                }
            ],
        ),
        (
            """
            query getName {
              dog {
                owner {
                  name
                }
              }
            }

            {
              dog {
                name
              }
            }
            """,
            [
                {
                    "message": "Anonymous operation must be the only defined operation.",
                    "path": None,
                    "locations": [{"line": 10, "column": 13}],
                }
            ],
        ),
        (
            """
            {
              dog {
                name
              }
            }
            
            query {
              dog {
                owner {
                  name
                }
              }
            }
            """,
            [
                {
                    "message": "Anonymous operation must be the only defined operation.",
                    "path": None,
                    "locations": [{"line": 2, "column": 13}],
                },
                {
                    "message": "Anonymous operation must be the only defined operation.",
                    "path": None,
                    "locations": [{"line": 8, "column": 13}],
                },
            ],
        ),
        (
            """
            query {
              dog {
                owner {
                  name
                }
              }
            }

            {
              dog {
                name
              }
            }
            """,
            [
                {
                    "message": "Anonymous operation must be the only defined operation.",
                    "path": None,
                    "locations": [{"line": 2, "column": 13}],
                },
                {
                    "message": "Anonymous operation must be the only defined operation.",
                    "path": None,
                    "locations": [{"line": 10, "column": 13}],
                },
            ],
        ),
    ],
)
async def test_issue86(engine, query, errors):
    assert await engine.execute(query) == {"data": None, "errors": errors}
