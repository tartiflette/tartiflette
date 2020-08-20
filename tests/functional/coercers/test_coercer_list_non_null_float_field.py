import pytest


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { listNonNullFloatField }""",
            None,
            {"data": {"listNonNullFloatField": "SUCCESS"}},
        ),
        (
            """query { listNonNullFloatField(param: null) }""",
            None,
            {"data": {"listNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query { listNonNullFloatField(param: [null]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 39}],
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
            """query { listNonNullFloatField(param: 23456.789e2) }""",
            None,
            {"data": {"listNonNullFloatField": "SUCCESS-[2345681.9]"}},
        ),
        (
            """query { listNonNullFloatField(param: [23456.789e2]) }""",
            None,
            {"data": {"listNonNullFloatField": "SUCCESS-[2345681.9]"}},
        ),
        (
            """query { listNonNullFloatField(param: [23456.789e2, null]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 52}],
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
            """query ($param: [Float!]) { listNonNullFloatField(param: $param) }""",
            None,
            {"data": {"listNonNullFloatField": "SUCCESS"}},
        ),
        (
            """query ($param: [Float!]) { listNonNullFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float!]) { listNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!]) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!] = null) { listNonNullFloatField(param: $param) }""",
            None,
            {"data": {"listNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float!] = null) { listNonNullFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float!] = null) { listNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!] = null) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!] = [null]) { listNonNullFloatField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 28}],
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
            """query ($param: [Float!] = [null]) { listNonNullFloatField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 28}],
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
            """query ($param: [Float!] = [null]) { listNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 28}],
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
            """query ($param: [Float!] = [null]) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 28}],
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
            """query ($param: [Float!] = 456.789e2) { listNonNullFloatField(param: $param) }""",
            None,
            {"data": {"listNonNullFloatField": "SUCCESS-[45681.9]"}},
        ),
        (
            """query ($param: [Float!] = 456.789e2) { listNonNullFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float!] = 456.789e2) { listNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!] = 456.789e2) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!] = [456.789e2]) { listNonNullFloatField(param: $param) }""",
            None,
            {"data": {"listNonNullFloatField": "SUCCESS-[45681.9]"}},
        ),
        (
            """query ($param: [Float!] = [456.789e2]) { listNonNullFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float!] = [456.789e2]) { listNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!] = [456.789e2]) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!] = [456.789e2, null]) { listNonNullFloatField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 39}],
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
            """query ($param: [Float!] = [456.789e2, null]) { listNonNullFloatField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 39}],
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
            """query ($param: [Float!] = [456.789e2, null]) { listNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 39}],
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
            """query ($param: [Float!] = [456.789e2, null]) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 39}],
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
            """query ($param: [Float!]!) { listNonNullFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { listNonNullFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { listNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!]!) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!]) { listNonNullFloatField(param: $param) }""",
            None,
            {"data": {"listNonNullFloatField": "SUCCESS"}},
        ),
        (
            """query ($param: [Float!]) { listNonNullFloatField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullFloatField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Float!]) { listNonNullFloatField(param: $param) }""",
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
            """query ($param: [Float!]) { listNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!]) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!]) { listNonNullFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { listNonNullFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { listNonNullFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { listNonNullFloatField(param: $param) }""",
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
            """query ($param: [Float!]!) { listNonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!]!) { listNonNullFloatField(param: $param) }""",
            {"param": [3456.789e2]},
            {"data": {"listNonNullFloatField": "SUCCESS-[345681.9]"}},
        ),
        (
            """query ($param: [Float!]!) { listNonNullFloatField(param: $param) }""",
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
            """query ($item: Float) { listNonNullFloatField(param: [23456.789e2, $item]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 1, "column": 8},
                            {"line": 1, "column": 67},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    }
                ],
            },
        ),
        (
            """query ($item: Float) { listNonNullFloatField(param: [23456.789e2, $item]) }""",
            {"item": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 1, "column": 8},
                            {"line": 1, "column": 67},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    }
                ],
            },
        ),
        (
            """query ($item: Float) { listNonNullFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 1, "column": 8},
                            {"line": 1, "column": 67},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    }
                ],
            },
        ),
        (
            """query ($item: Float = null) { listNonNullFloatField(param: [23456.789e2, $item]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 1, "column": 8},
                            {"line": 1, "column": 74},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    }
                ],
            },
        ),
        (
            """query ($item: Float = null) { listNonNullFloatField(param: [23456.789e2, $item]) }""",
            {"item": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 1, "column": 8},
                            {"line": 1, "column": 74},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    }
                ],
            },
        ),
        (
            """query ($item: Float = null) { listNonNullFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 1, "column": 8},
                            {"line": 1, "column": 74},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    }
                ],
            },
        ),
        (
            """query ($item: Float = 456.789e2) { listNonNullFloatField(param: [23456.789e2, $item]) }""",
            None,
            {"data": {"listNonNullFloatField": "SUCCESS-[2345681.9-45681.9]"}},
        ),
        (
            """query ($item: Float = 456.789e2) { listNonNullFloatField(param: [23456.789e2, $item]) }""",
            {"item": None},
            {
                "data": {"listNonNullFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [23456.789e2, $item] >.",
                        "path": ["listNonNullFloatField"],
                        "locations": [{"line": 1, "column": 65}],
                    }
                ],
            },
        ),
        (
            """query ($item: Float = 456.789e2) { listNonNullFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {
                "data": {
                    "listNonNullFloatField": "SUCCESS-[2345681.9-345681.9]"
                }
            },
        ),
        (
            """query ($item: Float!) { listNonNullFloatField(param: [23456.789e2, $item]) }""",
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
            """query ($item: Float!) { listNonNullFloatField(param: [23456.789e2, $item]) }""",
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
            """query ($item: Float!) { listNonNullFloatField(param: [23456.789e2, $item]) }""",
            {"item": 3456.789e2},
            {
                "data": {
                    "listNonNullFloatField": "SUCCESS-[2345681.9-345681.9]"
                }
            },
        ),
    ],
)
async def test_coercion_list_non_null_float_field(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected
