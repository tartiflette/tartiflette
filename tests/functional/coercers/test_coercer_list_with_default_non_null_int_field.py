import pytest

from tests.functional.coercers.common import resolve_list_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.listWithDefaultNonNullIntField": resolve_list_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { listWithDefaultNonNullIntField }""",
            None,
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[123459]"}},
        ),
        (
            """query { listWithDefaultNonNullIntField(param: null) }""",
            None,
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[None]"}},
        ),
        (
            """query { listWithDefaultNonNullIntField(param: [null]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Int! > must not be null.",
                        "path": ["listWithDefaultNonNullIntField"],
                        "locations": [{"line": 1, "column": 40}],
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
            """query { listWithDefaultNonNullIntField(param: 10) }""",
            None,
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[13]"}},
        ),
        (
            """query { listWithDefaultNonNullIntField(param: [10]) }""",
            None,
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[13]"}},
        ),
        (
            """query { listWithDefaultNonNullIntField(param: [10, null]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Int! > must not be null.",
                        "path": ["listWithDefaultNonNullIntField"],
                        "locations": [{"line": 1, "column": 40}],
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
            """query ($param: [Int!]) { listWithDefaultNonNullIntField(param: $param) }""",
            None,
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[123459]"}},
        ),
        (
            """query ($param: [Int!]) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int!]) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!] = null) { listWithDefaultNonNullIntField(param: $param) }""",
            None,
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int!] = null) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int!] = null) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!] = null) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!] = [null]) { listWithDefaultNonNullIntField(param: $param) }""",
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
            """query ($param: [Int!] = [null]) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int!] = [null]) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!] = [null]) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!] = 30) { listWithDefaultNonNullIntField(param: $param) }""",
            None,
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[33]"}},
        ),
        (
            """query ($param: [Int!] = 30) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int!] = 30) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!] = 30) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!] = [30]) { listWithDefaultNonNullIntField(param: $param) }""",
            None,
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[33]"}},
        ),
        (
            """query ($param: [Int!] = [30]) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int!] = [30]) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!] = [30]) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!] = [30, null]) { listWithDefaultNonNullIntField(param: $param) }""",
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
            """query ($param: [Int!] = [30, null]) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int!] = [30, null]) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!] = [30, null]) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]!) { listWithDefaultNonNullIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { listWithDefaultNonNullIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]!) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]) { listWithDefaultNonNullIntField(param: $param) }""",
            None,
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[123459]"}},
        ),
        (
            """query ($param: [Int!]) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Int!]) { listWithDefaultNonNullIntField(param: $param) }""",
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
            """query ($param: [Int!]) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]) { listWithDefaultNonNullIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { listWithDefaultNonNullIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { listWithDefaultNonNullIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { listWithDefaultNonNullIntField(param: $param) }""",
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
            """query ($param: [Int!]!) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": 20},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]!) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": [20]},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[23]"}},
        ),
        (
            """query ($param: [Int!]!) { listWithDefaultNonNullIntField(param: $param) }""",
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
            """query ($item: Int) { listWithDefaultNonNullIntField(param: [10, $item]) }""",
            None,
            {
                "data": {"listWithDefaultNonNullIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [10, $item] >.",
                        "path": ["listWithDefaultNonNullIntField"],
                        "locations": [{"line": 1, "column": 60}],
                    }
                ],
            },
        ),
        (
            """query ($item: Int) { listWithDefaultNonNullIntField(param: [10, $item]) }""",
            {"item": None},
            {
                "data": {"listWithDefaultNonNullIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [10, $item] >.",
                        "path": ["listWithDefaultNonNullIntField"],
                        "locations": [{"line": 1, "column": 60}],
                    }
                ],
            },
        ),
        (
            """query ($item: Int) { listWithDefaultNonNullIntField(param: [10, $item]) }""",
            {"item": 20},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[13-23]"}},
        ),
        (
            """query ($item: Int = null) { listWithDefaultNonNullIntField(param: [10, $item]) }""",
            None,
            {
                "data": {"listWithDefaultNonNullIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [10, $item] >.",
                        "path": ["listWithDefaultNonNullIntField"],
                        "locations": [{"line": 1, "column": 67}],
                    }
                ],
            },
        ),
        (
            """query ($item: Int = null) { listWithDefaultNonNullIntField(param: [10, $item]) }""",
            {"item": None},
            {
                "data": {"listWithDefaultNonNullIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [10, $item] >.",
                        "path": ["listWithDefaultNonNullIntField"],
                        "locations": [{"line": 1, "column": 67}],
                    }
                ],
            },
        ),
        (
            """query ($item: Int = null) { listWithDefaultNonNullIntField(param: [10, $item]) }""",
            {"item": 20},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[13-23]"}},
        ),
        (
            """query ($item: Int = 30) { listWithDefaultNonNullIntField(param: [10, $item]) }""",
            None,
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[13-33]"}},
        ),
        (
            """query ($item: Int = 30) { listWithDefaultNonNullIntField(param: [10, $item]) }""",
            {"item": None},
            {
                "data": {"listWithDefaultNonNullIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [10, $item] >.",
                        "path": ["listWithDefaultNonNullIntField"],
                        "locations": [{"line": 1, "column": 65}],
                    }
                ],
            },
        ),
        (
            """query ($item: Int = 30) { listWithDefaultNonNullIntField(param: [10, $item]) }""",
            {"item": 20},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[13-23]"}},
        ),
        (
            """query ($item: Int!) { listWithDefaultNonNullIntField(param: [10, $item]) }""",
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
            """query ($item: Int!) { listWithDefaultNonNullIntField(param: [10, $item]) }""",
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
            """query ($item: Int!) { listWithDefaultNonNullIntField(param: [10, $item]) }""",
            {"item": 20},
            {"data": {"listWithDefaultNonNullIntField": "SUCCESS-[13-23]"}},
        ),
    ],
)
async def test_coercion_list_with_default_non_null_int_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
