import pytest


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { enumWithDefaultField }""",
            None,
            {
                "data": {
                    "enumWithDefaultField": "SUCCESS-ENUM_1_1-MyEnum-enumWithDefaultField"
                }
            },
        ),
        (
            """query { enumWithDefaultField(param: null) }""",
            None,
            {"data": {"enumWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query { enumWithDefaultField(param: ENUM_2) }""",
            None,
            {
                "data": {
                    "enumWithDefaultField": "SUCCESS-ENUM_2_2-MyEnum-enumWithDefaultField"
                }
            },
        ),
        (
            """query ($param: MyEnum) { enumWithDefaultField(param: $param) }""",
            None,
            {
                "data": {
                    "enumWithDefaultField": "SUCCESS-ENUM_1_1-MyEnum-enumWithDefaultField"
                }
            },
        ),
        (
            """query ($param: MyEnum) { enumWithDefaultField(param: $param) }""",
            {"param": None},
            {"data": {"enumWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query ($param: MyEnum) { enumWithDefaultField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "enumWithDefaultField": "SUCCESS-ENUM_3_3-MyEnum-enumWithDefaultField"
                }
            },
        ),
        (
            """query ($param: MyEnum = null) { enumWithDefaultField(param: $param) }""",
            None,
            {"data": {"enumWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query ($param: MyEnum = null) { enumWithDefaultField(param: $param) }""",
            {"param": None},
            {"data": {"enumWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query ($param: MyEnum = null) { enumWithDefaultField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "enumWithDefaultField": "SUCCESS-ENUM_3_3-MyEnum-enumWithDefaultField"
                }
            },
        ),
        (
            """query ($param: MyEnum = ENUM_4) { enumWithDefaultField(param: $param) }""",
            None,
            {
                "data": {
                    "enumWithDefaultField": "SUCCESS-ENUM_4_4-MyEnum-enumWithDefaultField"
                }
            },
        ),
        (
            """query ($param: MyEnum = ENUM_4) { enumWithDefaultField(param: $param) }""",
            {"param": None},
            {"data": {"enumWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query ($param: MyEnum = ENUM_4) { enumWithDefaultField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "enumWithDefaultField": "SUCCESS-ENUM_3_3-MyEnum-enumWithDefaultField"
                }
            },
        ),
        (
            """query ($param: MyEnum!) { enumWithDefaultField(param: $param) }""",
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
            """query ($param: MyEnum!) { enumWithDefaultField(param: $param) }""",
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
            """query ($param: MyEnum!) { enumWithDefaultField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "enumWithDefaultField": "SUCCESS-ENUM_3_3-MyEnum-enumWithDefaultField"
                }
            },
        ),
    ],
)
async def test_coercion_enum_with_default_field(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected
