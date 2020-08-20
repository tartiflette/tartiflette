import pytest

from tartiflette import Resolver


def bakery(schema_name):
    @Resolver("Query.dog", schema_name=schema_name)
    async def resolve_query_dog(*_args, **__kwargs):
        return {"name": "Doggo"}

    @Resolver("Query.human", schema_name=schema_name)
    async def resolve_query_human(*_args, **_kwargs):
        return {"name": "Hooman"}


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="animals", bakery=bakery)
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
async def test_issue114(schema_stack, query, operation_name, expected):
    assert (
        await schema_stack.execute(query, operation_name=operation_name)
        == expected
    )
