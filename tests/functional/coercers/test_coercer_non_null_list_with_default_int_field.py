import pytest

from tests.functional.coercers.common import resolve_list_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.nonNullListWithDefaultIntField": resolve_list_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullListWithDefaultIntField }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultIntField": "SUCCESS-[123459-None]"
                }
            },
        ),
        (
            """query { nonNullListWithDefaultIntField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < [Int]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 47}],
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
            """query { nonNullListWithDefaultIntField(param: [null]) }""",
            None,
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query { nonNullListWithDefaultIntField(param: 10) }""",
            None,
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[13]"}},
        ),
        (
            """query { nonNullListWithDefaultIntField(param: [10]) }""",
            None,
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[13]"}},
        ),
        (
            """query { nonNullListWithDefaultIntField(param: [10, null]) }""",
            None,
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[13-None]"}},
        ),
        (
            """query ($param: [Int]) { nonNullListWithDefaultIntField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultIntField": "SUCCESS-[123459-None]"
                }
            },
        ),
        (
            """query ($param: [Int]) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Int]! > must not be null.",
                        "path": ["nonNullListWithDefaultIntField"],
                        "locations": [{"line": 1, "column": 63}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Int]) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int]) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int] = null) { nonNullListWithDefaultIntField(param: $param) }""",
            None,
            {
                "data": {"nonNullListWithDefaultIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Int]! > must not be null.",
                        "path": ["nonNullListWithDefaultIntField"],
                        "locations": [{"line": 1, "column": 70}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Int] = null) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Int]! > must not be null.",
                        "path": ["nonNullListWithDefaultIntField"],
                        "locations": [{"line": 1, "column": 70}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Int] = null) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = null) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = null) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = null) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int] = [null]) { nonNullListWithDefaultIntField(param: $param) }""",
            None,
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = [null]) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Int]! > must not be null.",
                        "path": ["nonNullListWithDefaultIntField"],
                        "locations": [{"line": 1, "column": 72}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Int] = [null]) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = [null]) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = [null]) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = [null]) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int] = 30) { nonNullListWithDefaultIntField(param: $param) }""",
            None,
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[33]"}},
        ),
        (
            """query ($param: [Int] = 30) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Int]! > must not be null.",
                        "path": ["nonNullListWithDefaultIntField"],
                        "locations": [{"line": 1, "column": 68}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Int] = 30) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = 30) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = 30) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = 30) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int] = [30]) { nonNullListWithDefaultIntField(param: $param) }""",
            None,
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[33]"}},
        ),
        (
            """query ($param: [Int] = [30]) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Int]! > must not be null.",
                        "path": ["nonNullListWithDefaultIntField"],
                        "locations": [{"line": 1, "column": 70}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Int] = [30]) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = [30]) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = [30]) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = [30]) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int] = [30, null]) { nonNullListWithDefaultIntField(param: $param) }""",
            None,
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[33-None]"}},
        ),
        (
            """query ($param: [Int] = [30, null]) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Int]! > must not be null.",
                        "path": ["nonNullListWithDefaultIntField"],
                        "locations": [{"line": 1, "column": 76}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Int] = [30, null]) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = [30, null]) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = [30, null]) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = [30, null]) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int]!) { nonNullListWithDefaultIntField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < [Int]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Int]!) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < [Int]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Int]!) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int]!) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]!) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]!) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int!]) { nonNullListWithDefaultIntField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultIntField": "SUCCESS-[123459-None]"
                }
            },
        ),
        (
            """query ($param: [Int!]) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Int]! > must not be null.",
                        "path": ["nonNullListWithDefaultIntField"],
                        "locations": [{"line": 1, "column": 64}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Int!]) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [None] >; Expected non-nullable type < Int! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Int!]) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [20, None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [20, None] >; Expected non-nullable type < Int! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Int!]!) { nonNullListWithDefaultIntField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < [Int!]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Int!]!) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < [Int!]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Int!]!) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [None] >; Expected non-nullable type < Int! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Int!]!) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]!) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]!) { nonNullListWithDefaultIntField(param: $param) }""",
            {"param": [20, None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [20, None] >; Expected non-nullable type < Int! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($item: Int) { nonNullListWithDefaultIntField(param: [10, $item]) }""",
            None,
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[13-None]"}},
        ),
        (
            """query ($item: Int) { nonNullListWithDefaultIntField(param: [10, $item]) }""",
            {"item": None},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[13-None]"}},
        ),
        (
            """query ($item: Int) { nonNullListWithDefaultIntField(param: [10, $item]) }""",
            {"item": 20},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[13-23]"}},
        ),
        (
            """query ($item: Int = null) { nonNullListWithDefaultIntField(param: [10, $item]) }""",
            None,
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[13-None]"}},
        ),
        (
            """query ($item: Int = null) { nonNullListWithDefaultIntField(param: [10, $item]) }""",
            {"item": None},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[13-None]"}},
        ),
        (
            """query ($item: Int = null) { nonNullListWithDefaultIntField(param: [10, $item]) }""",
            {"item": 20},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[13-23]"}},
        ),
        (
            """query ($item: Int = 30) { nonNullListWithDefaultIntField(param: [10, $item]) }""",
            None,
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[13-33]"}},
        ),
        (
            """query ($item: Int = 30) { nonNullListWithDefaultIntField(param: [10, $item]) }""",
            {"item": None},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[13-None]"}},
        ),
        (
            """query ($item: Int = 30) { nonNullListWithDefaultIntField(param: [10, $item]) }""",
            {"item": 20},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[13-23]"}},
        ),
        (
            """query ($item: Int!) { nonNullListWithDefaultIntField(param: [10, $item]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of required type < Int! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($item: Int!) { nonNullListWithDefaultIntField(param: [10, $item]) }""",
            {"item": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of non-null type < Int! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($item: Int!) { nonNullListWithDefaultIntField(param: [10, $item]) }""",
            {"item": 20},
            {"data": {"nonNullListWithDefaultIntField": "SUCCESS-[13-23]"}},
        ),
    ],
)
async def test_coercion_non_null_list_with_default_int_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
