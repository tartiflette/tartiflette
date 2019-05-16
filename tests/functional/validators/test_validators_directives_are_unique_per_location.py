import pytest


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
                        "message": "Can't have multiple directives named < skip > in the same location.",
                        "path": ["catOrDog"],
                        "locations": [
                            {"line": 3, "column": 33},
                            {"line": 3, "column": 49},
                        ],
                        "extensions": {
                            "rule": "5.7.3",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-Unique-Per-Location",
                            "tag": "directives-are-unique-per-location",
                        },
                    }
                ],
            },
        )
    ],
)
@pytest.mark.asyncio
@pytest.mark.ttftt_engine
async def test_validators_directives_are_unique_per_location(
    query, expected, engine
):
    assert await engine.execute(query) == expected
