import pytest


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="animals")
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
                    "message": "There can be only one argument named < catCommand >.",
                    "path": None,
                    "locations": [
                        {"line": 5, "column": 33},
                        {"line": 5, "column": 51},
                    ],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.2",
                        "tag": "argument-uniqueness",
                        "details": "http://spec.graphql.org/June2018/#sec-Argument-Uniqueness",
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
                    "message": "There can be only one argument named < catCommand >.",
                    "path": None,
                    "locations": [
                        {"line": 5, "column": 33},
                        {"line": 5, "column": 51},
                    ],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.2",
                        "tag": "argument-uniqueness",
                        "details": "http://spec.graphql.org/June2018/#sec-Argument-Uniqueness",
                    },
                },
                {
                    "message": "There can be only one argument named < catCommand >.",
                    "path": None,
                    "locations": [
                        {"line": 5, "column": 33},
                        {"line": 5, "column": 69},
                    ],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.2",
                        "tag": "argument-uniqueness",
                        "details": "http://spec.graphql.org/June2018/#sec-Argument-Uniqueness",
                    },
                },
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
                    "message": "Directive < @deprecated > may not be used on FIELD.",
                    "path": None,
                    "locations": [{"line": 4, "column": 22}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                },
                {
                    "message": "There can be only one argument named < reason >.",
                    "path": None,
                    "locations": [
                        {"line": 4, "column": 34},
                        {"line": 4, "column": 51},
                    ],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.2",
                        "tag": "argument-uniqueness",
                        "details": "http://spec.graphql.org/June2018/#sec-Argument-Uniqueness",
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
                    "message": "Directive < @deprecated > may not be used on FIELD.",
                    "path": None,
                    "locations": [{"line": 4, "column": 22}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                },
                {
                    "message": "There can be only one argument named < reason >.",
                    "path": None,
                    "locations": [
                        {"line": 4, "column": 34},
                        {"line": 4, "column": 51},
                    ],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.2",
                        "tag": "argument-uniqueness",
                        "details": "http://spec.graphql.org/June2018/#sec-Argument-Uniqueness",
                    },
                },
                {
                    "message": "There can be only one argument named < reason >.",
                    "path": None,
                    "locations": [
                        {"line": 4, "column": 34},
                        {"line": 4, "column": 69},
                    ],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.2",
                        "tag": "argument-uniqueness",
                        "details": "http://spec.graphql.org/June2018/#sec-Argument-Uniqueness",
                    },
                },
            ],
        ),
    ],
)
async def test_issue99(schema_stack, query, errors):
    assert await schema_stack.execute(query) == {
        "data": None,
        "errors": errors,
    }
