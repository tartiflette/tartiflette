import pytest

from tests.functional.coercers.common import resolve_list_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.listNonNullIntField": resolve_list_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { listNonNullIntField }""",
            None,
            {"data": {"listNonNullIntField": "SUCCESS"}},
        ),
        (
            """query { listNonNullIntField(param: null) }""",
            None,
            {"data": {"listNonNullIntField": "SUCCESS-[None]"}},
        ),
        (
            """query { listNonNullIntField(param: [null]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Int! > must not be null.",
                        "path": ["listNonNullIntField"],
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
            """query { listNonNullIntField(param: 10) }""",
            None,
            {"data": {"listNonNullIntField": "SUCCESS-[13]"}},
        ),
        (
            """query { listNonNullIntField(param: [10]) }""",
            None,
            {"data": {"listNonNullIntField": "SUCCESS-[13]"}},
        ),
        (
            """query { listNonNullIntField(param: [10, null]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Int! > must not be null.",
                        "path": ["listNonNullIntField"],
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
            """query ($param: [Int!]) { listNonNullIntField(param: $param) }""",
            None,
            {"data": {"listNonNullIntField": "SUCCESS"}},
        ),
        (
            """query ($param: [Int!]) { listNonNullIntField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int!]) { listNonNullIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]) { listNonNullIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!] = null) { listNonNullIntField(param: $param) }""",
            None,
            {"data": {"listNonNullIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int!] = null) { listNonNullIntField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int!] = null) { listNonNullIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!] = null) { listNonNullIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!] = [null]) { listNonNullIntField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid default value < [null] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 25}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Int!] = [null]) { listNonNullIntField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int!] = [null]) { listNonNullIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!] = [null]) { listNonNullIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!] = 30) { listNonNullIntField(param: $param) }""",
            None,
            {"data": {"listNonNullIntField": "SUCCESS-[33]"}},
        ),
        (
            """query ($param: [Int!] = 30) { listNonNullIntField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int!] = 30) { listNonNullIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!] = 30) { listNonNullIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!] = [30]) { listNonNullIntField(param: $param) }""",
            None,
            {"data": {"listNonNullIntField": "SUCCESS-[33]"}},
        ),
        (
            """query ($param: [Int!] = [30]) { listNonNullIntField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int!] = [30]) { listNonNullIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!] = [30]) { listNonNullIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!] = [30, null]) { listNonNullIntField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid default value < [30, null] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 25}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Int!] = [30, null]) { listNonNullIntField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int!] = [30, null]) { listNonNullIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!] = [30, null]) { listNonNullIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]!) { listNonNullIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { listNonNullIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { listNonNullIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]!) { listNonNullIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]) { listNonNullIntField(param: $param) }""",
            None,
            {"data": {"listNonNullIntField": "SUCCESS"}},
        ),
        (
            """query ($param: [Int!]) { listNonNullIntField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int!]) { listNonNullIntField(param: $param) }""",
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
            """query ($param: [Int!]) { listNonNullIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]) { listNonNullIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]) { listNonNullIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { listNonNullIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { listNonNullIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { listNonNullIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { listNonNullIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]!) { listNonNullIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]!) { listNonNullIntField(param: $param) }""",
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
            """query ($item: Int) { listNonNullIntField(param: [10, $item]) }""",
            None,
            {
                "data": {"listNonNullIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [10, $item] >.",
                        "path": ["listNonNullIntField"],
                        "locations": [{"line": 1, "column": 49}],
                    }
                ],
            },
        ),
        (
            """query ($item: Int) { listNonNullIntField(param: [10, $item]) }""",
            {"item": None},
            {
                "data": {"listNonNullIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [10, $item] >.",
                        "path": ["listNonNullIntField"],
                        "locations": [{"line": 1, "column": 49}],
                    }
                ],
            },
        ),
        (
            """query ($item: Int) { listNonNullIntField(param: [10, $item]) }""",
            {"item": 20},
            {"data": {"listNonNullIntField": "SUCCESS-[13-23]"}},
        ),
        (
            """query ($item: Int = null) { listNonNullIntField(param: [10, $item]) }""",
            None,
            {
                "data": {"listNonNullIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [10, $item] >.",
                        "path": ["listNonNullIntField"],
                        "locations": [{"line": 1, "column": 56}],
                    }
                ],
            },
        ),
        (
            """query ($item: Int = null) { listNonNullIntField(param: [10, $item]) }""",
            {"item": None},
            {
                "data": {"listNonNullIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [10, $item] >.",
                        "path": ["listNonNullIntField"],
                        "locations": [{"line": 1, "column": 56}],
                    }
                ],
            },
        ),
        (
            """query ($item: Int = null) { listNonNullIntField(param: [10, $item]) }""",
            {"item": 20},
            {"data": {"listNonNullIntField": "SUCCESS-[13-23]"}},
        ),
        (
            """query ($item: Int = 30) { listNonNullIntField(param: [10, $item]) }""",
            None,
            {"data": {"listNonNullIntField": "SUCCESS-[13-33]"}},
        ),
        (
            """query ($item: Int = 30) { listNonNullIntField(param: [10, $item]) }""",
            {"item": None},
            {
                "data": {"listNonNullIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [10, $item] >.",
                        "path": ["listNonNullIntField"],
                        "locations": [{"line": 1, "column": 54}],
                    }
                ],
            },
        ),
        (
            """query ($item: Int = 30) { listNonNullIntField(param: [10, $item]) }""",
            {"item": 20},
            {"data": {"listNonNullIntField": "SUCCESS-[13-23]"}},
        ),
        (
            """query ($item: Int!) { listNonNullIntField(param: [10, $item]) }""",
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
            """query ($item: Int!) { listNonNullIntField(param: [10, $item]) }""",
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
            """query ($item: Int!) { listNonNullIntField(param: [10, $item]) }""",
            {"item": 20},
            {"data": {"listNonNullIntField": "SUCCESS-[13-23]"}},
        ),
    ],
)
async def test_coercion_list_non_null_int_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
