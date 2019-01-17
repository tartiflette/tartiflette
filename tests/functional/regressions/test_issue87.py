import pytest

from tartiflette.resolver import Resolver


@Resolver("Query.dog")
async def resolver_query_viewer(*_, **__):
    return {"dog": {"name": "Dog", "owner": {"name": "Human"}}}


@pytest.mark.asyncio
@pytest.mark.ttftt_engine
@pytest.mark.parametrize(
    "query,errors",
    [
        (
            """
            subscription Sub {
              newDog {
                name
              }
              newHuman {
                name
              }
            }
            """,
            [
                {
                    "message": "Subscription operations must have exactly one root field.",
                    "path": None,
                    "locations": [{"line": 2, "column": 13}],
                }
            ],
        ),
        (
            """
            subscription Sub {
              newDog {
                name
              }
              __typename
            }
            """,
            [
                {
                    "message": "Subscription operations must have exactly one root field.",
                    "path": None,
                    "locations": [{"line": 2, "column": 13}],
                }
            ],
        ),
        (
            """
            fragment MultipleSubscriptionsFields on Subscription {
              newDog {
                name
              }
              newHuman {
                name
              }
            }
            
            subscription Sub {
              ...MultipleSubscriptionsFields
            }
            """,
            [
                {
                    "message": "Subscription operations must have exactly one root field.",
                    "path": None,
                    "locations": [{"line": 11, "column": 13}],
                }
            ],
        ),
        (
            """
            subscription Sub {
              ... on Subscription {
                newDog {
                  name
                }
                newHuman {
                  name
                }
              }
            }
            """,
            [
                {
                    "message": "Subscription operations must have exactly one root field.",
                    "path": None,
                    "locations": [{"line": 2, "column": 13}],
                }
            ],
        ),
        (
            """
            fragment MultipleSubscriptionsFields on Subscription {
              ... on Subscription {
                newDog {
                  name
                }
                newHuman {
                  name
                }
              }
            }
            
            subscription Sub {
              ...MultipleSubscriptionsFields
            }
            """,
            [
                {
                    "message": "Subscription operations must have exactly one root field.",
                    "path": None,
                    "locations": [{"line": 13, "column": 13}],
                }
            ],
        ),
    ],
)
async def test_issue87(engine, query, errors):
    assert await engine.execute(query) == {"data": None, "errors": errors}
