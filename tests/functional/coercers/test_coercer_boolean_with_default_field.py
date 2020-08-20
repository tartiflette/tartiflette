import pytest


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { booleanWithDefaultField }""",
            None,
            {"data": {"booleanWithDefaultField": "SUCCESS-True"}},
        ),
        (
            """query { booleanWithDefaultField(param: null) }""",
            None,
            {"data": {"booleanWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query { booleanWithDefaultField(param: false) }""",
            None,
            {"data": {"booleanWithDefaultField": "SUCCESS-False"}},
        ),
        (
            """query ($param: Boolean) { booleanWithDefaultField(param: $param) }""",
            None,
            {"data": {"booleanWithDefaultField": "SUCCESS-True"}},
        ),
        (
            """query ($param: Boolean) { booleanWithDefaultField(param: $param) }""",
            {"param": None},
            {"data": {"booleanWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query ($param: Boolean) { booleanWithDefaultField(param: $param) }""",
            {"param": True},
            {"data": {"booleanWithDefaultField": "SUCCESS-True"}},
        ),
        (
            """query ($param: Boolean = null) { booleanWithDefaultField(param: $param) }""",
            None,
            {"data": {"booleanWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query ($param: Boolean = null) { booleanWithDefaultField(param: $param) }""",
            {"param": None},
            {"data": {"booleanWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query ($param: Boolean = null) { booleanWithDefaultField(param: $param) }""",
            {"param": True},
            {"data": {"booleanWithDefaultField": "SUCCESS-True"}},
        ),
        (
            """query ($param: Boolean = false) { booleanWithDefaultField(param: $param) }""",
            None,
            {"data": {"booleanWithDefaultField": "SUCCESS-False"}},
        ),
        (
            """query ($param: Boolean = false) { booleanWithDefaultField(param: $param) }""",
            {"param": None},
            {"data": {"booleanWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query ($param: Boolean = false) { booleanWithDefaultField(param: $param) }""",
            {"param": True},
            {"data": {"booleanWithDefaultField": "SUCCESS-True"}},
        ),
        (
            """query ($param: Boolean!) { booleanWithDefaultField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < Boolean! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean!) { booleanWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < Boolean! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean!) { booleanWithDefaultField(param: $param) }""",
            {"param": True},
            {"data": {"booleanWithDefaultField": "SUCCESS-True"}},
        ),
    ],
)
async def test_coercion_boolean_with_default_field(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected
