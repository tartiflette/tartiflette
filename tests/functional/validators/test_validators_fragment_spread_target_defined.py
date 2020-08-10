import pytest


@pytest.mark.asyncio
@pytest.mark.ttftt_engine
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            "fragment B on Dog { name } query { ...B ...C }",
            {
                "data": None,
                "errors": [
                    {
                        "message": "Fragment < B > cannot be spread here as objects of type < Query > can never be of type < Dog >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 36}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.5.2.3",
                            "tag": "fragment-spread-is-possible",
                            "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-is-possible",
                        },
                    },
                    {
                        "message": "Unknown fragment < C >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 44}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.5.2.1",
                            "tag": "fragment-spread-target-defined",
                            "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-target-defined",
                        },
                    },
                ],
            },
        ),
        (
            "fragment B on Dog { name } query { ...B ...C ...C ...D } fragment D on Dog { name ...E ...C }",
            {
                "data": None,
                "errors": [
                    {
                        "message": "Fragment < B > cannot be spread here as objects of type < Query > can never be of type < Dog >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 36}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.5.2.3",
                            "tag": "fragment-spread-is-possible",
                            "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-is-possible",
                        },
                    },
                    {
                        "message": "Unknown fragment < C >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 44}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.5.2.1",
                            "tag": "fragment-spread-target-defined",
                            "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-target-defined",
                        },
                    },
                    {
                        "message": "Unknown fragment < C >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 49}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.5.2.1",
                            "tag": "fragment-spread-target-defined",
                            "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-target-defined",
                        },
                    },
                    {
                        "message": "Fragment < D > cannot be spread here as objects of type < Query > can never be of type < Dog >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 51}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.5.2.3",
                            "tag": "fragment-spread-is-possible",
                            "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-is-possible",
                        },
                    },
                    {
                        "message": "Unknown fragment < E >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 86}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.5.2.1",
                            "tag": "fragment-spread-target-defined",
                            "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-target-defined",
                        },
                    },
                    {
                        "message": "Unknown fragment < C >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 91}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.5.2.1",
                            "tag": "fragment-spread-target-defined",
                            "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-target-defined",
                        },
                    },
                ],
            },
        ),
    ],
)
async def test_validators_fragment_spread_target_defined(
    query, expected, engine
):
    assert await engine.execute(query) == expected
