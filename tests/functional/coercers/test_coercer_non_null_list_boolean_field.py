import pytest


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullListBooleanField }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Field < nonNullListBooleanField > argument < param > of type < [Boolean]! > is required, but it was not provided.",
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
            """query { nonNullListBooleanField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < [Boolean]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 40}],
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
            """query { nonNullListBooleanField(param: [null]) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query { nonNullListBooleanField(param: false) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query { nonNullListBooleanField(param: [false]) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query { nonNullListBooleanField(param: [false, null]) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($param: [Boolean]!) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean]!) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean]!) { nonNullListBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]!) { nonNullListBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]!) { nonNullListBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]!) { nonNullListBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean]! = null) { nonNullListBooleanField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < [Boolean]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 29}],
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
            """query ($param: [Boolean]! = null) { nonNullListBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < [Boolean]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 29}],
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
            """query ($param: [Boolean]! = null) { nonNullListBooleanField(param: $param) }""",
            {"param": [None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < [Boolean]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 29}],
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
            """query ($param: [Boolean]! = null) { nonNullListBooleanField(param: $param) }""",
            {"param": True},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < [Boolean]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 29}],
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
            """query ($param: [Boolean]! = null) { nonNullListBooleanField(param: $param) }""",
            {"param": [True]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < [Boolean]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 29}],
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
            """query ($param: [Boolean]! = null) { nonNullListBooleanField(param: $param) }""",
            {"param": [True, None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < [Boolean]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 29}],
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
            """query ($param: [Boolean]! = [null]) { nonNullListBooleanField(param: $param) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]! = [null]) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean]! = [null]) { nonNullListBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]! = [null]) { nonNullListBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]! = [null]) { nonNullListBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]! = [null]) { nonNullListBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean]! = false) { nonNullListBooleanField(param: $param) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query ($param: [Boolean]! = false) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean]! = false) { nonNullListBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]! = false) { nonNullListBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]! = false) { nonNullListBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]! = false) { nonNullListBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean]! = [false]) { nonNullListBooleanField(param: $param) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query ($param: [Boolean]! = [false]) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean]! = [false]) { nonNullListBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]! = [false]) { nonNullListBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]! = [false]) { nonNullListBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]! = [false]) { nonNullListBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean]! = [false, null]) { nonNullListBooleanField(param: $param) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($param: [Boolean]! = [false, null]) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean]! = [false, null]) { nonNullListBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]! = [false, null]) { nonNullListBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]! = [false, null]) { nonNullListBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]! = [false, null]) { nonNullListBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean]!) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean]!) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean]!) { nonNullListBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]!) { nonNullListBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]!) { nonNullListBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]!) { nonNullListBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean!]!) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { nonNullListBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]!) { nonNullListBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]!) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { nonNullListBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]!) { nonNullListBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]!) { nonNullListBooleanField(param: $param) }""",
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
            """query ($item: Boolean) { nonNullListBooleanField(param: [false, $item]) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($item: Boolean) { nonNullListBooleanField(param: [false, $item]) }""",
            {"item": None},
            {"data": {"nonNullListBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($item: Boolean) { nonNullListBooleanField(param: [false, $item]) }""",
            {"item": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[False-True]"}},
        ),
        (
            """query ($item: Boolean = null) { nonNullListBooleanField(param: [false, $item]) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($item: Boolean = null) { nonNullListBooleanField(param: [false, $item]) }""",
            {"item": None},
            {"data": {"nonNullListBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($item: Boolean = null) { nonNullListBooleanField(param: [false, $item]) }""",
            {"item": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[False-True]"}},
        ),
        (
            """query ($item: Boolean = false) { nonNullListBooleanField(param: [false, $item]) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[False-False]"}},
        ),
        (
            """query ($item: Boolean = false) { nonNullListBooleanField(param: [false, $item]) }""",
            {"item": None},
            {"data": {"nonNullListBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($item: Boolean = false) { nonNullListBooleanField(param: [false, $item]) }""",
            {"item": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[False-True]"}},
        ),
        (
            """query ($item: Boolean!) { nonNullListBooleanField(param: [false, $item]) }""",
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
            """query ($item: Boolean!) { nonNullListBooleanField(param: [false, $item]) }""",
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
            """query ($item: Boolean!) { nonNullListBooleanField(param: [false, $item]) }""",
            {"item": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[False-True]"}},
        ),
    ],
)
async def test_coercion_non_null_list_boolean_field(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected
