import pytest


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
                        "message": "Unused Varibable < b > in anonymous Operation.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 13},
                            {"line": 2, "column": 28},
                        ],
                        "extensions": {
                            "rule": "5.8.4",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variables-Used",
                            "tag": "all-variables-used",
                        },
                    },
                    {
                        "message": "Can't use < $a / Int > for type < Int! >.",
                        "path": ["catOrDog"],
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 3, "column": 30},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                ],
            },
        )
    ],
)
@pytest.mark.asyncio
@pytest.mark.ttftt_engine
async def test_validators_all_variables_used(query, expected, engine):
    assert await engine.execute(query) == expected
