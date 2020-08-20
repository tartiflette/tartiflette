import pytest


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { listFloatField }""",
            None,
            {"data": {"listFloatField": "SUCCESS"}},
        ),
        (
            """query { listFloatField(param: null) }""",
            None,
            {"data": {"listFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query { listFloatField(param: [null]) }""",
            None,
            {"data": {"listFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query { listFloatField(param: 23456.789e2) }""",
            None,
            {"data": {"listFloatField": "SUCCESS-[2345681.9]"}},
        ),
        (
            """query { listFloatField(param: [23456.789e2]) }""",
            None,
            {"data": {"listFloatField": "SUCCESS-[2345681.9]"}},
        ),
        (
            """query { listFloatField(param: [23456.789e2, null]) }""",
            None,
            {"data": {"listFloatField": "SUCCESS-[2345681.9-None]"}},
        ),
        (
            """query ($param: [Float]) { listFloatField(param: $param) }""",
            None,
            {"data": {"listFloatField": "SUCCESS"}},
        ),
        (
            """query ($param: [Float]) { listFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float]) { listFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"listFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float]) { listFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float]) { listFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float]) { listFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"listFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float] = null) { listFloatField(param: $param) }""",
            None,
            {"data": {"listFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = null) { listFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = null) { listFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"listFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = null) { listFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = null) { listFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = null) { listFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"listFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float] = [null]) { listFloatField(param: $param) }""",
            None,
            {"data": {"listFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = [null]) { listFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = [null]) { listFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"listFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = [null]) { listFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = [null]) { listFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = [null]) { listFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"listFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float] = 456.789e2) { listFloatField(param: $param) }""",
            None,
            {"data": {"listFloatField": "SUCCESS-[45681.9]"}},
        ),
        (
            """query ($param: [Float] = 456.789e2) { listFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = 456.789e2) { listFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"listFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = 456.789e2) { listFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = 456.789e2) { listFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = 456.789e2) { listFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"listFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2]) { listFloatField(param: $param) }""",
            None,
            {"data": {"listFloatField": "SUCCESS-[45681.9]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2]) { listFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2]) { listFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"listFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2]) { listFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2]) { listFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2]) { listFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"listFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2, null]) { listFloatField(param: $param) }""",
            None,
            {"data": {"listFloatField": "SUCCESS-[45681.9-None]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2, null]) { listFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2, null]) { listFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"listFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2, null]) { listFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2, null]) { listFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2, null]) { listFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"listFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float]!) { listFloatField(param: $param) }""",
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
            """query ($param: [Float]!) { listFloatField(param: $param) }""",
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
            """query ($param: [Float]!) { listFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"listFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float]!) { listFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float]!) { listFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float]!) { listFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"listFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float!]) { listFloatField(param: $param) }""",
            None,
            {"data": {"listFloatField": "SUCCESS"}},
        ),
        (
            """query ($param: [Float!]) { listFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float!]) { listFloatField(param: $param) }""",
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
            """query ($param: [Float!]) { listFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!]) { listFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!]) { listFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { listFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { listFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { listFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { listFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!]!) { listFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!]!) { listFloatField(param: $param) }""",
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
            """query ($item: Float) { listFloatField(param: [23456.789e2, $item]) }""",
            None,
            {"data": {"listFloatField": "SUCCESS-[2345681.9-None]"}},
        ),
        (
            """query ($item: Float) { listFloatField(param: [23456.789e2, $item]) }""",
            {"item": None},
            {"data": {"listFloatField": "SUCCESS-[2345681.9-None]"}},
        ),
        (
            """query ($item: Float) { listFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {"data": {"listFloatField": "SUCCESS-[2345681.9-345681.9]"}},
        ),
        (
            """query ($item: Float = null) { listFloatField(param: [23456.789e2, $item]) }""",
            None,
            {"data": {"listFloatField": "SUCCESS-[2345681.9-None]"}},
        ),
        (
            """query ($item: Float = null) { listFloatField(param: [23456.789e2, $item]) }""",
            {"item": None},
            {"data": {"listFloatField": "SUCCESS-[2345681.9-None]"}},
        ),
        (
            """query ($item: Float = null) { listFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {"data": {"listFloatField": "SUCCESS-[2345681.9-345681.9]"}},
        ),
        (
            """query ($item: Float = 456.789e2) { listFloatField(param: [23456.789e2, $item]) }""",
            None,
            {"data": {"listFloatField": "SUCCESS-[2345681.9-45681.9]"}},
        ),
        (
            """query ($item: Float = 456.789e2) { listFloatField(param: [23456.789e2, $item]) }""",
            {"item": None},
            {"data": {"listFloatField": "SUCCESS-[2345681.9-None]"}},
        ),
        (
            """query ($item: Float = 456.789e2) { listFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {"data": {"listFloatField": "SUCCESS-[2345681.9-345681.9]"}},
        ),
        (
            """query ($item: Float!) { listFloatField(param: [23456.789e2, $item]) }""",
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
            """query ($item: Float!) { listFloatField(param: [23456.789e2, $item]) }""",
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
            """query ($item: Float!) { listFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {"data": {"listFloatField": "SUCCESS-[2345681.9-345681.9]"}},
        ),
    ],
)
async def test_coercion_list_float_field(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected
