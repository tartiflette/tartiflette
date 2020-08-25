import pytest


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullEnumWithDefaultField }""",
            None,
            {
                "data": {
                    "nonNullEnumWithDefaultField": "SUCCESS-ENUM_1_1-MyEnum-nonNullEnumWithDefaultField"
                }
            },
        ),
        (
            """query { nonNullEnumWithDefaultField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 44}],
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
            """query { nonNullEnumWithDefaultField(param: ENUM_2) }""",
            None,
            {
                "data": {
                    "nonNullEnumWithDefaultField": "SUCCESS-ENUM_2_2-MyEnum-nonNullEnumWithDefaultField"
                }
            },
        ),
        (
            """query ($param: MyEnum) { nonNullEnumWithDefaultField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullEnumWithDefaultField": "SUCCESS-ENUM_1_1-MyEnum-nonNullEnumWithDefaultField"
                }
            },
        ),
        (
            """query ($param: MyEnum) { nonNullEnumWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullEnumWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < MyEnum! > must not be null.",
                        "path": ["nonNullEnumWithDefaultField"],
                        "locations": [{"line": 1, "column": 61}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum) { nonNullEnumWithDefaultField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "nonNullEnumWithDefaultField": "SUCCESS-ENUM_3_3-MyEnum-nonNullEnumWithDefaultField"
                }
            },
        ),
        (
            """query ($param: MyEnum = null) { nonNullEnumWithDefaultField(param: $param) }""",
            None,
            {
                "data": {"nonNullEnumWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < MyEnum! > must not be null.",
                        "path": ["nonNullEnumWithDefaultField"],
                        "locations": [{"line": 1, "column": 68}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum = null) { nonNullEnumWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullEnumWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < MyEnum! > must not be null.",
                        "path": ["nonNullEnumWithDefaultField"],
                        "locations": [{"line": 1, "column": 68}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum = null) { nonNullEnumWithDefaultField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "nonNullEnumWithDefaultField": "SUCCESS-ENUM_3_3-MyEnum-nonNullEnumWithDefaultField"
                }
            },
        ),
        (
            """query ($param: MyEnum = ENUM_4) { nonNullEnumWithDefaultField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullEnumWithDefaultField": "SUCCESS-ENUM_4_4-MyEnum-nonNullEnumWithDefaultField"
                }
            },
        ),
        (
            """query ($param: MyEnum = ENUM_4) { nonNullEnumWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullEnumWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < MyEnum! > must not be null.",
                        "path": ["nonNullEnumWithDefaultField"],
                        "locations": [{"line": 1, "column": 70}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum = ENUM_4) { nonNullEnumWithDefaultField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "nonNullEnumWithDefaultField": "SUCCESS-ENUM_3_3-MyEnum-nonNullEnumWithDefaultField"
                }
            },
        ),
        (
            """query ($param: MyEnum!) { nonNullEnumWithDefaultField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < MyEnum! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum!) { nonNullEnumWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < MyEnum! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum!) { nonNullEnumWithDefaultField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "nonNullEnumWithDefaultField": "SUCCESS-ENUM_3_3-MyEnum-nonNullEnumWithDefaultField"
                }
            },
        ),
    ],
)
async def test_coercion_non_null_enum_with_default_field(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected
