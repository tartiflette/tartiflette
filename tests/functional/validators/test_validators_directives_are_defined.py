import pytest


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
                        "message": "Unknow Directive < @dontExists >.",
                        "path": ["catOrDog"],
                        "locations": [{"line": 3, "column": 33}],
                        "extensions": {
                            "rule": "5.7.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-Defined",
                            "tag": "directives-are-defined",
                        },
                    }
                ],
            },
        )
    ],
)
@pytest.mark.asyncio
@pytest.mark.ttftt_engine
async def test_validators_directives_are_defined(query, expected, engine):
    assert await engine.execute(query) == expected
