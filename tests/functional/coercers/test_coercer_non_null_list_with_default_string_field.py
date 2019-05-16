import pytest

from tests.functional.coercers.common import resolve_list_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.nonNullListWithDefaultStringField": resolve_list_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullListWithDefaultStringField }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[defaultstring-scalar-None]"
                }
            },
        ),
        (
            """query { nonNullListWithDefaultStringField(param: null) }""",
            None,
            {
                "data": {"nonNullListWithDefaultStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [String]! > must not be null.",
                        "path": ["nonNullListWithDefaultStringField"],
                        "locations": [{"line": 1, "column": 50}],
                    }
                ],
            },
        ),
        (
            """query { nonNullListWithDefaultStringField(param: [null]) }""",
            None,
            {"data": {"nonNullListWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query { nonNullListWithDefaultStringField(param: "paramDefaultValue") }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar]"
                }
            },
        ),
        (
            """query { nonNullListWithDefaultStringField(param: ["paramDefaultValue"]) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar]"
                }
            },
        ),
        (
            """query { nonNullListWithDefaultStringField(param: ["paramDefaultValue", null]) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String]) { nonNullListWithDefaultStringField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[defaultstring-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String]) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [String]! > must not be null.",
                        "path": ["nonNullListWithDefaultStringField"],
                        "locations": [{"line": 1, "column": 69}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String]) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String]) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String]) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String]) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String] = null) { nonNullListWithDefaultStringField(param: $param) }""",
            None,
            {
                "data": {"nonNullListWithDefaultStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [String]! > must not be null.",
                        "path": ["nonNullListWithDefaultStringField"],
                        "locations": [{"line": 1, "column": 76}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String] = null) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [String]! > must not be null.",
                        "path": ["nonNullListWithDefaultStringField"],
                        "locations": [{"line": 1, "column": 76}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String] = null) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = null) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = null) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = null) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String] = [null]) { nonNullListWithDefaultStringField(param: $param) }""",
            None,
            {"data": {"nonNullListWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = [null]) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [String]! > must not be null.",
                        "path": ["nonNullListWithDefaultStringField"],
                        "locations": [{"line": 1, "column": 78}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String] = [null]) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = [null]) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = [null]) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = [null]) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String] = "varDefault") { nonNullListWithDefaultStringField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[vardefault-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = "varDefault") { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [String]! > must not be null.",
                        "path": ["nonNullListWithDefaultStringField"],
                        "locations": [{"line": 1, "column": 84}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String] = "varDefault") { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = "varDefault") { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = "varDefault") { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = "varDefault") { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault"]) { nonNullListWithDefaultStringField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[vardefault-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault"]) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [String]! > must not be null.",
                        "path": ["nonNullListWithDefaultStringField"],
                        "locations": [{"line": 1, "column": 86}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String] = ["varDefault"]) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = ["varDefault"]) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault"]) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault"]) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { nonNullListWithDefaultStringField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[vardefault-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [String]! > must not be null.",
                        "path": ["nonNullListWithDefaultStringField"],
                        "locations": [{"line": 1, "column": 92}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String]!) { nonNullListWithDefaultStringField(param: $param) }""",
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
            """query ($param: [String]!) { nonNullListWithDefaultStringField(param: $param) }""",
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
            """query ($param: [String]!) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String]!) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String]!) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String]!) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String!]) { nonNullListWithDefaultStringField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[defaultstring-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String!]) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [String]! > must not be null.",
                        "path": ["nonNullListWithDefaultStringField"],
                        "locations": [{"line": 1, "column": 70}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String!]) { nonNullListWithDefaultStringField(param: $param) }""",
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
            """query ($param: [String!]) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String!]) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String!]) { nonNullListWithDefaultStringField(param: $param) }""",
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
            """query ($param: [String!]!) { nonNullListWithDefaultStringField(param: $param) }""",
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
            """query ($param: [String!]!) { nonNullListWithDefaultStringField(param: $param) }""",
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
            """query ($param: [String!]!) { nonNullListWithDefaultStringField(param: $param) }""",
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
            """query ($param: [String!]!) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String!]!) { nonNullListWithDefaultStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String!]!) { nonNullListWithDefaultStringField(param: $param) }""",
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
            """query ($item: String) { nonNullListWithDefaultStringField(param: ["paramDefaultValue", $item]) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($item: String) { nonNullListWithDefaultStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": None},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($item: String) { nonNullListWithDefaultStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": "varValue"},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
        (
            """query ($item: String = null) { nonNullListWithDefaultStringField(param: ["paramDefaultValue", $item]) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($item: String = null) { nonNullListWithDefaultStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": None},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($item: String = null) { nonNullListWithDefaultStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": "varValue"},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
        (
            """query ($item: String = "varDefault") { nonNullListWithDefaultStringField(param: ["paramDefaultValue", $item]) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar-vardefault-scalar]"
                }
            },
        ),
        (
            """query ($item: String = "varDefault") { nonNullListWithDefaultStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": None},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($item: String = "varDefault") { nonNullListWithDefaultStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": "varValue"},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
        (
            """query ($item: String!) { nonNullListWithDefaultStringField(param: ["paramDefaultValue", $item]) }""",
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
            """query ($item: String!) { nonNullListWithDefaultStringField(param: ["paramDefaultValue", $item]) }""",
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
            """query ($item: String!) { nonNullListWithDefaultStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": "varValue"},
            {
                "data": {
                    "nonNullListWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
    ],
)
async def test_coercion_non_null_list_with_default_string_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
