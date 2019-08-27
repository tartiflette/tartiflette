import pytest


@pytest.mark.asyncio
@pytest.mark.ttftt_engine
@pytest.mark.parametrize(
    "query,errors",
    [
        (
            """
            query {
              cat {
                name
                doesKnowCommand(catCommand: JUMP, catCommand: JUMP)
              }
            }
            """,
            [
                {
                    "message": "Can't have multiple arguments named < catCommand >.",
                    "path": ["cat", "doesKnowCommand"],
                    "locations": [
                        {"line": 5, "column": 33},
                        {"line": 5, "column": 51},
                    ],
                    "extensions": {
                        "rule": "5.4.2",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Uniqueness",
                        "tag": "argument-uniqueness",
                    },
                }
            ],
        ),
        (
            """
            query {
              cat {
                name
                doesKnowCommand(catCommand: JUMP, catCommand: JUMP, catCommand: JUMP)
              }
            }
            """,
            [
                {
                    "message": "Can't have multiple arguments named < catCommand >.",
                    "path": ["cat", "doesKnowCommand"],
                    "locations": [
                        {"line": 5, "column": 33},
                        {"line": 5, "column": 51},
                        {"line": 5, "column": 69},
                    ],
                    "extensions": {
                        "rule": "5.4.2",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Uniqueness",
                        "tag": "argument-uniqueness",
                    },
                }
            ],
        ),
        (
            """
            query {
              cat {
                name @deprecated(reason: "first", reason: "second")
              }
            }
            """,
            [
                {
                    "message": "Can't have multiple arguments named < reason >.",
                    "path": ["cat", "name"],
                    "locations": [
                        {"line": 4, "column": 34},
                        {"line": 4, "column": 51},
                    ],
                    "extensions": {
                        "rule": "5.4.2",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Uniqueness",
                        "tag": "argument-uniqueness",
                    },
                },
                {
                    "message": "Directive < @deprecated > is not used in a valid location.",
                    "path": ["cat", "name"],
                    "locations": [
                        {"line": 4, "column": 17},
                        {"line": 4, "column": 22},
                    ],
                    "extensions": {
                        "rule": "5.7.2",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                        "tag": "directives-are-in-valid-locations",
                    },
                },
            ],
        ),
        (
            """
            query {
              cat {
                name @deprecated(reason: "first", reason: "second", reason: "third")
              }
            }
            """,
            [
                {
                    "message": "Can't have multiple arguments named < reason >.",
                    "path": ["cat", "name"],
                    "locations": [
                        {"line": 4, "column": 34},
                        {"line": 4, "column": 51},
                        {"line": 4, "column": 69},
                    ],
                    "extensions": {
                        "rule": "5.4.2",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Uniqueness",
                        "tag": "argument-uniqueness",
                    },
                },
                {
                    "message": "Directive < @deprecated > is not used in a valid location.",
                    "path": ["cat", "name"],
                    "locations": [
                        {"line": 4, "column": 17},
                        {"line": 4, "column": 22},
                    ],
                    "extensions": {
                        "rule": "5.7.2",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                        "tag": "directives-are-in-valid-locations",
                    },
                },
            ],
        ),
    ],
)
async def test_issue99(engine, query, errors):
    assert await engine.execute(query) == {"data": None, "errors": errors}
