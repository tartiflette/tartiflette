import pytest

from tests.functional.coercers.common import resolve_list_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.listNonNullFloatField": resolve_list_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { listNonNullFloatField }""",
            None,
            {"data": {"listNonNullFloatField": "SUCCESS"}},
        ),
        (
            """query { listNonNullFloatField(param: null) }""",
            None,
            {"data": {"listNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query { listNonNullFloatField(param: [null]) }""",
            None,
            {
                "data": {"listNonNullFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [null] >.",
                        "path": ["listNonNullFloatField"],
                        "locations": [{"line": 1, "column": 38}],
                    }
                ],
            },
        ),
        (
            """query { listNonNullFloatField(param: 23456.789e2) }""",
            None,
            {"data": {"listNonNullFloatField": "SUCCESS-[2345681.9]"}},
        ),
        (
            """query { listNonNullFloatField(param: [23456.789e2]) }""",
            None,
            {"data": {"listNonNullFloatField": "SUCCESS-[2345681.9]"}},
        ),
        (
            """query { listNonNullFloatField(param: [23456.789e2, null]) }""",
            None,
            {
                "data": {"listNonNullFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [23456.789e2, null] >.",
                        "path": ["listNonNullFloatField"],
                        "locations": [{"line": 1, "column": 38}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Float]) { listNonNullFloatField(param: $param) }""",
            None,
            {"data": {"listNonNullFloatField": "SUCCESS"}},
        ),
        (
            """query ($param: [Float]) { listNonNullFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float]) { listNonNullFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float]) { listNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float]) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float]) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float] = null) { listNonNullFloatField(param: $param) }""",
            None,
            {"data": {"listNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = null) { listNonNullFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = null) { listNonNullFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = null) { listNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = null) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = null) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float] = [null]) { listNonNullFloatField(param: $param) }""",
            None,
            {"data": {"listNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = [null]) { listNonNullFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = [null]) { listNonNullFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = [null]) { listNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = [null]) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = [null]) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float] = 456.789e2) { listNonNullFloatField(param: $param) }""",
            None,
            {"data": {"listNonNullFloatField": "SUCCESS-[45681.9]"}},
        ),
        (
            """query ($param: [Float] = 456.789e2) { listNonNullFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = 456.789e2) { listNonNullFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = 456.789e2) { listNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = 456.789e2) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = 456.789e2) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2]) { listNonNullFloatField(param: $param) }""",
            None,
            {"data": {"listNonNullFloatField": "SUCCESS-[45681.9]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2]) { listNonNullFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2]) { listNonNullFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2]) { listNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2]) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2]) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2, null]) { listNonNullFloatField(param: $param) }""",
            None,
            {"data": {"listNonNullFloatField": "SUCCESS-[45681.9-None]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2, null]) { listNonNullFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2, null]) { listNonNullFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2, null]) { listNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2, null]) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2, null]) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float]!) { listNonNullFloatField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < [Float]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Float]!) { listNonNullFloatField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < [Float]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Float]!) { listNonNullFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float]!) { listNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float]!) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float]!) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float!]) { listNonNullFloatField(param: $param) }""",
            None,
            {"data": {"listNonNullFloatField": "SUCCESS"}},
        ),
        (
            """query ($param: [Float!]) { listNonNullFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float!]) { listNonNullFloatField(param: $param) }""",
            {"param": [None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [None] >; Expected non-nullable type < Float! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Float!]) { listNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!]) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!]) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [345678.9, None] >; Expected non-nullable type < Float! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Float!]!) { listNonNullFloatField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < [Float!]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Float!]!) { listNonNullFloatField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < [Float!]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Float!]!) { listNonNullFloatField(param: $param) }""",
            {"param": [None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [None] >; Expected non-nullable type < Float! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Float!]!) { listNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!]!) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!]!) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [345678.9, None] >; Expected non-nullable type < Float! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($item: Float) { listNonNullFloatField(param: [23456.789e2, $item]) }""",
            None,
            {
                "data": {"listNonNullFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [23456.789e2, $item] >.",
                        "path": ["listNonNullFloatField"],
                        "locations": [{"line": 1, "column": 53}],
                    }
                ],
            },
        ),
        (
            """query ($item: Float) { listNonNullFloatField(param: [23456.789e2, $item]) }""",
            {"item": None},
            {"data": {"listNonNullFloatField": "SUCCESS-[2345681.9-None]"}},
        ),
        (
            """query ($item: Float) { listNonNullFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {
                "data": {
                    "listNonNullFloatField": "SUCCESS-[2345681.9-345681.9]"
                }
            },
        ),
        (
            """query ($item: Float = null) { listNonNullFloatField(param: [23456.789e2, $item]) }""",
            None,
            {"data": {"listNonNullFloatField": "SUCCESS-[2345681.9-None]"}},
        ),
        (
            """query ($item: Float = null) { listNonNullFloatField(param: [23456.789e2, $item]) }""",
            {"item": None},
            {"data": {"listNonNullFloatField": "SUCCESS-[2345681.9-None]"}},
        ),
        (
            """query ($item: Float = null) { listNonNullFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {
                "data": {
                    "listNonNullFloatField": "SUCCESS-[2345681.9-345681.9]"
                }
            },
        ),
        (
            """query ($item: Float = 456.789e2) { listNonNullFloatField(param: [23456.789e2, $item]) }""",
            None,
            {"data": {"listNonNullFloatField": "SUCCESS-[2345681.9-45681.9]"}},
        ),
        (
            """query ($item: Float = 456.789e2) { listNonNullFloatField(param: [23456.789e2, $item]) }""",
            {"item": None},
            {"data": {"listNonNullFloatField": "SUCCESS-[2345681.9-None]"}},
        ),
        (
            """query ($item: Float = 456.789e2) { listNonNullFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {
                "data": {
                    "listNonNullFloatField": "SUCCESS-[2345681.9-345681.9]"
                }
            },
        ),
        (
            """query ($item: Float!) { listNonNullFloatField(param: [23456.789e2, $item]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of required type < Float! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($item: Float!) { listNonNullFloatField(param: [23456.789e2, $item]) }""",
            {"item": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of non-null type < Float! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($item: Float!) { listNonNullFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {
                "data": {
                    "listNonNullFloatField": "SUCCESS-[2345681.9-345681.9]"
                }
            },
        ),
    ],
)
async def test_coercion_list_non_null_float_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
