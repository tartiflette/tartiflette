import pytest

from tests.functional.coercers.common import resolve_unwrapped_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.nonNullFloatField": resolve_unwrapped_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullFloatField }""",
            None,
            {
                "data": {"nonNullFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < Float! > was not provided.",
                        "path": ["nonNullFloatField"],
                        "locations": [{"line": 1, "column": 9}],
                    }
                ],
            },
        ),
        (
            """query { nonNullFloatField(param: null) }""",
            None,
            {
                "data": {"nonNullFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Float! > must not be null.",
                        "path": ["nonNullFloatField"],
                        "locations": [{"line": 1, "column": 34}],
                    }
                ],
            },
        ),
        (
            """query { nonNullFloatField(param: 23456.789e2) }""",
            None,
            {"data": {"nonNullFloatField": "SUCCESS-2345681.9"}},
        ),
        (
            """query ($param: Float) { nonNullFloatField(param: $param) }""",
            None,
            {
                "data": {"nonNullFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < Float! > was provided the variable < $param > which was not provided a runtime value.",
                        "path": ["nonNullFloatField"],
                        "locations": [{"line": 1, "column": 50}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float) { nonNullFloatField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Float! > must not be null.",
                        "path": ["nonNullFloatField"],
                        "locations": [{"line": 1, "column": 50}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float) { nonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"nonNullFloatField": "SUCCESS-345681.9"}},
        ),
        (
            """query ($param: Float = null) { nonNullFloatField(param: $param) }""",
            None,
            {
                "data": {"nonNullFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Float! > must not be null.",
                        "path": ["nonNullFloatField"],
                        "locations": [{"line": 1, "column": 57}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float = null) { nonNullFloatField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Float! > must not be null.",
                        "path": ["nonNullFloatField"],
                        "locations": [{"line": 1, "column": 57}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float = null) { nonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"nonNullFloatField": "SUCCESS-345681.9"}},
        ),
        (
            """query ($param: Float = 456.789e2) { nonNullFloatField(param: $param) }""",
            None,
            {"data": {"nonNullFloatField": "SUCCESS-45681.9"}},
        ),
        (
            """query ($param: Float = 456.789e2) { nonNullFloatField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Float! > must not be null.",
                        "path": ["nonNullFloatField"],
                        "locations": [{"line": 1, "column": 62}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float = 456.789e2) { nonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"nonNullFloatField": "SUCCESS-345681.9"}},
        ),
        (
            """query ($param: Float!) { nonNullFloatField(param: $param) }""",
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
            """query ($param: Float!) { nonNullFloatField(param: $param) }""",
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
            """query ($param: Float!) { nonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"nonNullFloatField": "SUCCESS-345681.9"}},
        ),
    ],
)
async def test_coercion_non_null_float_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
