import pytest

from tests.functional.coercers.common import resolve_unwrapped_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion", resolvers={"Query.stringField": resolve_unwrapped_field}
)
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
            """query { stringField(param: "paramDefaultValue) }""",
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
async def test_coercion_string_field(engine, query, variables, expected):
    assert await engine.execute(query, variables=variables) == expected
