import pytest


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { floatField }""",
            None,
            {"data": {"floatField": "SUCCESS"}},
        ),
        (
            """query { floatField(param: null) }""",
            None,
            {"data": {"floatField": "SUCCESS-None"}},
        ),
        (
            """query { floatField(param: 23456.789e2) }""",
            None,
            {"data": {"floatField": "SUCCESS-2345681.9"}},
        ),
        (
            """query ($param: Float) { floatField(param: $param) }""",
            None,
            {"data": {"floatField": "SUCCESS"}},
        ),
        (
            """query ($param: Float) { floatField(param: $param) }""",
            {"param": None},
            {"data": {"floatField": "SUCCESS-None"}},
        ),
        (
            """query ($param: Float) { floatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"floatField": "SUCCESS-345681.9"}},
        ),
        (
            """query ($param: Float = null) { floatField(param: $param) }""",
            None,
            {"data": {"floatField": "SUCCESS-None"}},
        ),
        (
            """query ($param: Float = null) { floatField(param: $param) }""",
            {"param": None},
            {"data": {"floatField": "SUCCESS-None"}},
        ),
        (
            """query ($param: Float = null) { floatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"floatField": "SUCCESS-345681.9"}},
        ),
        (
            """query ($param: Float = 456.789e2) { floatField(param: $param) }""",
            None,
            {"data": {"floatField": "SUCCESS-45681.9"}},
        ),
        (
            """query ($param: Float = 456.789e2) { floatField(param: $param) }""",
            {"param": None},
            {"data": {"floatField": "SUCCESS-None"}},
        ),
        (
            """query ($param: Float = 456.789e2) { floatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"floatField": "SUCCESS-345681.9"}},
        ),
        (
            """query ($param: Float!) { floatField(param: $param) }""",
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
            """query ($param: Float!) { floatField(param: $param) }""",
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
            """query ($param: Float!) { floatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"floatField": "SUCCESS-345681.9"}},
        ),
    ],
)
async def test_coercion_float_field(schema_stack, query, variables, expected):
    assert await schema_stack.execute(query, variables=variables) == expected
