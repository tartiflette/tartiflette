import pytest


@pytest.mark.asyncio
@pytest.mark.ttftt_engine
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query{
                catOrDog(id: 1) @dontExists { ... on Dog{ name @skip(if: false) } }
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Unknown directive < @dontExists >.",
                        "path": None,
                        "locations": [{"line": 3, "column": 33}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.7.1",
                            "tag": "directives-are-defined",
                            "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Defined",
                        },
                    }
                ],
            },
        )
    ],
)
async def test_validators_directives_are_defined(query, expected, engine):
    assert await engine.execute(query) == expected
