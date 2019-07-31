import pytest

from tests.functional.coercers.common import resolve_list_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.listWithDefaultNonNullStringField": resolve_list_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { listWithDefaultNonNullStringField }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[defaultstring-scalar]"
                }
            },
        ),
        (
            """query { listWithDefaultNonNullStringField(param: null) }""",
            None,
            {"data": {"listWithDefaultNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query { listWithDefaultNonNullStringField(param: [null]) }""",
            None,
            {
                "data": {"listWithDefaultNonNullStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [null] >.",
                        "path": ["listWithDefaultNonNullStringField"],
                        "locations": [{"line": 1, "column": 50}],
                    }
                ],
            },
        ),
        (
            """query { listWithDefaultNonNullStringField(param: "paramDefaultValue") }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[paramdefaultvalue-scalar]"
                }
            },
        ),
        (
            """query { listWithDefaultNonNullStringField(param: ["paramDefaultValue"]) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[paramdefaultvalue-scalar]"
                }
            },
        ),
        (
            """query { listWithDefaultNonNullStringField(param: ["paramDefaultValue", null]) }""",
            None,
            {
                "data": {"listWithDefaultNonNullStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [paramDefaultValue, null] >.",
                        "path": ["listWithDefaultNonNullStringField"],
                        "locations": [{"line": 1, "column": 50}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String]) { listWithDefaultNonNullStringField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[defaultstring-scalar]"
                }
            },
        ),
        (
            """query ($param: [String]) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String]) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String]) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String]) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String]) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String] = null) { listWithDefaultNonNullStringField(param: $param) }""",
            None,
            {"data": {"listWithDefaultNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = null) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = null) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = null) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = null) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = null) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String] = [null]) { listWithDefaultNonNullStringField(param: $param) }""",
            None,
            {"data": {"listWithDefaultNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = [null]) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = [null]) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = [null]) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = [null]) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = [null]) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String] = "varDefault") { listWithDefaultNonNullStringField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[vardefault-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = "varDefault") { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = "varDefault") { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = "varDefault") { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = "varDefault") { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = "varDefault") { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault"]) { listWithDefaultNonNullStringField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[vardefault-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault"]) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = ["varDefault"]) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = ["varDefault"]) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault"]) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault"]) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { listWithDefaultNonNullStringField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[vardefault-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String]!) { listWithDefaultNonNullStringField(param: $param) }""",
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
            """query ($param: [String]!) { listWithDefaultNonNullStringField(param: $param) }""",
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
            """query ($param: [String]!) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String]!) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String]!) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String]!) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String!]) { listWithDefaultNonNullStringField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[defaultstring-scalar]"
                }
            },
        ),
        (
            """query ($param: [String!]) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String!]) { listWithDefaultNonNullStringField(param: $param) }""",
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
            """query ($param: [String!]) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String!]) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String!]) { listWithDefaultNonNullStringField(param: $param) }""",
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
            """query ($param: [String!]!) { listWithDefaultNonNullStringField(param: $param) }""",
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
            """query ($param: [String!]!) { listWithDefaultNonNullStringField(param: $param) }""",
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
            """query ($param: [String!]!) { listWithDefaultNonNullStringField(param: $param) }""",
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
            """query ($param: [String!]!) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String!]!) { listWithDefaultNonNullStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String!]!) { listWithDefaultNonNullStringField(param: $param) }""",
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
            """query ($item: String) { listWithDefaultNonNullStringField(param: ["paramDefaultValue", $item]) }""",
            None,
            {
                "data": {"listWithDefaultNonNullStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [paramDefaultValue, $item] >.",
                        "path": ["listWithDefaultNonNullStringField"],
                        "locations": [{"line": 1, "column": 66}],
                    }
                ],
            },
        ),
        (
            """query ($item: String) { listWithDefaultNonNullStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": None},
            {
                "data": {"listWithDefaultNonNullStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [paramDefaultValue, $item] >.",
                        "path": ["listWithDefaultNonNullStringField"],
                        "locations": [{"line": 1, "column": 66}],
                    }
                ],
            },
        ),
        (
            """query ($item: String) { listWithDefaultNonNullStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": "varValue"},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
        (
            """query ($item: String = null) { listWithDefaultNonNullStringField(param: ["paramDefaultValue", $item]) }""",
            None,
            {
                "data": {"listWithDefaultNonNullStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [paramDefaultValue, $item] >.",
                        "path": ["listWithDefaultNonNullStringField"],
                        "locations": [{"line": 1, "column": 73}],
                    }
                ],
            },
        ),
        (
            """query ($item: String = null) { listWithDefaultNonNullStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": None},
            {
                "data": {"listWithDefaultNonNullStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [paramDefaultValue, $item] >.",
                        "path": ["listWithDefaultNonNullStringField"],
                        "locations": [{"line": 1, "column": 73}],
                    }
                ],
            },
        ),
        (
            """query ($item: String = null) { listWithDefaultNonNullStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": "varValue"},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
        (
            """query ($item: String = "varDefault") { listWithDefaultNonNullStringField(param: ["paramDefaultValue", $item]) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[paramdefaultvalue-scalar-vardefault-scalar]"
                }
            },
        ),
        (
            """query ($item: String = "varDefault") { listWithDefaultNonNullStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": None},
            {
                "data": {"listWithDefaultNonNullStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [paramDefaultValue, $item] >.",
                        "path": ["listWithDefaultNonNullStringField"],
                        "locations": [{"line": 1, "column": 81}],
                    }
                ],
            },
        ),
        (
            """query ($item: String = "varDefault") { listWithDefaultNonNullStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": "varValue"},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
        (
            """query ($item: String!) { listWithDefaultNonNullStringField(param: ["paramDefaultValue", $item]) }""",
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
            """query ($item: String!) { listWithDefaultNonNullStringField(param: ["paramDefaultValue", $item]) }""",
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
            """query ($item: String!) { listWithDefaultNonNullStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": "varValue"},
            {
                "data": {
                    "listWithDefaultNonNullStringField": "SUCCESS-[paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
    ],
)
async def test_coercion_list_with_default_non_null_string_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
