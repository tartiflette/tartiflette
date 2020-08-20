import pytest


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { stringField }""",
            None,
            {"data": {"stringField": "SUCCESS"}},
        ),
        (
            """query { stringField(param: null) }""",
            None,
            {"data": {"stringField": "SUCCESS-None"}},
        ),
        (
            """query { stringField(param: "paramDefaultValue") }""",
            None,
            {
                "data": {
                    "stringField": "SUCCESS-paramdefaultvalue-scalar-stringField"
                }
            },
        ),
        (
            """query ($param: String) { stringField(param: $param) }""",
            None,
            {"data": {"stringField": "SUCCESS"}},
        ),
        (
            """query ($param: String) { stringField(param: $param) }""",
            {"param": None},
            {"data": {"stringField": "SUCCESS-None"}},
        ),
        (
            """query ($param: String) { stringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"stringField": "SUCCESS-varvalue-scalar-stringField"}},
        ),
        (
            """query ($param: String = null) { stringField(param: $param) }""",
            None,
            {"data": {"stringField": "SUCCESS-None"}},
        ),
        (
            """query ($param: String = null) { stringField(param: $param) }""",
            {"param": None},
            {"data": {"stringField": "SUCCESS-None"}},
        ),
        (
            """query ($param: String = null) { stringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"stringField": "SUCCESS-varvalue-scalar-stringField"}},
        ),
        (
            """query ($param: String = "varDefault") { stringField(param: $param) }""",
            None,
            {"data": {"stringField": "SUCCESS-vardefault-scalar-stringField"}},
        ),
        (
            """query ($param: String = "varDefault") { stringField(param: $param) }""",
            {"param": None},
            {"data": {"stringField": "SUCCESS-None"}},
        ),
        (
            """query ($param: String = "varDefault") { stringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"stringField": "SUCCESS-varvalue-scalar-stringField"}},
        ),
        (
            """query ($param: String!) { stringField(param: $param) }""",
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
            """query ($param: String!) { stringField(param: $param) }""",
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
            """query ($param: String!) { stringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"stringField": "SUCCESS-varvalue-scalar-stringField"}},
        ),
    ],
)
async def test_coercion_string_field(schema_stack, query, variables, expected):
    assert await schema_stack.execute(query, variables=variables) == expected
