import pytest

from tests.functional.coercers.common import resolve_list_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.listWithDefaultNonNullFloatField": resolve_list_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { listWithDefaultNonNullFloatField }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[12345681.9]"
                }
            },
        ),
        (
            """query { listWithDefaultNonNullFloatField(param: null) }""",
            None,
            {"data": {"listWithDefaultNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query { listWithDefaultNonNullFloatField(param: [null]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Float! > must not be null.",
                        "path": ["listWithDefaultNonNullFloatField"],
                        "locations": [{"line": 1, "column": 42}],
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
            """query { listWithDefaultNonNullFloatField(param: 23456.789e2) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[2345681.9]"
                }
            },
        ),
        (
            """query { listWithDefaultNonNullFloatField(param: [23456.789e2]) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[2345681.9]"
                }
            },
        ),
        (
            """query { listWithDefaultNonNullFloatField(param: [23456.789e2, null]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Float! > must not be null.",
                        "path": ["listWithDefaultNonNullFloatField"],
                        "locations": [{"line": 1, "column": 42}],
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
            """query ($param: [Float!]) { listWithDefaultNonNullFloatField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[12345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!]) { listWithDefaultNonNullFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float!]) { listWithDefaultNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!]) { listWithDefaultNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!] = null) { listWithDefaultNonNullFloatField(param: $param) }""",
            None,
            {"data": {"listWithDefaultNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float!] = null) { listWithDefaultNonNullFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float!] = null) { listWithDefaultNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!] = null) { listWithDefaultNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!] = [null]) { listWithDefaultNonNullFloatField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid default value < [null] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 27}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Float!] = [null]) { listWithDefaultNonNullFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float!] = [null]) { listWithDefaultNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!] = [null]) { listWithDefaultNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!] = 456.789e2) { listWithDefaultNonNullFloatField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[45681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!] = 456.789e2) { listWithDefaultNonNullFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float!] = 456.789e2) { listWithDefaultNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!] = 456.789e2) { listWithDefaultNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!] = [456.789e2]) { listWithDefaultNonNullFloatField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[45681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!] = [456.789e2]) { listWithDefaultNonNullFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float!] = [456.789e2]) { listWithDefaultNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!] = [456.789e2]) { listWithDefaultNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!] = [456.789e2, null]) { listWithDefaultNonNullFloatField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid default value < [456.789e2, null] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 27}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Float!] = [456.789e2, null]) { listWithDefaultNonNullFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float!] = [456.789e2, null]) { listWithDefaultNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!] = [456.789e2, null]) { listWithDefaultNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!]!) { listWithDefaultNonNullFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { listWithDefaultNonNullFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { listWithDefaultNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!]!) { listWithDefaultNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!]) { listWithDefaultNonNullFloatField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[12345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!]) { listWithDefaultNonNullFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float!]) { listWithDefaultNonNullFloatField(param: $param) }""",
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
            """query ($param: [Float!]) { listWithDefaultNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!]) { listWithDefaultNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!]) { listWithDefaultNonNullFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { listWithDefaultNonNullFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { listWithDefaultNonNullFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { listWithDefaultNonNullFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { listWithDefaultNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!]!) { listWithDefaultNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[345681.9]"
                }
            },
        ),
        (
            """query ($param: [Float!]!) { listWithDefaultNonNullFloatField(param: $param) }""",
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
            """query ($item: Float) { listWithDefaultNonNullFloatField(param: [23456.789e2, $item]) }""",
            None,
            {
                "data": {"listWithDefaultNonNullFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [23456.789e2, $item] >.",
                        "path": ["listWithDefaultNonNullFloatField"],
                        "locations": [{"line": 1, "column": 64}],
                    }
                ],
            },
        ),
        (
            """query ($item: Float) { listWithDefaultNonNullFloatField(param: [23456.789e2, $item]) }""",
            {"item": None},
            {
                "data": {"listWithDefaultNonNullFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [23456.789e2, $item] >.",
                        "path": ["listWithDefaultNonNullFloatField"],
                        "locations": [{"line": 1, "column": 64}],
                    }
                ],
            },
        ),
        (
            """query ($item: Float) { listWithDefaultNonNullFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[2345681.9-345681.9]"
                }
            },
        ),
        (
            """query ($item: Float = null) { listWithDefaultNonNullFloatField(param: [23456.789e2, $item]) }""",
            None,
            {
                "data": {"listWithDefaultNonNullFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [23456.789e2, $item] >.",
                        "path": ["listWithDefaultNonNullFloatField"],
                        "locations": [{"line": 1, "column": 71}],
                    }
                ],
            },
        ),
        (
            """query ($item: Float = null) { listWithDefaultNonNullFloatField(param: [23456.789e2, $item]) }""",
            {"item": None},
            {
                "data": {"listWithDefaultNonNullFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [23456.789e2, $item] >.",
                        "path": ["listWithDefaultNonNullFloatField"],
                        "locations": [{"line": 1, "column": 71}],
                    }
                ],
            },
        ),
        (
            """query ($item: Float = null) { listWithDefaultNonNullFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[2345681.9-345681.9]"
                }
            },
        ),
        (
            """query ($item: Float = 456.789e2) { listWithDefaultNonNullFloatField(param: [23456.789e2, $item]) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[2345681.9-45681.9]"
                }
            },
        ),
        (
            """query ($item: Float = 456.789e2) { listWithDefaultNonNullFloatField(param: [23456.789e2, $item]) }""",
            {"item": None},
            {
                "data": {"listWithDefaultNonNullFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [23456.789e2, $item] >.",
                        "path": ["listWithDefaultNonNullFloatField"],
                        "locations": [{"line": 1, "column": 76}],
                    }
                ],
            },
        ),
        (
            """query ($item: Float = 456.789e2) { listWithDefaultNonNullFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[2345681.9-345681.9]"
                }
            },
        ),
        (
            """query ($item: Float!) { listWithDefaultNonNullFloatField(param: [23456.789e2, $item]) }""",
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
            """query ($item: Float!) { listWithDefaultNonNullFloatField(param: [23456.789e2, $item]) }""",
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
            """query ($item: Float!) { listWithDefaultNonNullFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {
                "data": {
                    "listWithDefaultNonNullFloatField": "SUCCESS-[2345681.9-345681.9]"
                }
            },
        ),
    ],
)
async def test_coercion_list_with_default_non_null_float_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
