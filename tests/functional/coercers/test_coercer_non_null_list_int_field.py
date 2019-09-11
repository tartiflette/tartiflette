import pytest

from tests.functional.coercers.common import resolve_list_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.nonNullListIntField": resolve_list_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullListIntField }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Missing mandatory argument < param > in field < Query.nonNullListIntField >.",
                        "path": ["nonNullListIntField"],
                        "locations": [{"line": 1, "column": 9}],
                        "extensions": {
                            "rule": "5.4.2.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Required-Arguments",
                            "tag": "required-arguments",
                        },
                    }
                ],
            },
        ),
        (
            """query { nonNullListIntField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Int]! > must not be null.",
                        "path": ["nonNullListIntField"],
                        "locations": [{"line": 1, "column": 29}],
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
            """query { nonNullListIntField(param: [null]) }""",
            None,
            {"data": {"nonNullListIntField": "SUCCESS-[None]"}},
        ),
        (
            """query { nonNullListIntField(param: 10) }""",
            None,
            {"data": {"nonNullListIntField": "SUCCESS-[13]"}},
        ),
        (
            """query { nonNullListIntField(param: [10]) }""",
            None,
            {"data": {"nonNullListIntField": "SUCCESS-[13]"}},
        ),
        (
            """query { nonNullListIntField(param: [10, null]) }""",
            None,
            {"data": {"nonNullListIntField": "SUCCESS-[13-None]"}},
        ),
        (
            """query ($param: [Int]!) { nonNullListIntField(param: $param) }""",
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
            """query ($param: [Int]!) { nonNullListIntField(param: $param) }""",
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
            """query ($param: [Int]!) { nonNullListIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int]!) { nonNullListIntField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullListIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]!) { nonNullListIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"nonNullListIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]!) { nonNullListIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"nonNullListIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int]! = null) { nonNullListIntField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid default value < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 25}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Int]! = null) { nonNullListIntField(param: $param) }""",
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
            """query ($param: [Int]! = null) { nonNullListIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int]! = null) { nonNullListIntField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullListIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]! = null) { nonNullListIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"nonNullListIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]! = null) { nonNullListIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"nonNullListIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int]! = [null]) { nonNullListIntField(param: $param) }""",
            None,
            {"data": {"nonNullListIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int]! = [null]) { nonNullListIntField(param: $param) }""",
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
            """query ($param: [Int]! = [null]) { nonNullListIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int]! = [null]) { nonNullListIntField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullListIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]! = [null]) { nonNullListIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"nonNullListIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]! = [null]) { nonNullListIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"nonNullListIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int]! = 30) { nonNullListIntField(param: $param) }""",
            None,
            {"data": {"nonNullListIntField": "SUCCESS-[33]"}},
        ),
        (
            """query ($param: [Int]! = 30) { nonNullListIntField(param: $param) }""",
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
            """query ($param: [Int]! = 30) { nonNullListIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int]! = 30) { nonNullListIntField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullListIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]! = 30) { nonNullListIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"nonNullListIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]! = 30) { nonNullListIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"nonNullListIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int]! = [30]) { nonNullListIntField(param: $param) }""",
            None,
            {"data": {"nonNullListIntField": "SUCCESS-[33]"}},
        ),
        (
            """query ($param: [Int]! = [30]) { nonNullListIntField(param: $param) }""",
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
            """query ($param: [Int]! = [30]) { nonNullListIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int]! = [30]) { nonNullListIntField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullListIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]! = [30]) { nonNullListIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"nonNullListIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]! = [30]) { nonNullListIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"nonNullListIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int]! = [30, null]) { nonNullListIntField(param: $param) }""",
            None,
            {"data": {"nonNullListIntField": "SUCCESS-[33-None]"}},
        ),
        (
            """query ($param: [Int]! = [30, null]) { nonNullListIntField(param: $param) }""",
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
            """query ($param: [Int]! = [30, null]) { nonNullListIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int]! = [30, null]) { nonNullListIntField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullListIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]! = [30, null]) { nonNullListIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"nonNullListIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]! = [30, null]) { nonNullListIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"nonNullListIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int]!) { nonNullListIntField(param: $param) }""",
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
            """query ($param: [Int]!) { nonNullListIntField(param: $param) }""",
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
            """query ($param: [Int]!) { nonNullListIntField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int]!) { nonNullListIntField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullListIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]!) { nonNullListIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"nonNullListIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int]!) { nonNullListIntField(param: $param) }""",
            {"param": [20, None]},
            {"data": {"nonNullListIntField": "SUCCESS-[23-None]"}},
        ),
        (
            """query ($param: [Int!]!) { nonNullListIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { nonNullListIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { nonNullListIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { nonNullListIntField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullListIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]!) { nonNullListIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"nonNullListIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]!) { nonNullListIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { nonNullListIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { nonNullListIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { nonNullListIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { nonNullListIntField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullListIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]!) { nonNullListIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"nonNullListIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]!) { nonNullListIntField(param: $param) }""",
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
            """query ($item: Int) { nonNullListIntField(param: [10, $item]) }""",
            None,
            {"data": {"nonNullListIntField": "SUCCESS-[13-None]"}},
        ),
        (
            """query ($item: Int) { nonNullListIntField(param: [10, $item]) }""",
            {"item": None},
            {"data": {"nonNullListIntField": "SUCCESS-[13-None]"}},
        ),
        (
            """query ($item: Int) { nonNullListIntField(param: [10, $item]) }""",
            {"item": 20},
            {"data": {"nonNullListIntField": "SUCCESS-[13-23]"}},
        ),
        (
            """query ($item: Int = null) { nonNullListIntField(param: [10, $item]) }""",
            None,
            {"data": {"nonNullListIntField": "SUCCESS-[13-None]"}},
        ),
        (
            """query ($item: Int = null) { nonNullListIntField(param: [10, $item]) }""",
            {"item": None},
            {"data": {"nonNullListIntField": "SUCCESS-[13-None]"}},
        ),
        (
            """query ($item: Int = null) { nonNullListIntField(param: [10, $item]) }""",
            {"item": 20},
            {"data": {"nonNullListIntField": "SUCCESS-[13-23]"}},
        ),
        (
            """query ($item: Int = 30) { nonNullListIntField(param: [10, $item]) }""",
            None,
            {"data": {"nonNullListIntField": "SUCCESS-[13-33]"}},
        ),
        (
            """query ($item: Int = 30) { nonNullListIntField(param: [10, $item]) }""",
            {"item": None},
            {"data": {"nonNullListIntField": "SUCCESS-[13-None]"}},
        ),
        (
            """query ($item: Int = 30) { nonNullListIntField(param: [10, $item]) }""",
            {"item": 20},
            {"data": {"nonNullListIntField": "SUCCESS-[13-23]"}},
        ),
        (
            """query ($item: Int!) { nonNullListIntField(param: [10, $item]) }""",
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
            """query ($item: Int!) { nonNullListIntField(param: [10, $item]) }""",
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
            """query ($item: Int!) { nonNullListIntField(param: [10, $item]) }""",
            {"item": 20},
            {"data": {"nonNullListIntField": "SUCCESS-[13-23]"}},
        ),
    ],
)
async def test_coercion_non_null_list_int_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
