import pytest

from tartiflette.engine import Engine
from tartiflette.resolver import Resolver


@Resolver("Query.dog", schema_name="test_issue86")
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
    
    type MutateDogPayload {
      id: String
    }
    
    type Query {
      dog: Dog
    }
    
    type Mutation {
      mutateDog: MutateDogPayload
    }
    """,
    schema_name="test_issue86",
)


@pytest.mark.asyncio
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
async def test_issue86(query, errors):
    assert await _TTFTT_ENGINE.execute(query) == {
        "data": None,
        "errors": errors,
    }
