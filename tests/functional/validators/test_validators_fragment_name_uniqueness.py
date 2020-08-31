import pytest


@pytest.mark.asyncio
@pytest.mark.ttftt_engine
async def test_validators_fragment_same_name(engine):
    assert await engine.execute(
        """
    fragment a on Dog {
        name
    }

    fragment a on Cat {
        name
    }


    query {
        dog {
            name
        }
    }

    """
    ) == {
        "data": None,
        "errors": [
            {
                "message": "Can't have multiple fragments named < a >.",
                "path": None,
                "locations": [
                    {"line": 2, "column": 5},
                    {"line": 6, "column": 5},
                ],
                "extensions": {
                    "rule": "5.5.1.1",
                    "spec": "June 2018",
                    "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-Name-Uniqueness",
                    "tag": "fragment-name-uniqueness",
                },
            },
            {
                "message": "Fragment < a > is never used.",
                "path": None,
                "locations": [{"line": 2, "column": 5}],
                "extensions": {
                    "rule": "5.5.1.4",
                    "spec": "June 2018",
                    "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Fragments-Must-Be-Used",
                    "tag": "fragment-must-be-used",
                },
            },
            {
                "message": "Fragment < a > is never used.",
                "path": None,
                "locations": [{"line": 6, "column": 5}],
                "extensions": {
                    "rule": "5.5.1.4",
                    "spec": "June 2018",
                    "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Fragments-Must-Be-Used",
                    "tag": "fragment-must-be-used",
                },
            },
        ],
    }
