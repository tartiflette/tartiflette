import pytest

from tests.functional.coercers.common import resolve_unwrapped_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.nonNullStringField": resolve_unwrapped_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullStringField }""",
            None,
            {
                "data": {"nonNullStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < String! > was not provided.",
                        "path": ["nonNullStringField"],
                        "locations": [{"line": 1, "column": 9}],
                    }
                ],
            },
        ),
        (
            """query { nonNullStringField(param: null) }""",
            None,
            {
                "data": {"nonNullStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < String! > must not be null.",
                        "path": ["nonNullStringField"],
                        "locations": [{"line": 1, "column": 35}],
                    }
                ],
            },
        ),
        (
            """query { nonNullStringField(param: "paramDefaultValue") }""",
            None,
            {
                "data": {
                    "nonNullStringField": "SUCCESS-paramdefaultvalue-scalar-nonNullStringField"
                }
            },
        ),
        (
            """query ($param: String) { nonNullStringField(param: $param) }""",
            None,
            {
                "data": {"nonNullStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < String! > was provided the variable < $param > which was not provided a runtime value.",
                        "path": ["nonNullStringField"],
                        "locations": [{"line": 1, "column": 52}],
                    }
                ],
            },
        ),
        (
            """query ($param: String) { nonNullStringField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < String! > must not be null.",
                        "path": ["nonNullStringField"],
                        "locations": [{"line": 1, "column": 52}],
                    }
                ],
            },
        ),
        (
            """query ($param: String) { nonNullStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "nonNullStringField": "SUCCESS-varvalue-scalar-nonNullStringField"
                }
            },
        ),
        (
            """query ($param: String = null) { nonNullStringField(param: $param) }""",
            None,
            {
                "data": {"nonNullStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < String! > must not be null.",
                        "path": ["nonNullStringField"],
                        "locations": [{"line": 1, "column": 59}],
                    }
                ],
            },
        ),
        (
            """query ($param: String = null) { nonNullStringField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < String! > must not be null.",
                        "path": ["nonNullStringField"],
                        "locations": [{"line": 1, "column": 59}],
                    }
                ],
            },
        ),
        (
            """query ($param: String = null) { nonNullStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "nonNullStringField": "SUCCESS-varvalue-scalar-nonNullStringField"
                }
            },
        ),
        (
            """query ($param: String = "varDefault") { nonNullStringField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullStringField": "SUCCESS-vardefault-scalar-nonNullStringField"
                }
            },
        ),
        (
            """query ($param: String = "varDefault") { nonNullStringField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < String! > must not be null.",
                        "path": ["nonNullStringField"],
                        "locations": [{"line": 1, "column": 67}],
                    }
                ],
            },
        ),
        (
            """query ($param: String = "varDefault") { nonNullStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "nonNullStringField": "SUCCESS-varvalue-scalar-nonNullStringField"
                }
            },
        ),
        (
            """query ($param: String!) { nonNullStringField(param: $param) }""",
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
            """query ($param: String!) { nonNullStringField(param: $param) }""",
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
            """query ($param: String!) { nonNullStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "nonNullStringField": "SUCCESS-varvalue-scalar-nonNullStringField"
                }
            },
        ),
    ],
)
async def test_coercion_non_null_string_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
