import pytest

from tartiflette import Resolver


def bakery(schema_name):
    @Resolver("Query.dog", schema_name=schema_name)
    async def resolver_query_viewer(*_, **__):
        return {"dog": {"name": "Dog", "owner": {"name": "Human"}}}


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
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
    bakery=bakery,
)
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
                        "message": "There can be only one operation named < getName >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 8, "column": 15},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.2.1.1",
                            "tag": "operation-name-uniqueness",
                            "details": "https://spec.graphql.org/June2018/#sec-Operation-Name-Uniqueness",
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
                        "message": "There can be only one operation named < getName >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 8, "column": 15},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.2.1.1",
                            "tag": "operation-name-uniqueness",
                            "details": "https://spec.graphql.org/June2018/#sec-Operation-Name-Uniqueness",
                        },
                    },
                    {
                        "message": "There can be only one operation named < getName >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 16, "column": 15},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.2.1.1",
                            "tag": "operation-name-uniqueness",
                            "details": "https://spec.graphql.org/June2018/#sec-Operation-Name-Uniqueness",
                        },
                    },
                ],
            },
        ),
    ],
)
async def test_issue85(schema_stack, query, expected):
    assert await schema_stack.execute(query) == expected
