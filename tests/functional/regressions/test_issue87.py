import pytest


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
                    "message": "Subscription < Sub > must select only one top level field.",
                    "path": None,
                    "locations": [{"line": 6, "column": 15}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.2.3.1",
                        "tag": "single-root-field",
                        "details": "https://spec.graphql.org/June2018/#sec-Single-root-field",
                    },
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
                    "message": "Subscription < Sub > must select only one top level field.",
                    "path": None,
                    "locations": [{"line": 6, "column": 15}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.2.3.1",
                        "tag": "single-root-field",
                        "details": "https://spec.graphql.org/June2018/#sec-Single-root-field",
                    },
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
                    "message": "Subscription < Sub > must select only one top level field.",
                    "path": None,
                    "locations": [{"line": 6, "column": 15}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.2.3.1",
                        "tag": "single-root-field",
                        "details": "https://spec.graphql.org/June2018/#sec-Single-root-field",
                    },
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
                    "message": "Subscription < Sub > must select only one top level field.",
                    "path": None,
                    "locations": [{"line": 7, "column": 17}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.2.3.1",
                        "tag": "single-root-field",
                        "details": "https://spec.graphql.org/June2018/#sec-Single-root-field",
                    },
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
                newAlien {
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
                    "message": "Subscription < Sub > must select only one top level field.",
                    "path": None,
                    "locations": [
                        {"line": 7, "column": 17},
                        {"line": 10, "column": 17},
                    ],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.2.3.1",
                        "tag": "single-root-field",
                        "details": "https://spec.graphql.org/June2018/#sec-Single-root-field",
                    },
                }
            ],
        ),
    ],
)
async def test_issue87(engine, query, errors):
    assert await engine.execute(query) == {"data": None, "errors": errors}
