import pytest

from tests.functional.coercers.common import resolve_list_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.nonNullListStringField": resolve_list_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullListStringField }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Missing mandatory argument < param > in field < Query.nonNullListStringField >.",
                        "path": ["nonNullListStringField"],
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
            """query { nonNullListStringField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [String]! > must not be null.",
                        "path": ["nonNullListStringField"],
                        "locations": [{"line": 1, "column": 32}],
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
            """query { nonNullListStringField(param: [null]) }""",
            None,
            {"data": {"nonNullListStringField": "SUCCESS-[None]"}},
        ),
        (
            """query { nonNullListStringField(param: "paramDefaultValue") }""",
            None,
            {
                "data": {
                    "nonNullListStringField": "SUCCESS-[paramdefaultvalue-scalar]"
                }
            },
        ),
        (
            """query { nonNullListStringField(param: ["paramDefaultValue"]) }""",
            None,
            {
                "data": {
                    "nonNullListStringField": "SUCCESS-[paramdefaultvalue-scalar]"
                }
            },
        ),
        (
            """query { nonNullListStringField(param: ["paramDefaultValue", null]) }""",
            None,
            {
                "data": {
                    "nonNullListStringField": "SUCCESS-[paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String]!) { nonNullListStringField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < [String]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String]!) { nonNullListStringField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < [String]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String]!) { nonNullListStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String]!) { nonNullListStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"nonNullListStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String]!) { nonNullListStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"nonNullListStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String]!) { nonNullListStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "nonNullListStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String]! = null) { nonNullListStringField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid default value < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 28}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String]! = null) { nonNullListStringField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < [String]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String]! = null) { nonNullListStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String]! = null) { nonNullListStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"nonNullListStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String]! = null) { nonNullListStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"nonNullListStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String]! = null) { nonNullListStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "nonNullListStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String]! = [null]) { nonNullListStringField(param: $param) }""",
            None,
            {"data": {"nonNullListStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String]! = [null]) { nonNullListStringField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < [String]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String]! = [null]) { nonNullListStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String]! = [null]) { nonNullListStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"nonNullListStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String]! = [null]) { nonNullListStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"nonNullListStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String]! = [null]) { nonNullListStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "nonNullListStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String]! = "varDefault") { nonNullListStringField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListStringField": "SUCCESS-[vardefault-scalar]"
                }
            },
        ),
        (
            """query ($param: [String]! = "varDefault") { nonNullListStringField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < [String]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String]! = "varDefault") { nonNullListStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String]! = "varDefault") { nonNullListStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"nonNullListStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String]! = "varDefault") { nonNullListStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"nonNullListStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String]! = "varDefault") { nonNullListStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "nonNullListStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String]! = ["varDefault"]) { nonNullListStringField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListStringField": "SUCCESS-[vardefault-scalar]"
                }
            },
        ),
        (
            """query ($param: [String]! = ["varDefault"]) { nonNullListStringField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < [String]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String]! = ["varDefault"]) { nonNullListStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String]! = ["varDefault"]) { nonNullListStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"nonNullListStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String]! = ["varDefault"]) { nonNullListStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"nonNullListStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String]! = ["varDefault"]) { nonNullListStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "nonNullListStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String]! = ["varDefault", null]) { nonNullListStringField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListStringField": "SUCCESS-[vardefault-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String]! = ["varDefault", null]) { nonNullListStringField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < [String]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String]! = ["varDefault", null]) { nonNullListStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String]! = ["varDefault", null]) { nonNullListStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"nonNullListStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String]! = ["varDefault", null]) { nonNullListStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"nonNullListStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String]! = ["varDefault", null]) { nonNullListStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "nonNullListStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String]!) { nonNullListStringField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < [String]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String]!) { nonNullListStringField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < [String]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String]!) { nonNullListStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String]!) { nonNullListStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"nonNullListStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String]!) { nonNullListStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"nonNullListStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String]!) { nonNullListStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "nonNullListStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String!]!) { nonNullListStringField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < [String!]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String!]!) { nonNullListStringField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < [String!]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String!]!) { nonNullListStringField(param: $param) }""",
            {"param": [None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [None] >; Expected non-nullable type < String! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String!]!) { nonNullListStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"nonNullListStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String!]!) { nonNullListStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"nonNullListStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String!]!) { nonNullListStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < ['varValue', None] >; Expected non-nullable type < String! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String!]!) { nonNullListStringField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < [String!]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String!]!) { nonNullListStringField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < [String!]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String!]!) { nonNullListStringField(param: $param) }""",
            {"param": [None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [None] >; Expected non-nullable type < String! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String!]!) { nonNullListStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"nonNullListStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String!]!) { nonNullListStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"nonNullListStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String!]!) { nonNullListStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < ['varValue', None] >; Expected non-nullable type < String! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($item: String) { nonNullListStringField(param: ["paramDefaultValue", $item]) }""",
            None,
            {
                "data": {
                    "nonNullListStringField": "SUCCESS-[paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($item: String) { nonNullListStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": None},
            {
                "data": {
                    "nonNullListStringField": "SUCCESS-[paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($item: String) { nonNullListStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": "varValue"},
            {
                "data": {
                    "nonNullListStringField": "SUCCESS-[paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
        (
            """query ($item: String = null) { nonNullListStringField(param: ["paramDefaultValue", $item]) }""",
            None,
            {
                "data": {
                    "nonNullListStringField": "SUCCESS-[paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($item: String = null) { nonNullListStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": None},
            {
                "data": {
                    "nonNullListStringField": "SUCCESS-[paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($item: String = null) { nonNullListStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": "varValue"},
            {
                "data": {
                    "nonNullListStringField": "SUCCESS-[paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
        (
            """query ($item: String = "varDefault") { nonNullListStringField(param: ["paramDefaultValue", $item]) }""",
            None,
            {
                "data": {
                    "nonNullListStringField": "SUCCESS-[paramdefaultvalue-scalar-vardefault-scalar]"
                }
            },
        ),
        (
            """query ($item: String = "varDefault") { nonNullListStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": None},
            {
                "data": {
                    "nonNullListStringField": "SUCCESS-[paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($item: String = "varDefault") { nonNullListStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": "varValue"},
            {
                "data": {
                    "nonNullListStringField": "SUCCESS-[paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
        (
            """query ($item: String!) { nonNullListStringField(param: ["paramDefaultValue", $item]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of required type < String! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($item: String!) { nonNullListStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of non-null type < String! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($item: String!) { nonNullListStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": "varValue"},
            {
                "data": {
                    "nonNullListStringField": "SUCCESS-[paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
    ],
)
async def test_coercion_non_null_list_string_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
