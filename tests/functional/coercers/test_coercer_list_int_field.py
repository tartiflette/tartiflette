import pytest

from tests.functional.coercers.common import resolve_list_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion", resolvers={"Query.listIntField": resolve_list_field}
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { listIntField }""",
            None,
            {"data": {"listIntField": "SUCCESS"}},
        ),
        (
            """query { listIntField(param: null) }""",
            None,
            {"data": {"listIntField": "SUCCESS-[None]"}},
        ),
        (
            """query { listIntField(param: [null]) }""",
            None,
            {"data": {"listIntField": "SUCCESS-[None]"}},
        ),
        (
            """query { listIntField(param: 10) }""",
            None,
            {"data": {"listIntField": "SUCCESS-[13]"}},
        ),
        (
            """query { listIntField(param: [10]) }""",
            None,
            {"data": {"listIntField": "SUCCESS-[13]"}},
        ),
        (
            """query { listIntField(param: [10, null]) }""",
            None,
            {"data": {"listIntField": "SUCCESS-[13-None]"}},
        ),
        (
            """query ($param: [Int]) { listIntField(param: $param) }""",
            None,
            {"data": {"listIntField": "SUCCESS"}},
        ),
        (
            """query ($param: [Int]) { listIntField(param: $param) }""",
            {"param": None},
            {"data": {"listIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int]) { listIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"listIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int]) { listIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]) { listIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]) { listIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"listIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int] = null) { listIntField(param: $param) }""",
            None,
            {"data": {"listIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = null) { listIntField(param: $param) }""",
            {"param": None},
            {"data": {"listIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = null) { listIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"listIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = null) { listIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = null) { listIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = null) { listIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"listIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int] = [null]) { listIntField(param: $param) }""",
            None,
            {"data": {"listIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = [null]) { listIntField(param: $param) }""",
            {"param": None},
            {"data": {"listIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = [null]) { listIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"listIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = [null]) { listIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = [null]) { listIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = [null]) { listIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"listIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int] = 30) { listIntField(param: $param) }""",
            None,
            {"data": {"listIntField": "SUCCESS-[33]"}},
        ),
        (
            """query ($param: [Int] = 30) { listIntField(param: $param) }""",
            {"param": None},
            {"data": {"listIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = 30) { listIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"listIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = 30) { listIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = 30) { listIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = 30) { listIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"listIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int] = [30]) { listIntField(param: $param) }""",
            None,
            {"data": {"listIntField": "SUCCESS-[33]"}},
        ),
        (
            """query ($param: [Int] = [30]) { listIntField(param: $param) }""",
            {"param": None},
            {"data": {"listIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = [30]) { listIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"listIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = [30]) { listIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = [30]) { listIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = [30]) { listIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"listIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int] = [30, null]) { listIntField(param: $param) }""",
            None,
            {"data": {"listIntField": "SUCCESS-[33-None]"}},
        ),
        (
            """query ($param: [Int] = [30, null]) { listIntField(param: $param) }""",
            {"param": None},
            {"data": {"listIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = [30, null]) { listIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"listIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int] = [30, null]) { listIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = [30, null]) { listIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int] = [30, null]) { listIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"listIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int]!) { listIntField(param: $param) }""",
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
            """query ($param: [Int]!) { listIntField(param: $param) }""",
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
            """query ($param: [Int]!) { listIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"listIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int]!) { listIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]!) { listIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]!) { listIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"listIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int!]) { listIntField(param: $param) }""",
            None,
            {"data": {"listIntField": "SUCCESS"}},
        ),
        (
            """query ($param: [Int!]) { listIntField(param: $param) }""",
            {"param": None},
            {"data": {"listIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int!]) { listIntField(param: $param) }""",
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
            """query ($param: [Int!]) { listIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]) { listIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]) { listIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { listIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { listIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { listIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { listIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]!) { listIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]!) { listIntField(param: $param) }""",
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
            """query ($item: Int) { listIntField(param: [10, $item]) }""",
            None,
            {"data": {"listIntField": "SUCCESS-[13-None]"}},
        ),
        (
            """query ($item: Int) { listIntField(param: [10, $item]) }""",
            {"item": None},
            {"data": {"listIntField": "SUCCESS-[13-None]"}},
        ),
        (
            """query ($item: Int) { listIntField(param: [10, $item]) }""",
            {"item": 20},
            {"data": {"listIntField": "SUCCESS-[13-23]"}},
        ),
        (
            """query ($item: Int = null) { listIntField(param: [10, $item]) }""",
            None,
            {"data": {"listIntField": "SUCCESS-[13-None]"}},
        ),
        (
            """query ($item: Int = null) { listIntField(param: [10, $item]) }""",
            {"item": None},
            {"data": {"listIntField": "SUCCESS-[13-None]"}},
        ),
        (
            """query ($item: Int = null) { listIntField(param: [10, $item]) }""",
            {"item": 20},
            {"data": {"listIntField": "SUCCESS-[13-23]"}},
        ),
        (
            """query ($item: Int = 30) { listIntField(param: [10, $item]) }""",
            None,
            {"data": {"listIntField": "SUCCESS-[13-33]"}},
        ),
        (
            """query ($item: Int = 30) { listIntField(param: [10, $item]) }""",
            {"item": None},
            {"data": {"listIntField": "SUCCESS-[13-None]"}},
        ),
        (
            """query ($item: Int = 30) { listIntField(param: [10, $item]) }""",
            {"item": 20},
            {"data": {"listIntField": "SUCCESS-[13-23]"}},
        ),
        (
            """query ($item: Int!) { listIntField(param: [10, $item]) }""",
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
            """query ($item: Int!) { listIntField(param: [10, $item]) }""",
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
            """query ($item: Int!) { listIntField(param: [10, $item]) }""",
            {"item": 20},
            {"data": {"listIntField": "SUCCESS-[13-23]"}},
        ),
    ],
)
async def test_coercion_list_int_field(engine, query, variables, expected):
    assert await engine.execute(query, variables=variables) == expected
