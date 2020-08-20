import pytest


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { listWithDefaultFloatField }""",
            None,
            {
                "data": {
                    "listWithDefaultFloatField": "SUCCESS-[12345681.9-None]"
                }
            },
        ),
        (
            """query { listWithDefaultFloatField(param: null) }""",
            None,
            {"data": {"listWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query { listWithDefaultFloatField(param: [null]) }""",
            None,
            {"data": {"listWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query { listWithDefaultFloatField(param: 23456.789e2) }""",
            None,
            {"data": {"listWithDefaultFloatField": "SUCCESS-[2345681.9]"}},
        ),
        (
            """query { listWithDefaultFloatField(param: [23456.789e2]) }""",
            None,
            {"data": {"listWithDefaultFloatField": "SUCCESS-[2345681.9]"}},
        ),
        (
            """query { listWithDefaultFloatField(param: [23456.789e2, null]) }""",
            None,
            {
                "data": {
                    "listWithDefaultFloatField": "SUCCESS-[2345681.9-None]"
                }
            },
        ),
        (
            """query ($param: [Float]) { listWithDefaultFloatField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultFloatField": "SUCCESS-[12345681.9-None]"
                }
            },
        ),
        (
            """query ($param: [Float]) { listWithDefaultFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float]) { listWithDefaultFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float]) { listWithDefaultFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float]) { listWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float]) { listWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float] = null) { listWithDefaultFloatField(param: $param) }""",
            None,
            {"data": {"listWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = null) { listWithDefaultFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = null) { listWithDefaultFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = null) { listWithDefaultFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = null) { listWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = null) { listWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float] = [null]) { listWithDefaultFloatField(param: $param) }""",
            None,
            {"data": {"listWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = [null]) { listWithDefaultFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = [null]) { listWithDefaultFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = [null]) { listWithDefaultFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = [null]) { listWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = [null]) { listWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float] = 456.789e2) { listWithDefaultFloatField(param: $param) }""",
            None,
            {"data": {"listWithDefaultFloatField": "SUCCESS-[45681.9]"}},
        ),
        (
            """query ($param: [Float] = 456.789e2) { listWithDefaultFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = 456.789e2) { listWithDefaultFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = 456.789e2) { listWithDefaultFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = 456.789e2) { listWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = 456.789e2) { listWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2]) { listWithDefaultFloatField(param: $param) }""",
            None,
            {"data": {"listWithDefaultFloatField": "SUCCESS-[45681.9]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2]) { listWithDefaultFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2]) { listWithDefaultFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2]) { listWithDefaultFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2]) { listWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2]) { listWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2, null]) { listWithDefaultFloatField(param: $param) }""",
            None,
            {"data": {"listWithDefaultFloatField": "SUCCESS-[45681.9-None]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2, null]) { listWithDefaultFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2, null]) { listWithDefaultFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2, null]) { listWithDefaultFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2, null]) { listWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2, null]) { listWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float]!) { listWithDefaultFloatField(param: $param) }""",
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
            """query ($param: [Float]!) { listWithDefaultFloatField(param: $param) }""",
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
            """query ($param: [Float]!) { listWithDefaultFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float]!) { listWithDefaultFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float]!) { listWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float]!) { listWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float!]) { listWithDefaultFloatField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultFloatField": "SUCCESS-[12345681.9-None]"
                }
            },
        ),
        (
            """query ($param: [Float!]) { listWithDefaultFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float!]) { listWithDefaultFloatField(param: $param) }""",
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
            """query ($param: [Float!]) { listWithDefaultFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!]) { listWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!]) { listWithDefaultFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { listWithDefaultFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { listWithDefaultFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { listWithDefaultFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { listWithDefaultFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!]!) { listWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listWithDefaultFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!]!) { listWithDefaultFloatField(param: $param) }""",
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
            """query ($item: Float) { listWithDefaultFloatField(param: [23456.789e2, $item]) }""",
            None,
            {
                "data": {
                    "listWithDefaultFloatField": "SUCCESS-[2345681.9-None]"
                }
            },
        ),
        (
            """query ($item: Float) { listWithDefaultFloatField(param: [23456.789e2, $item]) }""",
            {"item": None},
            {
                "data": {
                    "listWithDefaultFloatField": "SUCCESS-[2345681.9-None]"
                }
            },
        ),
        (
            """query ($item: Float) { listWithDefaultFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {
                "data": {
                    "listWithDefaultFloatField": "SUCCESS-[2345681.9-345681.9]"
                }
            },
        ),
        (
            """query ($item: Float = null) { listWithDefaultFloatField(param: [23456.789e2, $item]) }""",
            None,
            {
                "data": {
                    "listWithDefaultFloatField": "SUCCESS-[2345681.9-None]"
                }
            },
        ),
        (
            """query ($item: Float = null) { listWithDefaultFloatField(param: [23456.789e2, $item]) }""",
            {"item": None},
            {
                "data": {
                    "listWithDefaultFloatField": "SUCCESS-[2345681.9-None]"
                }
            },
        ),
        (
            """query ($item: Float = null) { listWithDefaultFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {
                "data": {
                    "listWithDefaultFloatField": "SUCCESS-[2345681.9-345681.9]"
                }
            },
        ),
        (
            """query ($item: Float = 456.789e2) { listWithDefaultFloatField(param: [23456.789e2, $item]) }""",
            None,
            {
                "data": {
                    "listWithDefaultFloatField": "SUCCESS-[2345681.9-45681.9]"
                }
            },
        ),
        (
            """query ($item: Float = 456.789e2) { listWithDefaultFloatField(param: [23456.789e2, $item]) }""",
            {"item": None},
            {
                "data": {
                    "listWithDefaultFloatField": "SUCCESS-[2345681.9-None]"
                }
            },
        ),
        (
            """query ($item: Float = 456.789e2) { listWithDefaultFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {
                "data": {
                    "listWithDefaultFloatField": "SUCCESS-[2345681.9-345681.9]"
                }
            },
        ),
        (
            """query ($item: Float!) { listWithDefaultFloatField(param: [23456.789e2, $item]) }""",
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
            """query ($item: Float!) { listWithDefaultFloatField(param: [23456.789e2, $item]) }""",
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
            """query ($item: Float!) { listWithDefaultFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {
                "data": {
                    "listWithDefaultFloatField": "SUCCESS-[2345681.9-345681.9]"
                }
            },
        ),
    ],
)
async def test_coercion_list_with_default_float_field(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected
