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
    "query,expected",
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
            {
                "data": None,
                "errors": [
                    {
                        "message": "Can't have multiple operations named < getName >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 9},
                            {"line": 8, "column": 9},
                        ],
                        "extensions": {
                            "rule": "5.2.1.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Operation-Name-Uniqueness",
                            "tag": "operation-name-uniqueness",
                        },
                    }
                ],
            },
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
            {
                "data": None,
                "errors": [
                    {
                        "message": "Can't have multiple operations named < getName >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 9},
                            {"line": 8, "column": 9},
                            {"line": 16, "column": 9},
                        ],
                        "extensions": {
                            "rule": "5.2.1.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Operation-Name-Uniqueness",
                            "tag": "operation-name-uniqueness",
                        },
                    }
                ],
            },
        ),
    ],
)
async def test_issue85(query, expected, ttftt_engine):
    assert await ttftt_engine.execute(query) == expected
