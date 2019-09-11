import pytest


async def resolve_dog(*_, **__):
    return {"name": "JeanMichel"}


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(resolvers={"Query.dog": resolve_dog})
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
        query lol($a: Int, $b: String!) {
            dog {
                name
            }
        }
        """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Unused Varibable < a > in Operation < lol >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 9},
                            {"line": 2, "column": 19},
                        ],
                        "extensions": {
                            "rule": "5.8.4",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variables-Used",
                            "tag": "all-variables-used",
                        },
                    },
                    {
                        "message": "Unused Varibable < b > in Operation < lol >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 9},
                            {"line": 2, "column": 28},
                        ],
                        "extensions": {
                            "rule": "5.8.4",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variables-Used",
                            "tag": "all-variables-used",
                        },
                    },
                ],
            },
        ),
        (
            """
        query lol($a: Int, $b: String!, $a: String) {
            dog {
                name
            }
        }
        """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Can't have multiple variables named < a >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 2, "column": 41},
                        ],
                        "extensions": {
                            "rule": "5.8.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Variable-Uniqueness",
                            "tag": "variable-uniqueness",
                        },
                    },
                    {
                        "message": "Unused Varibable < a > in Operation < lol >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 9},
                            {"line": 2, "column": 19},
                            {"line": 2, "column": 41},
                        ],
                        "extensions": {
                            "rule": "5.8.4",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variables-Used",
                            "tag": "all-variables-used",
                        },
                    },
                    {
                        "message": "Unused Varibable < b > in Operation < lol >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 9},
                            {"line": 2, "column": 28},
                        ],
                        "extensions": {
                            "rule": "5.8.4",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variables-Used",
                            "tag": "all-variables-used",
                        },
                    },
                ],
            },
        ),
    ],
)
async def test_validators_variable_uniqueness(query, expected, engine):
    assert (
        await engine.execute(query, variables={"a": 1, "b": "b"}) == expected
    )
