import pytest


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullListWithDefaultFloatField }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[12345681.9-None]"
                }
            },
        ),
        (
            """query { nonNullListWithDefaultFloatField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < [Float]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 49}],
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
            """query { nonNullListWithDefaultFloatField(param: [null]) }""",
            None,
            {"data": {"nonNullListWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query { nonNullListWithDefaultFloatField(param: 23456.789e2) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[2345681.9]"
                }
            },
        ),
        (
            """query { nonNullListWithDefaultFloatField(param: [23456.789e2]) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[2345681.9]"
                }
            },
        ),
        (
            """query { nonNullListWithDefaultFloatField(param: [23456.789e2, null]) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[2345681.9-None]"
                }
            },
        ),
        (
            """query ($param: [Float]) { nonNullListWithDefaultFloatField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[12345681.9-None]"
                }
            },
        ),
        (
            """query ($param: [Float]) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Float]! > must not be null.",
                        "path": ["nonNullListWithDefaultFloatField"],
                        "locations": [{"line": 1, "column": 67}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Float]) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float]) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float]) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float]) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[345681.9-None]"
                }
            },
        ),
        (
            """query ($param: [Float] = null) { nonNullListWithDefaultFloatField(param: $param) }""",
            None,
            {
                "data": {"nonNullListWithDefaultFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Float]! > must not be null.",
                        "path": ["nonNullListWithDefaultFloatField"],
                        "locations": [{"line": 1, "column": 74}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Float] = null) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Float]! > must not be null.",
                        "path": ["nonNullListWithDefaultFloatField"],
                        "locations": [{"line": 1, "column": 74}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Float] = null) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = null) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float] = null) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float] = null) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[345681.9-None]"
                }
            },
        ),
        (
            """query ($param: [Float] = [null]) { nonNullListWithDefaultFloatField(param: $param) }""",
            None,
            {"data": {"nonNullListWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = [null]) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Float]! > must not be null.",
                        "path": ["nonNullListWithDefaultFloatField"],
                        "locations": [{"line": 1, "column": 76}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Float] = [null]) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = [null]) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float] = [null]) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float] = [null]) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[345681.9-None]"
                }
            },
        ),
        (
            """query ($param: [Float] = 456.789e2) { nonNullListWithDefaultFloatField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[45681.9]"
                }
            },
        ),
        (
            """query ($param: [Float] = 456.789e2) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Float]! > must not be null.",
                        "path": ["nonNullListWithDefaultFloatField"],
                        "locations": [{"line": 1, "column": 79}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Float] = 456.789e2) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = 456.789e2) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float] = 456.789e2) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float] = 456.789e2) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[345681.9-None]"
                }
            },
        ),
        (
            """query ($param: [Float] = [456.789e2]) { nonNullListWithDefaultFloatField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[45681.9]"
                }
            },
        ),
        (
            """query ($param: [Float] = [456.789e2]) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Float]! > must not be null.",
                        "path": ["nonNullListWithDefaultFloatField"],
                        "locations": [{"line": 1, "column": 81}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Float] = [456.789e2]) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2]) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float] = [456.789e2]) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float] = [456.789e2]) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[345681.9-None]"
                }
            },
        ),
        (
            """query ($param: [Float] = [456.789e2, null]) { nonNullListWithDefaultFloatField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[45681.9-None]"
                }
            },
        ),
        (
            """query ($param: [Float] = [456.789e2, null]) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Float]! > must not be null.",
                        "path": ["nonNullListWithDefaultFloatField"],
                        "locations": [{"line": 1, "column": 87}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Float] = [456.789e2, null]) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float] = [456.789e2, null]) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float] = [456.789e2, null]) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float] = [456.789e2, null]) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[345681.9-None]"
                }
            },
        ),
        (
            """query ($param: [Float]!) { nonNullListWithDefaultFloatField(param: $param) }""",
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
            """query ($param: [Float]!) { nonNullListWithDefaultFloatField(param: $param) }""",
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
            """query ($param: [Float]!) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float]!) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float]!) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float]!) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[345681.9-None]"
                }
            },
        ),
        (
            """query ($param: [Float!]) { nonNullListWithDefaultFloatField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[12345681.9-None]"
                }
            },
        ),
        (
            """query ($param: [Float!]) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Float]! > must not be null.",
                        "path": ["nonNullListWithDefaultFloatField"],
                        "locations": [{"line": 1, "column": 68}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Float!]) { nonNullListWithDefaultFloatField(param: $param) }""",
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
            """query ($param: [Float!]) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!]) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!]) { nonNullListWithDefaultFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { nonNullListWithDefaultFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { nonNullListWithDefaultFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { nonNullListWithDefaultFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!]!) { nonNullListWithDefaultFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!]!) { nonNullListWithDefaultFloatField(param: $param) }""",
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
            """query ($item: Float) { nonNullListWithDefaultFloatField(param: [23456.789e2, $item]) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[2345681.9-None]"
                }
            },
        ),
        (
            """query ($item: Float) { nonNullListWithDefaultFloatField(param: [23456.789e2, $item]) }""",
            {"item": None},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[2345681.9-None]"
                }
            },
        ),
        (
            """query ($item: Float) { nonNullListWithDefaultFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[2345681.9-345681.9]"
                }
            },
        ),
        (
            """query ($item: Float = null) { nonNullListWithDefaultFloatField(param: [23456.789e2, $item]) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[2345681.9-None]"
                }
            },
        ),
        (
            """query ($item: Float = null) { nonNullListWithDefaultFloatField(param: [23456.789e2, $item]) }""",
            {"item": None},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[2345681.9-None]"
                }
            },
        ),
        (
            """query ($item: Float = null) { nonNullListWithDefaultFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[2345681.9-345681.9]"
                }
            },
        ),
        (
            """query ($item: Float = 456.789e2) { nonNullListWithDefaultFloatField(param: [23456.789e2, $item]) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[2345681.9-45681.9]"
                }
            },
        ),
        (
            """query ($item: Float = 456.789e2) { nonNullListWithDefaultFloatField(param: [23456.789e2, $item]) }""",
            {"item": None},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[2345681.9-None]"
                }
            },
        ),
        (
            """query ($item: Float = 456.789e2) { nonNullListWithDefaultFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[2345681.9-345681.9]"
                }
            },
        ),
        (
            """query ($item: Float!) { nonNullListWithDefaultFloatField(param: [23456.789e2, $item]) }""",
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
            """query ($item: Float!) { nonNullListWithDefaultFloatField(param: [23456.789e2, $item]) }""",
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
            """query ($item: Float!) { nonNullListWithDefaultFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {
                "data": {
                    "nonNullListWithDefaultFloatField": "SUCCESS-[2345681.9-345681.9]"
                }
            },
        ),
    ],
)
async def test_coercion_non_null_list_with_default_float_field(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected
