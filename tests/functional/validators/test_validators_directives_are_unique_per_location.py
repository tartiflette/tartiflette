import pytest


@pytest.mark.asyncio
@pytest.mark.ttftt_engine
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query{
                catOrDog(id: 1) @skip(if: true) @skip(if: false) { ... on Dog{ name @skip(if: false) @include(if: true)} }
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "The directive < @skip > can only be used once at this location.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 33},
                            {"line": 3, "column": 49},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.7.3",
                            "tag": "directives-are-unique-per-location",
                            "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location",
                        },
                    }
                ],
            },
        )
    ],
)
async def test_validators_directives_are_unique_per_location(
    query, expected, engine
):
    assert await engine.execute(query) == expected
