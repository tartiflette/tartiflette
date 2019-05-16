import pytest


async def resolver_query_viewer(*_, **__):
    return {"dog": {"name": "Dog", "owner": {"name": "Human"}}}


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(resolvers={"Query.dog": resolver_query_viewer})
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
                    "extensions": {
                        "rule": "5.2.2.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Lone-Anonymous-Operation",
                        "tag": "lone-anonymous-operation",
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
                    "message": "Anonymous operation must be the only defined operation.",
                    "path": None,
                    "locations": [{"line": 10, "column": 13}],
                    "extensions": {
                        "rule": "5.2.2.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Lone-Anonymous-Operation",
                        "tag": "lone-anonymous-operation",
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
                    "message": "Anonymous operation must be the only defined operation.",
                    "path": None,
                    "locations": [
                        {"line": 2, "column": 13},
                        {"line": 8, "column": 13},
                    ],
                    "extensions": {
                        "rule": "5.2.2.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Lone-Anonymous-Operation",
                        "tag": "lone-anonymous-operation",
                    },
                }
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
                    "locations": [
                        {"line": 2, "column": 13},
                        {"line": 10, "column": 13},
                    ],
                    "extensions": {
                        "rule": "5.2.2.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Lone-Anonymous-Operation",
                        "tag": "lone-anonymous-operation",
                    },
                }
            ],
        ),
    ],
)
async def test_issue86(engine, query, errors):
    assert await engine.execute(query) == {"data": None, "errors": errors}
