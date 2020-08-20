import pytest


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullStringWithDefaultField }""",
            None,
            {
                "data": {
                    "nonNullStringWithDefaultField": "SUCCESS-defaultstring-scalar-nonNullStringWithDefaultField"
                }
            },
        ),
        (
            """query { nonNullStringWithDefaultField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < String! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 46}],
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
            """query { nonNullStringWithDefaultField(param: "paramDefaultValue") }""",
            None,
            {
                "data": {
                    "nonNullStringWithDefaultField": "SUCCESS-paramdefaultvalue-scalar-nonNullStringWithDefaultField"
                }
            },
        ),
        (
            """query ($param: String) { nonNullStringWithDefaultField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullStringWithDefaultField": "SUCCESS-defaultstring-scalar-nonNullStringWithDefaultField"
                }
            },
        ),
        (
            """query ($param: String) { nonNullStringWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullStringWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < String! > must not be null.",
                        "path": ["nonNullStringWithDefaultField"],
                        "locations": [{"line": 1, "column": 63}],
                    }
                ],
            },
        ),
        (
            """query ($param: String) { nonNullStringWithDefaultField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "nonNullStringWithDefaultField": "SUCCESS-varvalue-scalar-nonNullStringWithDefaultField"
                }
            },
        ),
        (
            """query ($param: String = null) { nonNullStringWithDefaultField(param: $param) }""",
            None,
            {
                "data": {"nonNullStringWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < String! > must not be null.",
                        "path": ["nonNullStringWithDefaultField"],
                        "locations": [{"line": 1, "column": 70}],
                    }
                ],
            },
        ),
        (
            """query ($param: String = null) { nonNullStringWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullStringWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < String! > must not be null.",
                        "path": ["nonNullStringWithDefaultField"],
                        "locations": [{"line": 1, "column": 70}],
                    }
                ],
            },
        ),
        (
            """query ($param: String = null) { nonNullStringWithDefaultField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "nonNullStringWithDefaultField": "SUCCESS-varvalue-scalar-nonNullStringWithDefaultField"
                }
            },
        ),
        (
            """query ($param: String = "varDefault") { nonNullStringWithDefaultField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullStringWithDefaultField": "SUCCESS-vardefault-scalar-nonNullStringWithDefaultField"
                }
            },
        ),
        (
            """query ($param: String = "varDefault") { nonNullStringWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullStringWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < String! > must not be null.",
                        "path": ["nonNullStringWithDefaultField"],
                        "locations": [{"line": 1, "column": 78}],
                    }
                ],
            },
        ),
        (
            """query ($param: String = "varDefault") { nonNullStringWithDefaultField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "nonNullStringWithDefaultField": "SUCCESS-varvalue-scalar-nonNullStringWithDefaultField"
                }
            },
        ),
        (
            """query ($param: String!) { nonNullStringWithDefaultField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < String! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: String!) { nonNullStringWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < String! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: String!) { nonNullStringWithDefaultField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "nonNullStringWithDefaultField": "SUCCESS-varvalue-scalar-nonNullStringWithDefaultField"
                }
            },
        ),
    ],
)
async def test_coercion_non_null_string_with_default_field(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected
