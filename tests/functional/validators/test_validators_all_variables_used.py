import pytest


@pytest.mark.asyncio
@pytest.mark.ttftt_engine
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query($a: Int, $b: Int){
                catOrDog(id: $a) { ... on Dog{ name } }
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $b > is never used.",
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
                        "message": "Variable < $a > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 3, "column": 30},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        )
    ],
)
async def test_validators_all_variables_used(query, expected, engine):
    assert await engine.execute(query) == expected
