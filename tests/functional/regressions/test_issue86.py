import pytest

from tartiflette import Resolver


def bakery(schema_name):
    @Resolver("Query.dog", schema_name=schema_name)
    async def resolver_query_dog(*_, **__):
        return {"dog": {"name": "Dog", "owner": {"name": "Human"}}}


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="animals", bakery=bakery)
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
                    "message": "This anonymous operation must be the only defined operation.",
                    "path": None,
                    "locations": [{"line": 2, "column": 13}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.2.2.1",
                        "tag": "lone-anonymous-operation",
                        "details": "https://spec.graphql.org/June2018/#sec-Lone-Anonymous-Operation",
                    },
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
                    "message": "This anonymous operation must be the only defined operation.",
                    "path": None,
                    "locations": [{"line": 10, "column": 13}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.2.2.1",
                        "tag": "lone-anonymous-operation",
                        "details": "https://spec.graphql.org/June2018/#sec-Lone-Anonymous-Operation",
                    },
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
                    "message": "This anonymous operation must be the only defined operation.",
                    "path": None,
                    "locations": [{"line": 2, "column": 13}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.2.2.1",
                        "tag": "lone-anonymous-operation",
                        "details": "https://spec.graphql.org/June2018/#sec-Lone-Anonymous-Operation",
                    },
                },
                {
                    "message": "This anonymous operation must be the only defined operation.",
                    "path": None,
                    "locations": [{"line": 8, "column": 13}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.2.2.1",
                        "tag": "lone-anonymous-operation",
                        "details": "https://spec.graphql.org/June2018/#sec-Lone-Anonymous-Operation",
                    },
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
                    "message": "This anonymous operation must be the only defined operation.",
                    "path": None,
                    "locations": [{"line": 2, "column": 13}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.2.2.1",
                        "tag": "lone-anonymous-operation",
                        "details": "https://spec.graphql.org/June2018/#sec-Lone-Anonymous-Operation",
                    },
                },
                {
                    "message": "This anonymous operation must be the only defined operation.",
                    "path": None,
                    "locations": [{"line": 10, "column": 13}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.2.2.1",
                        "tag": "lone-anonymous-operation",
                        "details": "https://spec.graphql.org/June2018/#sec-Lone-Anonymous-Operation",
                    },
                },
            ],
        ),
    ],
)
async def test_issue86(schema_stack, query, errors):
    assert await schema_stack.execute(query) == {
        "data": None,
        "errors": errors,
    }
