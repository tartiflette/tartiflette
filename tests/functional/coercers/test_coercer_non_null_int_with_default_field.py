import pytest

from tests.functional.coercers.common import resolve_unwrapped_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.nonNullIntWithDefaultField": resolve_unwrapped_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullIntWithDefaultField }""",
            None,
            {"data": {"nonNullIntWithDefaultField": "SUCCESS-123459"}},
        ),
        (
            """query { nonNullIntWithDefaultField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Int! > must not be null.",
                        "path": ["nonNullIntWithDefaultField"],
                        "locations": [{"line": 1, "column": 36}],
                        "extensions": {
                            "rule": "5.6.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Values-of-Correct-Type",
                            "tag": "values-of-correct-type",
                        },
                    }
                ],
            },
        ),
        (
            """query { nonNullIntWithDefaultField(param: 10) }""",
            None,
            {"data": {"nonNullIntWithDefaultField": "SUCCESS-13"}},
        ),
        (
            """query ($param: Int) { nonNullIntWithDefaultField(param: $param) }""",
            None,
            {"data": {"nonNullIntWithDefaultField": "SUCCESS-123459"}},
        ),
        (
            """query ($param: Int) { nonNullIntWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullIntWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Int! > must not be null.",
                        "path": ["nonNullIntWithDefaultField"],
                        "locations": [{"line": 1, "column": 57}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int) { nonNullIntWithDefaultField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullIntWithDefaultField": "SUCCESS-23"}},
        ),
        (
            """query ($param: Int = null) { nonNullIntWithDefaultField(param: $param) }""",
            None,
            {
                "data": {"nonNullIntWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Int! > must not be null.",
                        "path": ["nonNullIntWithDefaultField"],
                        "locations": [{"line": 1, "column": 64}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int = null) { nonNullIntWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullIntWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Int! > must not be null.",
                        "path": ["nonNullIntWithDefaultField"],
                        "locations": [{"line": 1, "column": 64}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int = null) { nonNullIntWithDefaultField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullIntWithDefaultField": "SUCCESS-23"}},
        ),
        (
            """query ($param: Int = 30) { nonNullIntWithDefaultField(param: $param) }""",
            None,
            {"data": {"nonNullIntWithDefaultField": "SUCCESS-33"}},
        ),
        (
            """query ($param: Int = 30) { nonNullIntWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullIntWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Int! > must not be null.",
                        "path": ["nonNullIntWithDefaultField"],
                        "locations": [{"line": 1, "column": 62}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int = 30) { nonNullIntWithDefaultField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullIntWithDefaultField": "SUCCESS-23"}},
        ),
        (
            """query ($param: Int!) { nonNullIntWithDefaultField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < Int! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int!) { nonNullIntWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < Int! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int!) { nonNullIntWithDefaultField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullIntWithDefaultField": "SUCCESS-23"}},
        ),
    ],
)
async def test_coercion_non_null_int_with_default_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
