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
                        "message": "Variable < $a > is never used in operation < lol >.",
                        "path": None,
                        "locations": [{"line": 2, "column": 19}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.4",
                            "tag": "all-variables-used",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variables-Used",
                        },
                    },
                    {
                        "message": "Variable < $b > is never used in operation < lol >.",
                        "path": None,
                        "locations": [{"line": 2, "column": 28}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.4",
                            "tag": "all-variables-used",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variables-Used",
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
                        "message": "There can be only one variable named < $a >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 2, "column": 41},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.1",
                            "tag": "variable-uniqueness",
                            "details": "https://spec.graphql.org/June2018/#sec-Variable-Uniqueness",
                        },
                    },
                    {
                        "message": "Variable < $a > is never used in operation < lol >.",
                        "path": None,
                        "locations": [{"line": 2, "column": 19}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.4",
                            "tag": "all-variables-used",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variables-Used",
                        },
                    },
                    {
                        "message": "Variable < $b > is never used in operation < lol >.",
                        "path": None,
                        "locations": [{"line": 2, "column": 28}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.4",
                            "tag": "all-variables-used",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variables-Used",
                        },
                    },
                    {
                        "message": "Variable < $a > is never used in operation < lol >.",
                        "path": None,
                        "locations": [{"line": 2, "column": 41}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.4",
                            "tag": "all-variables-used",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variables-Used",
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
