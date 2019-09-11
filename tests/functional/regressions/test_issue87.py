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
                    "message": "Subcription Sub must select only one top level field.",
                    "path": None,
                    "locations": [
                        {"line": 2, "column": 13},
                        {"line": 2, "column": 30},
                    ],
                    "extensions": {
                        "rule": "5.2.3.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Single-root-field",
                        "tag": "single-root-field",
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
                    "message": "Subcription Sub must select only one top level field.",
                    "path": None,
                    "locations": [
                        {"line": 2, "column": 13},
                        {"line": 2, "column": 30},
                    ],
                    "extensions": {
                        "rule": "5.2.3.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Single-root-field",
                        "tag": "single-root-field",
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
                    "message": "Subcription Sub must select only one top level field.",
                    "path": None,
                    "locations": [
                        {"line": 11, "column": 13},
                        {"line": 2, "column": 66},
                    ],
                    "extensions": {
                        "rule": "5.2.3.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Single-root-field",
                        "tag": "single-root-field",
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
                    "message": "Subcription Sub must select only one top level field.",
                    "path": None,
                    "locations": [
                        {"line": 2, "column": 13},
                        {"line": 3, "column": 35},
                    ],
                    "extensions": {
                        "rule": "5.2.3.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Single-root-field",
                        "tag": "single-root-field",
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
              }
            }

            subscription Sub {
              ...MultipleSubscriptionsFields
            }
            """,
            [
                {
                    "message": "Subcription Sub must select only one top level field.",
                    "path": None,
                    "locations": [
                        {"line": 13, "column": 13},
                        {"line": 3, "column": 35},
                    ],
                    "extensions": {
                        "rule": "5.2.3.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Single-root-field",
                        "tag": "single-root-field",
                    },
                }
            ],
        ),
    ],
)
async def test_issue87(engine, query, errors):
    assert await engine.execute(query) == {"data": None, "errors": errors}
