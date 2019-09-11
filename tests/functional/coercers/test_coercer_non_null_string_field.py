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
                "data": None,
                "errors": [
                    {
                        "message": "Missing mandatory argument < param > in field < Query.nonNullStringField >.",
                        "path": ["nonNullStringField"],
                        "locations": [{"line": 1, "column": 9}],
                        "extensions": {
                            "rule": "5.4.2.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Required-Arguments",
                            "tag": "required-arguments",
                        },
                    }
                ],
            },
        ),
        (
            """query { nonNullStringField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < String! > must not be null.",
                        "path": ["nonNullStringField"],
                        "locations": [{"line": 1, "column": 28}],
                        "extensions": {
                            "rule": "5.6.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Values-of-Correct-Type",
                            "tag": "values-of-correct-type",
                        },
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
        (
            """query ($param: String! = null) { nonNullStringField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid default value < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 26}],
                    }
                ],
            },
        ),
        (
            """query ($param: String! = null) { nonNullStringField(param: $param) }""",
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
            """query ($param: String! = null) { nonNullStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "nonNullStringField": "SUCCESS-varvalue-scalar-nonNullStringField"
                }
            },
        ),
        (
            """query ($param: String! = "varDefault") { nonNullStringField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullStringField": "SUCCESS-vardefault-scalar-nonNullStringField"
                }
            },
        ),
        (
            """query ($param: String! = "varDefault") { nonNullStringField(param: $param) }""",
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
            """query ($param: String! = "varDefault") { nonNullStringField(param: $param) }""",
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
