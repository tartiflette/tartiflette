import pytest

from tests.functional.coercers.common import resolve_list_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.nonNullListFloatField": resolve_list_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullListFloatField }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Field < nonNullListFloatField > argument < param > of type < [Float]! > is required, but it was not provided.",
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
            """query { nonNullListFloatField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < [Float]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 38}],
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
            """query { nonNullListFloatField(param: [null]) }""",
            None,
            {"data": {"nonNullListFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query { nonNullListFloatField(param: 23456.789e2) }""",
            None,
            {"data": {"nonNullListFloatField": "SUCCESS-[2345681.9]"}},
        ),
        (
            """query { nonNullListFloatField(param: [23456.789e2]) }""",
            None,
            {"data": {"nonNullListFloatField": "SUCCESS-[2345681.9]"}},
        ),
        (
            """query { nonNullListFloatField(param: [23456.789e2, null]) }""",
            None,
            {"data": {"nonNullListFloatField": "SUCCESS-[2345681.9-None]"}},
        ),
        (
            """query ($param: [Float]!) { nonNullListFloatField(param: $param) }""",
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
            """query ($param: [Float]!) { nonNullListFloatField(param: $param) }""",
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
            """query ($param: [Float]!) { nonNullListFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float]!) { nonNullListFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"nonNullListFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float]!) { nonNullListFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"nonNullListFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float]!) { nonNullListFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"nonNullListFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float]! = null) { nonNullListFloatField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < [Float]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 27}],
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
            """query ($param: [Float]! = null) { nonNullListFloatField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < [Float]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 27}],
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
            """query ($param: [Float]! = null) { nonNullListFloatField(param: $param) }""",
            {"param": [None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < [Float]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 27}],
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
            """query ($param: [Float]! = null) { nonNullListFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < [Float]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 27}],
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
            """query ($param: [Float]! = null) { nonNullListFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < [Float]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 27}],
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
            """query ($param: [Float]! = null) { nonNullListFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < [Float]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 27}],
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
            """query ($param: [Float]! = [null]) { nonNullListFloatField(param: $param) }""",
            None,
            {"data": {"nonNullListFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float]! = [null]) { nonNullListFloatField(param: $param) }""",
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
            """query ($param: [Float]! = [null]) { nonNullListFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float]! = [null]) { nonNullListFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"nonNullListFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float]! = [null]) { nonNullListFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"nonNullListFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float]! = [null]) { nonNullListFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"nonNullListFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float]! = 456.789e2) { nonNullListFloatField(param: $param) }""",
            None,
            {"data": {"nonNullListFloatField": "SUCCESS-[45681.9]"}},
        ),
        (
            """query ($param: [Float]! = 456.789e2) { nonNullListFloatField(param: $param) }""",
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
            """query ($param: [Float]! = 456.789e2) { nonNullListFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float]! = 456.789e2) { nonNullListFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"nonNullListFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float]! = 456.789e2) { nonNullListFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"nonNullListFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float]! = 456.789e2) { nonNullListFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"nonNullListFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float]! = [456.789e2]) { nonNullListFloatField(param: $param) }""",
            None,
            {"data": {"nonNullListFloatField": "SUCCESS-[45681.9]"}},
        ),
        (
            """query ($param: [Float]! = [456.789e2]) { nonNullListFloatField(param: $param) }""",
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
            """query ($param: [Float]! = [456.789e2]) { nonNullListFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float]! = [456.789e2]) { nonNullListFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"nonNullListFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float]! = [456.789e2]) { nonNullListFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"nonNullListFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float]! = [456.789e2]) { nonNullListFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"nonNullListFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float]! = [456.789e2, null]) { nonNullListFloatField(param: $param) }""",
            None,
            {"data": {"nonNullListFloatField": "SUCCESS-[45681.9-None]"}},
        ),
        (
            """query ($param: [Float]! = [456.789e2, null]) { nonNullListFloatField(param: $param) }""",
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
            """query ($param: [Float]! = [456.789e2, null]) { nonNullListFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float]! = [456.789e2, null]) { nonNullListFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"nonNullListFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float]! = [456.789e2, null]) { nonNullListFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"nonNullListFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float]! = [456.789e2, null]) { nonNullListFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"nonNullListFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float]!) { nonNullListFloatField(param: $param) }""",
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
            """query ($param: [Float]!) { nonNullListFloatField(param: $param) }""",
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
            """query ($param: [Float]!) { nonNullListFloatField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float]!) { nonNullListFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"nonNullListFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float]!) { nonNullListFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"nonNullListFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float]!) { nonNullListFloatField(param: $param) }""",
            {"param": [3456.789e2, None]},
            {"data": {"nonNullListFloatField": "SUCCESS-[345681.9-None]"}},
        ),
        (
            """query ($param: [Float!]!) { nonNullListFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { nonNullListFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { nonNullListFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { nonNullListFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"nonNullListFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!]!) { nonNullListFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"nonNullListFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!]!) { nonNullListFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { nonNullListFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { nonNullListFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { nonNullListFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { nonNullListFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"nonNullListFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!]!) { nonNullListFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"nonNullListFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!]!) { nonNullListFloatField(param: $param) }""",
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
            """query ($item: Float) { nonNullListFloatField(param: [23456.789e2, $item]) }""",
            None,
            {"data": {"nonNullListFloatField": "SUCCESS-[2345681.9-None]"}},
        ),
        (
            """query ($item: Float) { nonNullListFloatField(param: [23456.789e2, $item]) }""",
            {"item": None},
            {"data": {"nonNullListFloatField": "SUCCESS-[2345681.9-None]"}},
        ),
        (
            """query ($item: Float) { nonNullListFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {
                "data": {
                    "nonNullListFloatField": "SUCCESS-[2345681.9-345681.9]"
                }
            },
        ),
        (
            """query ($item: Float = null) { nonNullListFloatField(param: [23456.789e2, $item]) }""",
            None,
            {"data": {"nonNullListFloatField": "SUCCESS-[2345681.9-None]"}},
        ),
        (
            """query ($item: Float = null) { nonNullListFloatField(param: [23456.789e2, $item]) }""",
            {"item": None},
            {"data": {"nonNullListFloatField": "SUCCESS-[2345681.9-None]"}},
        ),
        (
            """query ($item: Float = null) { nonNullListFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {
                "data": {
                    "nonNullListFloatField": "SUCCESS-[2345681.9-345681.9]"
                }
            },
        ),
        (
            """query ($item: Float = 456.789e2) { nonNullListFloatField(param: [23456.789e2, $item]) }""",
            None,
            {"data": {"nonNullListFloatField": "SUCCESS-[2345681.9-45681.9]"}},
        ),
        (
            """query ($item: Float = 456.789e2) { nonNullListFloatField(param: [23456.789e2, $item]) }""",
            {"item": None},
            {"data": {"nonNullListFloatField": "SUCCESS-[2345681.9-None]"}},
        ),
        (
            """query ($item: Float = 456.789e2) { nonNullListFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {
                "data": {
                    "nonNullListFloatField": "SUCCESS-[2345681.9-345681.9]"
                }
            },
        ),
        (
            """query ($item: Float!) { nonNullListFloatField(param: [23456.789e2, $item]) }""",
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
            """query ($item: Float!) { nonNullListFloatField(param: [23456.789e2, $item]) }""",
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
            """query ($item: Float!) { nonNullListFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {
                "data": {
                    "nonNullListFloatField": "SUCCESS-[2345681.9-345681.9]"
                }
            },
        ),
    ],
)
async def test_coercion_non_null_list_float_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
