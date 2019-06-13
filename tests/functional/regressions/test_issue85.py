import pytest

from tartiflette import Resolver, create_engine

_SDL = """
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
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Resolver("Query.dog", schema_name="test_issue85")
    async def resolver_query_viewer(*_, **__):
        return {"dog": {"name": "Dog", "owner": {"name": "Human"}}}

    return await create_engine(sdl=_SDL, schema_name="test_issue85")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,errors",
    [
        (
            """
        query getName {
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
                    "message": "Operation name < getName > should be unique.",
                    "path": None,
                    "locations": [
                        {"line": 2, "column": 9},
                        {"line": 8, "column": 9},
                    ],
                }
            ],
        ),
        (
            """
        query getName {
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
                    "message": "Operation name < getName > should be unique.",
                    "path": None,
                    "locations": [
                        {"line": 2, "column": 9},
                        {"line": 8, "column": 9},
                    ],
                },
                {
                    "message": "Operation name < getName > should be unique.",
                    "path": None,
                    "locations": [
                        {"line": 2, "column": 9},
                        {"line": 16, "column": 9},
                    ],
                },
            ],
        ),
    ],
)
async def test_issue85(query, errors, ttftt_engine):
    assert await ttftt_engine.execute(query) == {
        "data": None,
        "errors": errors,
    }
