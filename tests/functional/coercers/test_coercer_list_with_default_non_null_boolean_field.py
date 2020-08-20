import pytest


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { listWithDefaultNonNullBooleanField }""",
            None,
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query { listWithDefaultNonNullBooleanField(param: null) }""",
            None,
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query { listWithDefaultNonNullBooleanField(param: [null]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
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
            """query { listWithDefaultNonNullBooleanField(param: false) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[False]"
                }
            },
        ),
        (
            """query { listWithDefaultNonNullBooleanField(param: [false]) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[False]"
                }
            },
        ),
        (
            """query { listWithDefaultNonNullBooleanField(param: [false, null]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 59}],
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
            """query ($param: [Boolean!]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            None,
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean!]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!] = null) { listWithDefaultNonNullBooleanField(param: $param) }""",
            None,
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean!] = null) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean!] = null) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!] = null) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!] = [null]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
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
            """query ($param: [Boolean!] = [null]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
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
            """query ($param: [Boolean!] = [null]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": True},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
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
            """query ($param: [Boolean!] = [null]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
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
            """query ($param: [Boolean!] = false) { listWithDefaultNonNullBooleanField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[False]"
                }
            },
        ),
        (
            """query ($param: [Boolean!] = false) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean!] = false) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!] = false) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!] = [false]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[False]"
                }
            },
        ),
        (
            """query ($param: [Boolean!] = [false]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean!] = [false]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!] = [false]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!] = [false, null]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 37}],
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
            """query ($param: [Boolean!] = [false, null]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 37}],
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
            """query ($param: [Boolean!] = [false, null]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": True},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 37}],
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
            """query ($param: [Boolean!] = [false, null]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 37}],
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
            """query ($param: [Boolean!]!) { listWithDefaultNonNullBooleanField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < [Boolean!]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean!]!) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < [Boolean!]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean!]!) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]!) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            None,
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean!]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [None] >; Expected non-nullable type < Boolean! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean!]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True, None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [True, None] >; Expected non-nullable type < Boolean! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean!]!) { listWithDefaultNonNullBooleanField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < [Boolean!]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean!]!) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < [Boolean!]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean!]!) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [None] >; Expected non-nullable type < Boolean! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean!]!) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]!) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]!) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True, None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [True, None] >; Expected non-nullable type < Boolean! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($item: Boolean) { listWithDefaultNonNullBooleanField(param: [false, $item]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 1, "column": 8},
                            {"line": 1, "column": 76},
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
            """query ($item: Boolean) { listWithDefaultNonNullBooleanField(param: [false, $item]) }""",
            {"item": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 1, "column": 8},
                            {"line": 1, "column": 76},
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
            """query ($item: Boolean) { listWithDefaultNonNullBooleanField(param: [false, $item]) }""",
            {"item": True},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 1, "column": 8},
                            {"line": 1, "column": 76},
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
            """query ($item: Boolean = null) { listWithDefaultNonNullBooleanField(param: [false, $item]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 1, "column": 8},
                            {"line": 1, "column": 83},
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
            """query ($item: Boolean = null) { listWithDefaultNonNullBooleanField(param: [false, $item]) }""",
            {"item": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 1, "column": 8},
                            {"line": 1, "column": 83},
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
            """query ($item: Boolean = null) { listWithDefaultNonNullBooleanField(param: [false, $item]) }""",
            {"item": True},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 1, "column": 8},
                            {"line": 1, "column": 83},
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
            """query ($item: Boolean = false) { listWithDefaultNonNullBooleanField(param: [false, $item]) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[False-False]"
                }
            },
        ),
        (
            """query ($item: Boolean = false) { listWithDefaultNonNullBooleanField(param: [false, $item]) }""",
            {"item": None},
            {
                "data": {"listWithDefaultNonNullBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [false, $item] >.",
                        "path": ["listWithDefaultNonNullBooleanField"],
                        "locations": [{"line": 1, "column": 76}],
                    }
                ],
            },
        ),
        (
            """query ($item: Boolean = false) { listWithDefaultNonNullBooleanField(param: [false, $item]) }""",
            {"item": True},
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[False-True]"
                }
            },
        ),
        (
            """query ($item: Boolean!) { listWithDefaultNonNullBooleanField(param: [false, $item]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of required type < Boolean! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($item: Boolean!) { listWithDefaultNonNullBooleanField(param: [false, $item]) }""",
            {"item": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of non-null type < Boolean! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($item: Boolean!) { listWithDefaultNonNullBooleanField(param: [false, $item]) }""",
            {"item": True},
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[False-True]"
                }
            },
        ),
    ],
)
async def test_coercion_list_with_default_non_null_boolean_field(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected
