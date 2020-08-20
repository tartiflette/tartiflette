import pytest


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
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
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 48}],
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
                        "message": "Expected value of type < Int! >, found < null >.",
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
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 26}],
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
            """query ($param: [Int!] = [null]) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 26}],
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
            """query ($param: [Int!] = [null]) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": 20},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 26}],
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
            """query ($param: [Int!] = [null]) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": [20]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 26}],
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
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 30}],
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
            """query ($param: [Int!] = [30, null]) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 30}],
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
            """query ($param: [Int!] = [30, null]) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": 20},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 30}],
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
            """query ($param: [Int!] = [30, null]) { listWithDefaultNonNullIntField(param: $param) }""",
            {"param": [20]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 30}],
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
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 1, "column": 8},
                            {"line": 1, "column": 65},
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
            """query ($item: Int) { listWithDefaultNonNullIntField(param: [10, $item]) }""",
            {"item": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 1, "column": 8},
                            {"line": 1, "column": 65},
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
            """query ($item: Int) { listWithDefaultNonNullIntField(param: [10, $item]) }""",
            {"item": 20},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 1, "column": 8},
                            {"line": 1, "column": 65},
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
            """query ($item: Int = null) { listWithDefaultNonNullIntField(param: [10, $item]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 1, "column": 8},
                            {"line": 1, "column": 72},
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
            """query ($item: Int = null) { listWithDefaultNonNullIntField(param: [10, $item]) }""",
            {"item": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 1, "column": 8},
                            {"line": 1, "column": 72},
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
            """query ($item: Int = null) { listWithDefaultNonNullIntField(param: [10, $item]) }""",
            {"item": 20},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 1, "column": 8},
                            {"line": 1, "column": 72},
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
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected
