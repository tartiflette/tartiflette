import pytest

from tests.functional.coercers.common import resolve_list_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.listWithDefaultIntField": resolve_list_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { listWithDefaultIntField }""",
            None,
            {"data": {"listWithDefaultIntField": "SUCCESS-[123459-None]"}},
        ),
        (
            """query { listWithDefaultIntField(param: null) }""",
            None,
            {"data": {"listWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query { listWithDefaultIntField(param: [null]) }""",
            None,
            {"data": {"listWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query { listWithDefaultIntField(param: 10) }""",
            None,
            {"data": {"listWithDefaultIntField": "SUCCESS-[13]"}},
        ),
        (
            """query { listWithDefaultIntField(param: [10]) }""",
            None,
            {"data": {"listWithDefaultIntField": "SUCCESS-[13]"}},
        ),
        (
            """query { listWithDefaultIntField(param: [10, null]) }""",
            None,
            {"data": {"listWithDefaultIntField": "SUCCESS-[13-None]"}},
        ),
        (
            """query ($param: [Int]) { listWithDefaultIntField(param: $param) }""",
            None,
            {"data": {"listWithDefaultIntField": "SUCCESS-[123459-None]"}},
        ),
        (
            """query ($param: [Int]) { listWithDefaultIntField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int]) { listWithDefaultIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int]) { listWithDefaultIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]) { listWithDefaultIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]) { listWithDefaultIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"listWithDefaultIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int] = null) { listWithDefaultIntField(param: $param) }""",
            None,
            {"data": {"listWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = null) { listWithDefaultIntField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = null) { listWithDefaultIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = null) { listWithDefaultIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = null) { listWithDefaultIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = null) { listWithDefaultIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"listWithDefaultIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int] = [null]) { listWithDefaultIntField(param: $param) }""",
            None,
            {"data": {"listWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = [null]) { listWithDefaultIntField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = [null]) { listWithDefaultIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = [null]) { listWithDefaultIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = [null]) { listWithDefaultIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = [null]) { listWithDefaultIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"listWithDefaultIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int] = 30) { listWithDefaultIntField(param: $param) }""",
            None,
            {"data": {"listWithDefaultIntField": "SUCCESS-[33]"}},
        ),
        (
            """query ($param: [Int] = 30) { listWithDefaultIntField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = 30) { listWithDefaultIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = 30) { listWithDefaultIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = 30) { listWithDefaultIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = 30) { listWithDefaultIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"listWithDefaultIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int] = [30]) { listWithDefaultIntField(param: $param) }""",
            None,
            {"data": {"listWithDefaultIntField": "SUCCESS-[33]"}},
        ),
        (
            """query ($param: [Int] = [30]) { listWithDefaultIntField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = [30]) { listWithDefaultIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = [30]) { listWithDefaultIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = [30]) { listWithDefaultIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = [30]) { listWithDefaultIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"listWithDefaultIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int] = [30, null]) { listWithDefaultIntField(param: $param) }""",
            None,
            {"data": {"listWithDefaultIntField": "SUCCESS-[33-None]"}},
        ),
        (
            """query ($param: [Int] = [30, null]) { listWithDefaultIntField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = [30, null]) { listWithDefaultIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = [30, null]) { listWithDefaultIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = [30, null]) { listWithDefaultIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = [30, null]) { listWithDefaultIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"listWithDefaultIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int]!) { listWithDefaultIntField(param: $param) }""",
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
            """query ($param: [Int]!) { listWithDefaultIntField(param: $param) }""",
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
            """query ($param: [Int]!) { listWithDefaultIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int]!) { listWithDefaultIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]!) { listWithDefaultIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]!) { listWithDefaultIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"listWithDefaultIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int!]) { listWithDefaultIntField(param: $param) }""",
            None,
            {"data": {"listWithDefaultIntField": "SUCCESS-[123459-None]"}},
        ),
        (
            """query ($param: [Int!]) { listWithDefaultIntField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int!]) { listWithDefaultIntField(param: $param) }""",
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
            """query ($param: [Int!]) { listWithDefaultIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]) { listWithDefaultIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]) { listWithDefaultIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { listWithDefaultIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { listWithDefaultIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { listWithDefaultIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { listWithDefaultIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]!) { listWithDefaultIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listWithDefaultIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]!) { listWithDefaultIntField(param: $param) }""",
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
            """query ($item: Int) { listWithDefaultIntField(param: [10, $item]) }""",
            None,
            {"data": {"listWithDefaultIntField": "SUCCESS-[13-None]"}},
        ),
        (
            """query ($item: Int) { listWithDefaultIntField(param: [10, $item]) }""",
            {"item": None},
            {"data": {"listWithDefaultIntField": "SUCCESS-[13-None]"}},
        ),
        (
            """query ($item: Int) { listWithDefaultIntField(param: [10, $item]) }""",
            {"item": 20},
            {"data": {"listWithDefaultIntField": "SUCCESS-[13-23]"}},
        ),
        (
            """query ($item: Int = null) { listWithDefaultIntField(param: [10, $item]) }""",
            None,
            {"data": {"listWithDefaultIntField": "SUCCESS-[13-None]"}},
        ),
        (
            """query ($item: Int = null) { listWithDefaultIntField(param: [10, $item]) }""",
            {"item": None},
            {"data": {"listWithDefaultIntField": "SUCCESS-[13-None]"}},
        ),
        (
            """query ($item: Int = null) { listWithDefaultIntField(param: [10, $item]) }""",
            {"item": 20},
            {"data": {"listWithDefaultIntField": "SUCCESS-[13-23]"}},
        ),
        (
            """query ($item: Int = 30) { listWithDefaultIntField(param: [10, $item]) }""",
            None,
            {"data": {"listWithDefaultIntField": "SUCCESS-[13-33]"}},
        ),
        (
            """query ($item: Int = 30) { listWithDefaultIntField(param: [10, $item]) }""",
            {"item": None},
            {"data": {"listWithDefaultIntField": "SUCCESS-[13-None]"}},
        ),
        (
            """query ($item: Int = 30) { listWithDefaultIntField(param: [10, $item]) }""",
            {"item": 20},
            {"data": {"listWithDefaultIntField": "SUCCESS-[13-23]"}},
        ),
        (
            """query ($item: Int!) { listWithDefaultIntField(param: [10, $item]) }""",
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
            """query ($item: Int!) { listWithDefaultIntField(param: [10, $item]) }""",
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
            """query ($item: Int!) { listWithDefaultIntField(param: [10, $item]) }""",
            {"item": 20},
            {"data": {"listWithDefaultIntField": "SUCCESS-[13-23]"}},
        ),
    ],
)
async def test_coercion_list_with_default_int_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
