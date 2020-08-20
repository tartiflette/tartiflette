import pytest


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullListWithDefaultBooleanField }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[True-None]"
                }
            },
        ),
        (
            """query { nonNullListWithDefaultBooleanField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < [Boolean]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 51}],
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
            """query { nonNullListWithDefaultBooleanField(param: [null]) }""",
            None,
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query { nonNullListWithDefaultBooleanField(param: false) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[False]"
                }
            },
        ),
        (
            """query { nonNullListWithDefaultBooleanField(param: [false]) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[False]"
                }
            },
        ),
        (
            """query { nonNullListWithDefaultBooleanField(param: [false, null]) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[False-None]"
                }
            },
        ),
        (
            """query ($param: [Boolean]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[True-None]"
                }
            },
        ),
        (
            """query ($param: [Boolean]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Boolean]! > must not be null.",
                        "path": ["nonNullListWithDefaultBooleanField"],
                        "locations": [{"line": 1, "column": 71}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": [True, None]},
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[True-None]"
                }
            },
        ),
        (
            """query ($param: [Boolean] = null) { nonNullListWithDefaultBooleanField(param: $param) }""",
            None,
            {
                "data": {"nonNullListWithDefaultBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Boolean]! > must not be null.",
                        "path": ["nonNullListWithDefaultBooleanField"],
                        "locations": [{"line": 1, "column": 78}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean] = null) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Boolean]! > must not be null.",
                        "path": ["nonNullListWithDefaultBooleanField"],
                        "locations": [{"line": 1, "column": 78}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean] = null) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = null) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = null) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = null) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": [True, None]},
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[True-None]"
                }
            },
        ),
        (
            """query ($param: [Boolean] = [null]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            None,
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Boolean]! > must not be null.",
                        "path": ["nonNullListWithDefaultBooleanField"],
                        "locations": [{"line": 1, "column": 80}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean] = [null]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": [True, None]},
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[True-None]"
                }
            },
        ),
        (
            """query ($param: [Boolean] = false) { nonNullListWithDefaultBooleanField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[False]"
                }
            },
        ),
        (
            """query ($param: [Boolean] = false) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Boolean]! > must not be null.",
                        "path": ["nonNullListWithDefaultBooleanField"],
                        "locations": [{"line": 1, "column": 79}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean] = false) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = false) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = false) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = false) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": [True, None]},
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[True-None]"
                }
            },
        ),
        (
            """query ($param: [Boolean] = [false]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[False]"
                }
            },
        ),
        (
            """query ($param: [Boolean] = [false]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Boolean]! > must not be null.",
                        "path": ["nonNullListWithDefaultBooleanField"],
                        "locations": [{"line": 1, "column": 81}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean] = [false]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": [True, None]},
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[True-None]"
                }
            },
        ),
        (
            """query ($param: [Boolean] = [false, null]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[False-None]"
                }
            },
        ),
        (
            """query ($param: [Boolean] = [false, null]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Boolean]! > must not be null.",
                        "path": ["nonNullListWithDefaultBooleanField"],
                        "locations": [{"line": 1, "column": 87}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean] = [false, null]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": [True, None]},
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[True-None]"
                }
            },
        ),
        (
            """query ($param: [Boolean]!) { nonNullListWithDefaultBooleanField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < [Boolean]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean]!) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < [Boolean]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean]!) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]!) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]!) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]!) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": [True, None]},
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[True-None]"
                }
            },
        ),
        (
            """query ($param: [Boolean!]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[True-None]"
                }
            },
        ),
        (
            """query ($param: [Boolean!]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Boolean]! > must not be null.",
                        "path": ["nonNullListWithDefaultBooleanField"],
                        "locations": [{"line": 1, "column": 72}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean!]) { nonNullListWithDefaultBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]) { nonNullListWithDefaultBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { nonNullListWithDefaultBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { nonNullListWithDefaultBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { nonNullListWithDefaultBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]!) { nonNullListWithDefaultBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]!) { nonNullListWithDefaultBooleanField(param: $param) }""",
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
            """query ($item: Boolean) { nonNullListWithDefaultBooleanField(param: [false, $item]) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[False-None]"
                }
            },
        ),
        (
            """query ($item: Boolean) { nonNullListWithDefaultBooleanField(param: [false, $item]) }""",
            {"item": None},
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[False-None]"
                }
            },
        ),
        (
            """query ($item: Boolean) { nonNullListWithDefaultBooleanField(param: [false, $item]) }""",
            {"item": True},
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[False-True]"
                }
            },
        ),
        (
            """query ($item: Boolean = null) { nonNullListWithDefaultBooleanField(param: [false, $item]) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[False-None]"
                }
            },
        ),
        (
            """query ($item: Boolean = null) { nonNullListWithDefaultBooleanField(param: [false, $item]) }""",
            {"item": None},
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[False-None]"
                }
            },
        ),
        (
            """query ($item: Boolean = null) { nonNullListWithDefaultBooleanField(param: [false, $item]) }""",
            {"item": True},
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[False-True]"
                }
            },
        ),
        (
            """query ($item: Boolean = false) { nonNullListWithDefaultBooleanField(param: [false, $item]) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[False-False]"
                }
            },
        ),
        (
            """query ($item: Boolean = false) { nonNullListWithDefaultBooleanField(param: [false, $item]) }""",
            {"item": None},
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[False-None]"
                }
            },
        ),
        (
            """query ($item: Boolean = false) { nonNullListWithDefaultBooleanField(param: [false, $item]) }""",
            {"item": True},
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[False-True]"
                }
            },
        ),
        (
            """query ($item: Boolean!) { nonNullListWithDefaultBooleanField(param: [false, $item]) }""",
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
            """query ($item: Boolean!) { nonNullListWithDefaultBooleanField(param: [false, $item]) }""",
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
            """query ($item: Boolean!) { nonNullListWithDefaultBooleanField(param: [false, $item]) }""",
            {"item": True},
            {
                "data": {
                    "nonNullListWithDefaultBooleanField": "SUCCESS-[False-True]"
                }
            },
        ),
    ],
)
async def test_coercion_non_null_with_default_list_boolean_field(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected
