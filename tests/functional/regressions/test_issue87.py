import pytest

from tartiflette.engine import Engine
from tartiflette.resolver import Resolver


@Resolver("Query.dog", schema_name="test_issue87")
async def resolver_query_viewer(*_, **__):
    return {"dog": {"name": "Dog", "owner": {"name": "Human"}}}


_TTFTT_ENGINE = Engine(
    """
    interface Sentient {
      name: String!
    }
    
    interface Pet {
      name: String!
    }
    
    type Human implements Sentient {
      name: String!
    }
    
    type Dog implements Pet {
      name: String!
      owner: Human
    }
    
    type Query {
      dog: Dog
    }
    
    type Subscription {
      newDog: Dog
      newHuman: Human
    }
    """,
    schema_name="test_issue87",
)


@pytest.mark.asyncio
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
async def test_issue87(query, errors):
    print(await _TTFTT_ENGINE.execute(query))
    assert await _TTFTT_ENGINE.execute(query) == {
        "data": None,
        "errors": errors,
    }
