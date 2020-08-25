import pytest


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { listNonNullBooleanField }""",
            None,
            {"data": {"listNonNullBooleanField": "SUCCESS"}},
        ),
        (
            """query { listNonNullBooleanField(param: null) }""",
            None,
            {"data": {"listNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query { listNonNullBooleanField(param: [null]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 41}],
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
            """query { listNonNullBooleanField(param: false) }""",
            None,
            {"data": {"listNonNullBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query { listNonNullBooleanField(param: [false]) }""",
            None,
            {"data": {"listNonNullBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query { listNonNullBooleanField(param: [false, null]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
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
            """query ($param: [Boolean!]) { listNonNullBooleanField(param: $param) }""",
            None,
            {"data": {"listNonNullBooleanField": "SUCCESS"}},
        ),
        (
            """query ($param: [Boolean!]) { listNonNullBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean!]) { listNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]) { listNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!] = null) { listNonNullBooleanField(param: $param) }""",
            None,
            {"data": {"listNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean!] = null) { listNonNullBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean!] = null) { listNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!] = null) { listNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!] = [null]) { listNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!] = [null]) { listNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!] = [null]) { listNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!] = [null]) { listNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!] = false) { listNonNullBooleanField(param: $param) }""",
            None,
            {"data": {"listNonNullBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query ($param: [Boolean!] = false) { listNonNullBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean!] = false) { listNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!] = false) { listNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!] = [false]) { listNonNullBooleanField(param: $param) }""",
            None,
            {"data": {"listNonNullBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query ($param: [Boolean!] = [false]) { listNonNullBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean!] = [false]) { listNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!] = [false]) { listNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!] = [false, null]) { listNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!] = [false, null]) { listNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!] = [false, null]) { listNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { listNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { listNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { listNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]!) { listNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]) { listNonNullBooleanField(param: $param) }""",
            None,
            {"data": {"listNonNullBooleanField": "SUCCESS"}},
        ),
        (
            """query ($param: [Boolean!]) { listNonNullBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean!]) { listNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]) { listNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]) { listNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]) { listNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { listNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { listNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { listNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { listNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]!) { listNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]!) { listNonNullBooleanField(param: $param) }""",
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
            """query ($item: Boolean) { listNonNullBooleanField(param: [false, $item]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < Boolean > used in position expecting type < Boolean! >.",
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
            """query ($item: Boolean) { listNonNullBooleanField(param: [false, $item]) }""",
            {"item": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < Boolean > used in position expecting type < Boolean! >.",
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
            """query ($item: Boolean) { listNonNullBooleanField(param: [false, $item]) }""",
            {"item": True},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < Boolean > used in position expecting type < Boolean! >.",
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
            """query ($item: Boolean = null) { listNonNullBooleanField(param: [false, $item]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < Boolean > used in position expecting type < Boolean! >.",
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
            """query ($item: Boolean = null) { listNonNullBooleanField(param: [false, $item]) }""",
            {"item": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < Boolean > used in position expecting type < Boolean! >.",
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
            """query ($item: Boolean = null) { listNonNullBooleanField(param: [false, $item]) }""",
            {"item": True},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < Boolean > used in position expecting type < Boolean! >.",
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
            """query ($item: Boolean = false) { listNonNullBooleanField(param: [false, $item]) }""",
            None,
            {"data": {"listNonNullBooleanField": "SUCCESS-[False-False]"}},
        ),
        (
            """query ($item: Boolean = false) { listNonNullBooleanField(param: [false, $item]) }""",
            {"item": None},
            {
                "data": {"listNonNullBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [false, $item] >.",
                        "path": ["listNonNullBooleanField"],
                        "locations": [{"line": 1, "column": 65}],
                    }
                ],
            },
        ),
        (
            """query ($item: Boolean = false) { listNonNullBooleanField(param: [false, $item]) }""",
            {"item": True},
            {"data": {"listNonNullBooleanField": "SUCCESS-[False-True]"}},
        ),
        (
            """query ($item: Boolean!) { listNonNullBooleanField(param: [false, $item]) }""",
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
            """query ($item: Boolean!) { listNonNullBooleanField(param: [false, $item]) }""",
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
            """query ($item: Boolean!) { listNonNullBooleanField(param: [false, $item]) }""",
            {"item": True},
            {"data": {"listNonNullBooleanField": "SUCCESS-[False-True]"}},
        ),
    ],
)
async def test_coercion_list_non_null_boolean_field(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected
