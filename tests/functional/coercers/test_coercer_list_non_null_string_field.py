import pytest

from tests.functional.coercers.common import resolve_list_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.listNonNullStringField": resolve_list_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { listNonNullStringField }""",
            None,
            {"data": {"listNonNullStringField": "SUCCESS"}},
        ),
        (
            """query { listNonNullStringField(param: null) }""",
            None,
            {"data": {"listNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query { listNonNullStringField(param: [null]) }""",
            None,
            {
                "data": {"listNonNullStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [null] >.",
                        "path": ["listNonNullStringField"],
                        "locations": [{"line": 1, "column": 39}],
                    }
                ],
            },
        ),
        (
            """query { listNonNullStringField(param: "paramDefaultValue") }""",
            None,
            {
                "data": {
                    "listNonNullStringField": "SUCCESS-[paramdefaultvalue-scalar]"
                }
            },
        ),
        (
            """query { listNonNullStringField(param: ["paramDefaultValue"]) }""",
            None,
            {
                "data": {
                    "listNonNullStringField": "SUCCESS-[paramdefaultvalue-scalar]"
                }
            },
        ),
        (
            """query { listNonNullStringField(param: ["paramDefaultValue", null]) }""",
            None,
            {
                "data": {"listNonNullStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [paramDefaultValue, null] >.",
                        "path": ["listNonNullStringField"],
                        "locations": [{"line": 1, "column": 39}],
                    }
                ],
            },
        ),
        (
            """query ($param: [String]) { listNonNullStringField(param: $param) }""",
            None,
            {"data": {"listNonNullStringField": "SUCCESS"}},
        ),
        (
            """query ($param: [String]) { listNonNullStringField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String]) { listNonNullStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String]) { listNonNullStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"listNonNullStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String]) { listNonNullStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"listNonNullStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String]) { listNonNullStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "listNonNullStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String] = null) { listNonNullStringField(param: $param) }""",
            None,
            {"data": {"listNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = null) { listNonNullStringField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = null) { listNonNullStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = null) { listNonNullStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"listNonNullStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String] = null) { listNonNullStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"listNonNullStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String] = null) { listNonNullStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "listNonNullStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String] = [null]) { listNonNullStringField(param: $param) }""",
            None,
            {"data": {"listNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = [null]) { listNonNullStringField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = [null]) { listNonNullStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = [null]) { listNonNullStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"listNonNullStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String] = [null]) { listNonNullStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"listNonNullStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String] = [null]) { listNonNullStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "listNonNullStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String] = "varDefault") { listNonNullStringField(param: $param) }""",
            None,
            {
                "data": {
                    "listNonNullStringField": "SUCCESS-[vardefault-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = "varDefault") { listNonNullStringField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = "varDefault") { listNonNullStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = "varDefault") { listNonNullStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"listNonNullStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String] = "varDefault") { listNonNullStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"listNonNullStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String] = "varDefault") { listNonNullStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "listNonNullStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault"]) { listNonNullStringField(param: $param) }""",
            None,
            {
                "data": {
                    "listNonNullStringField": "SUCCESS-[vardefault-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault"]) { listNonNullStringField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = ["varDefault"]) { listNonNullStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = ["varDefault"]) { listNonNullStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"listNonNullStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String] = ["varDefault"]) { listNonNullStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"listNonNullStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String] = ["varDefault"]) { listNonNullStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "listNonNullStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { listNonNullStringField(param: $param) }""",
            None,
            {
                "data": {
                    "listNonNullStringField": "SUCCESS-[vardefault-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { listNonNullStringField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { listNonNullStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { listNonNullStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"listNonNullStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { listNonNullStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"listNonNullStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { listNonNullStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "listNonNullStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String]!) { listNonNullStringField(param: $param) }""",
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
            """query ($param: [String]!) { listNonNullStringField(param: $param) }""",
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
            """query ($param: [String]!) { listNonNullStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String]!) { listNonNullStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"listNonNullStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String]!) { listNonNullStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"listNonNullStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String]!) { listNonNullStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "listNonNullStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String!]) { listNonNullStringField(param: $param) }""",
            None,
            {"data": {"listNonNullStringField": "SUCCESS"}},
        ),
        (
            """query ($param: [String!]) { listNonNullStringField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String!]) { listNonNullStringField(param: $param) }""",
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
            """query ($param: [String!]) { listNonNullStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"listNonNullStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String!]) { listNonNullStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"listNonNullStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String!]) { listNonNullStringField(param: $param) }""",
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
            """query ($param: [String!]!) { listNonNullStringField(param: $param) }""",
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
            """query ($param: [String!]!) { listNonNullStringField(param: $param) }""",
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
            """query ($param: [String!]!) { listNonNullStringField(param: $param) }""",
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
            """query ($param: [String!]!) { listNonNullStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"listNonNullStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String!]!) { listNonNullStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"listNonNullStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String!]!) { listNonNullStringField(param: $param) }""",
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
            """query ($item: String) { listNonNullStringField(param: ["paramDefaultValue", $item]) }""",
            None,
            {
                "data": {"listNonNullStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [paramDefaultValue, $item] >.",
                        "path": ["listNonNullStringField"],
                        "locations": [{"line": 1, "column": 55}],
                    }
                ],
            },
        ),
        (
            """query ($item: String) { listNonNullStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": None},
            {
                "data": {"listNonNullStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [paramDefaultValue, $item] >.",
                        "path": ["listNonNullStringField"],
                        "locations": [{"line": 1, "column": 55}],
                    }
                ],
            },
        ),
        (
            """query ($item: String) { listNonNullStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": "varValue"},
            {
                "data": {
                    "listNonNullStringField": "SUCCESS-[paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
        (
            """query ($item: String = null) { listNonNullStringField(param: ["paramDefaultValue", $item]) }""",
            None,
            {
                "data": {"listNonNullStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [paramDefaultValue, $item] >.",
                        "path": ["listNonNullStringField"],
                        "locations": [{"line": 1, "column": 62}],
                    }
                ],
            },
        ),
        (
            """query ($item: String = null) { listNonNullStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": None},
            {
                "data": {"listNonNullStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [paramDefaultValue, $item] >.",
                        "path": ["listNonNullStringField"],
                        "locations": [{"line": 1, "column": 62}],
                    }
                ],
            },
        ),
        (
            """query ($item: String = null) { listNonNullStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": "varValue"},
            {
                "data": {
                    "listNonNullStringField": "SUCCESS-[paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
        (
            """query ($item: String = "varDefault") { listNonNullStringField(param: ["paramDefaultValue", $item]) }""",
            None,
            {
                "data": {
                    "listNonNullStringField": "SUCCESS-[paramdefaultvalue-scalar-vardefault-scalar]"
                }
            },
        ),
        (
            """query ($item: String = "varDefault") { listNonNullStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": None},
            {
                "data": {"listNonNullStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [paramDefaultValue, $item] >.",
                        "path": ["listNonNullStringField"],
                        "locations": [{"line": 1, "column": 70}],
                    }
                ],
            },
        ),
        (
            """query ($item: String = "varDefault") { listNonNullStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": "varValue"},
            {
                "data": {
                    "listNonNullStringField": "SUCCESS-[paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
        (
            """query ($item: String!) { listNonNullStringField(param: ["paramDefaultValue", $item]) }""",
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
            """query ($item: String!) { listNonNullStringField(param: ["paramDefaultValue", $item]) }""",
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
            """query ($item: String!) { listNonNullStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": "varValue"},
            {
                "data": {
                    "listNonNullStringField": "SUCCESS-[paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
    ],
)
async def test_coercion_list_non_null_string_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
