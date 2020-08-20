import pytest


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { floatWithDefaultField }""",
            None,
            {"data": {"floatWithDefaultField": "SUCCESS-12345681.9"}},
        ),
        (
            """query { floatWithDefaultField(param: null) }""",
            None,
            {"data": {"floatWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query { floatWithDefaultField(param: 23456.789e2) }""",
            None,
            {"data": {"floatWithDefaultField": "SUCCESS-2345681.9"}},
        ),
        (
            """query ($param: Float) { floatWithDefaultField(param: $param) }""",
            None,
            {"data": {"floatWithDefaultField": "SUCCESS-12345681.9"}},
        ),
        (
            """query ($param: Float) { floatWithDefaultField(param: $param) }""",
            {"param": None},
            {"data": {"floatWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query ($param: Float) { floatWithDefaultField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"floatWithDefaultField": "SUCCESS-345681.9"}},
        ),
        (
            """query ($param: Float = null) { floatWithDefaultField(param: $param) }""",
            None,
            {"data": {"floatWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query ($param: Float = null) { floatWithDefaultField(param: $param) }""",
            {"param": None},
            {"data": {"floatWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query ($param: Float = null) { floatWithDefaultField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"floatWithDefaultField": "SUCCESS-345681.9"}},
        ),
        (
            """query ($param: Float = 456.789e2) { floatWithDefaultField(param: $param) }""",
            None,
            {"data": {"floatWithDefaultField": "SUCCESS-45681.9"}},
        ),
        (
            """query ($param: Float = 456.789e2) { floatWithDefaultField(param: $param) }""",
            {"param": None},
            {"data": {"floatWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query ($param: Float = 456.789e2) { floatWithDefaultField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"floatWithDefaultField": "SUCCESS-345681.9"}},
        ),
        (
            """query ($param: Float!) { floatWithDefaultField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < Float! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float!) { floatWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < Float! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float!) { floatWithDefaultField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"floatWithDefaultField": "SUCCESS-345681.9"}},
        ),
    ],
)
async def test_coercion_float_with_default_field(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected
