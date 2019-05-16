import pytest

from tests.functional.coercers.common import resolve_unwrapped_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.stringWithDefaultField": resolve_unwrapped_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { stringWithDefaultField }""",
            None,
            {
                "data": {
                    "stringWithDefaultField": "SUCCESS-defaultstring-scalar-stringWithDefaultField"
                }
            },
        ),
        (
            """query { stringWithDefaultField(param: null) }""",
            None,
            {"data": {"stringWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query { stringWithDefaultField(param: "paramDefaultValue") }""",
            None,
            {
                "data": {
                    "stringWithDefaultField": "SUCCESS-paramdefaultvalue-scalar-stringWithDefaultField"
                }
            },
        ),
        (
            """query ($param: String) { stringWithDefaultField(param: $param) }""",
            None,
            {
                "data": {
                    "stringWithDefaultField": "SUCCESS-defaultstring-scalar-stringWithDefaultField"
                }
            },
        ),
        (
            """query ($param: String) { stringWithDefaultField(param: $param) }""",
            {"param": None},
            {"data": {"stringWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query ($param: String) { stringWithDefaultField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "stringWithDefaultField": "SUCCESS-varvalue-scalar-stringWithDefaultField"
                }
            },
        ),
        (
            """query ($param: String = null) { stringWithDefaultField(param: $param) }""",
            None,
            {"data": {"stringWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query ($param: String = null) { stringWithDefaultField(param: $param) }""",
            {"param": None},
            {"data": {"stringWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query ($param: String = null) { stringWithDefaultField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "stringWithDefaultField": "SUCCESS-varvalue-scalar-stringWithDefaultField"
                }
            },
        ),
        (
            """query ($param: String = "varDefault") { stringWithDefaultField(param: $param) }""",
            None,
            {
                "data": {
                    "stringWithDefaultField": "SUCCESS-vardefault-scalar-stringWithDefaultField"
                }
            },
        ),
        (
            """query ($param: String = "varDefault") { stringWithDefaultField(param: $param) }""",
            {"param": None},
            {"data": {"stringWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query ($param: String = "varDefault") { stringWithDefaultField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "stringWithDefaultField": "SUCCESS-varvalue-scalar-stringWithDefaultField"
                }
            },
        ),
        (
            """query ($param: String!) { stringWithDefaultField(param: $param) }""",
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
            """query ($param: String!) { stringWithDefaultField(param: $param) }""",
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
            """query ($param: String!) { stringWithDefaultField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "stringWithDefaultField": "SUCCESS-varvalue-scalar-stringWithDefaultField"
                }
            },
        ),
    ],
)
async def test_coercion_string_with_default_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
