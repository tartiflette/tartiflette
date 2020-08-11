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
                        "message": "Field < nonNullListIntField > argument < param > of type < [Int]! > is required, but it was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 9}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.4.2.1",
                            "tag": "required-arguments",
                            "details": "https://spec.graphql.org/June2018/#sec-Required-Arguments",
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
                        "message": "Expected value of type < [Int]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 36}],
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
                        "message": "Expected value of type < [Int]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 25}],
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
            """query ($param: [Int]! = null) { nonNullListIntField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < [Int]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 25}],
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
            """query ($param: [Int]! = null) { nonNullListIntField(param: $param) }""",
            {"param": [None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < [Int]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 25}],
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
            """query ($param: [Int]! = null) { nonNullListIntField(param: $param) }""",
            {"param": 20},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < [Int]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 25}],
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
            """query ($param: [Int]! = null) { nonNullListIntField(param: $param) }""",
            {"param": [20]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < [Int]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 25}],
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
            """query ($param: [Int]! = null) { nonNullListIntField(param: $param) }""",
            {"param": [20, None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < [Int]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 25}],
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
