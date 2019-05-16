import pytest


# TODO: unskip this test once `validate_document` function has been implemented
@pytest.mark.skip(
    reason="Will handled by the `validate_document` function which isn't implemented yet."
)
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
