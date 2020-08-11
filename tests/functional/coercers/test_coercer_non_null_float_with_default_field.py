import pytest

from tests.functional.coercers.common import resolve_unwrapped_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.nonNullFloatWithDefaultField": resolve_unwrapped_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullFloatWithDefaultField }""",
            None,
            {"data": {"nonNullFloatWithDefaultField": "SUCCESS-12345681.9"}},
        ),
        (
            """query { nonNullFloatWithDefaultField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 45}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    }
                ],
            },
        ),
        (
            """query { nonNullFloatWithDefaultField(param: 23456.789e2) }""",
            None,
            {"data": {"nonNullFloatWithDefaultField": "SUCCESS-2345681.9"}},
        ),
        (
            """query ($param: Float) { nonNullFloatWithDefaultField(param: $param) }""",
            None,
            {"data": {"nonNullFloatWithDefaultField": "SUCCESS-12345681.9"}},
        ),
        (
            """query ($param: Float) { nonNullFloatWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullFloatWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Float! > must not be null.",
                        "path": ["nonNullFloatWithDefaultField"],
                        "locations": [{"line": 1, "column": 61}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float) { nonNullFloatWithDefaultField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"nonNullFloatWithDefaultField": "SUCCESS-345681.9"}},
        ),
        (
            """query ($param: Float = null) { nonNullFloatWithDefaultField(param: $param) }""",
            None,
            {
                "data": {"nonNullFloatWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Float! > must not be null.",
                        "path": ["nonNullFloatWithDefaultField"],
                        "locations": [{"line": 1, "column": 68}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float = null) { nonNullFloatWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullFloatWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Float! > must not be null.",
                        "path": ["nonNullFloatWithDefaultField"],
                        "locations": [{"line": 1, "column": 68}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float = null) { nonNullFloatWithDefaultField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"nonNullFloatWithDefaultField": "SUCCESS-345681.9"}},
        ),
        (
            """query ($param: Float = 456.789e2) { nonNullFloatWithDefaultField(param: $param) }""",
            None,
            {"data": {"nonNullFloatWithDefaultField": "SUCCESS-45681.9"}},
        ),
        (
            """query ($param: Float = 456.789e2) { nonNullFloatWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullFloatWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Float! > must not be null.",
                        "path": ["nonNullFloatWithDefaultField"],
                        "locations": [{"line": 1, "column": 73}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float = 456.789e2) { nonNullFloatWithDefaultField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"nonNullFloatWithDefaultField": "SUCCESS-345681.9"}},
        ),
        (
            """query ($param: Float!) { nonNullFloatWithDefaultField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < Float! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float!) { nonNullFloatWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < Float! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float!) { nonNullFloatWithDefaultField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"nonNullFloatWithDefaultField": "SUCCESS-345681.9"}},
        ),
    ],
)
async def test_coercion_non_null_float_with_default_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
