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
                        "message": "Unknown Fragment for Spread < C >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 41}],
                        "extensions": {
                            "rule": "5.5.2.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-spread-target-defined",
                            "tag": "fragment-spread-target-defined",
                        },
                    },
                    {
                        "message": "Can't spread < Dog > via < B > Fragment on Type < Query >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 36}],
                        "extensions": {
                            "rule": "5.5.2.3",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-spread-is-possible",
                            "tag": "fragment-spread-is-possible",
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
                        "message": "Unknown Fragment for Spread < C >.",
                        "path": None,
                        "locations": [
                            {"line": 1, "column": 41},
                            {"line": 1, "column": 46},
                            {"line": 1, "column": 88},
                        ],
                        "extensions": {
                            "rule": "5.5.2.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-spread-target-defined",
                            "tag": "fragment-spread-target-defined",
                        },
                    },
                    {
                        "message": "Unknown Fragment for Spread < E >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 83}],
                        "extensions": {
                            "rule": "5.5.2.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-spread-target-defined",
                            "tag": "fragment-spread-target-defined",
                        },
                    },
                    {
                        "message": "Can't spread < Dog > via < B > Fragment on Type < Query >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 36}],
                        "extensions": {
                            "rule": "5.5.2.3",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-spread-is-possible",
                            "tag": "fragment-spread-is-possible",
                        },
                    },
                    {
                        "message": "Can't spread < Dog > via < D > Fragment on Type < Query >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 41}],
                        "extensions": {
                            "rule": "5.5.2.3",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-spread-is-possible",
                            "tag": "fragment-spread-is-possible",
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
