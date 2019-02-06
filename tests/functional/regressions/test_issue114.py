import pytest


async def _query_dog_resolver(*_args, **__kwargs):
    return {"name": "Doggo"}


async def _query_human_resolver(*_args, **_kwargs):
    return {"name": "Hooman"}


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    resolvers={
        "Query.dog": _query_dog_resolver,
        "Query.human": _query_human_resolver,
    }
)
@pytest.mark.parametrize(
    "query,operation_name,expected",
    [
        (
            """
            query {
              dog {
                name
              }
            }
            """,
            None,
            {"data": {"dog": {"name": "Doggo"}}},
        ),
        (
            """
            query Dog {
              dog {
                name
              }
            }
            """,
            "Dog",
            {"data": {"dog": {"name": "Doggo"}}},
        ),
        (
            """
            query {
              dog {
                name
              }
            }
            """,
            "Dog",
            {
                "data": None,
                "errors": [
                    {
                        "message": "Unknown operation named < Dog >.",
                        "path": None,
                        "locations": [],
                    }
                ],
            },
        ),
        (
            """
            query Dog {
              dog {
                name
              }
            }
            """,
            None,
            {"data": {"dog": {"name": "Doggo"}}},
        ),
        (
            """
            query Dog {
              dog {
                name
              }
            }
            
            query Human {
              human(id: 1) {
                name
              }
            }
            """,
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Must provide operation name if query contains multiple operations.",
                        "path": None,
                        "locations": [],
                    }
                ],
            },
        ),
        (
            """
            query Dog {
              dog {
                name
              }
            }
            
            query Human {
              human(id: 1) {
                name
              }
            }
            """,
            "Dog",
            {"data": {"dog": {"name": "Doggo"}}},
        ),
        (
            """
            query Dog {
              dog {
                name
              }
            }
            
            query Human {
              human(id: 1) {
                name
              }
            }
            """,
            "Human",
            {"data": {"human": {"name": "Hooman"}}},
        ),
        (
            """
            query Dog {
              dog {
                name
              }
            }
            
            query Human {
              human(id: 1) {
                name
              }
            }
            """,
            "Unknown",
            {
                "data": None,
                "errors": [
                    {
                        "message": "Unknown operation named < Unknown >.",
                        "path": None,
                        "locations": [],
                    }
                ],
            },
        ),
    ],
)
async def test_issue114(engine, query, operation_name, expected):
    assert (
        await engine.execute(query, operation_name=operation_name) == expected
    )
