import pytest

from tests.functional.coercers.common import resolve_list_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.listWithDefaultStringField": resolve_list_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { listWithDefaultStringField }""",
            None,
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[defaultstring-scalar-None]"
                }
            },
        ),
        (
            """query { listWithDefaultStringField(param: null) }""",
            None,
            {"data": {"listWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query { listWithDefaultStringField(param: [null]) }""",
            None,
            {"data": {"listWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query { listWithDefaultStringField(param: "paramDefaultValue") }""",
            None,
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar]"
                }
            },
        ),
        (
            """query { listWithDefaultStringField(param: ["paramDefaultValue"]) }""",
            None,
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar]"
                }
            },
        ),
        (
            """query { listWithDefaultStringField(param: ["paramDefaultValue", null]) }""",
            None,
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String]) { listWithDefaultStringField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[defaultstring-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String]) { listWithDefaultStringField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String]) { listWithDefaultStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String]) { listWithDefaultStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String]) { listWithDefaultStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String]) { listWithDefaultStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String] = null) { listWithDefaultStringField(param: $param) }""",
            None,
            {"data": {"listWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = null) { listWithDefaultStringField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = null) { listWithDefaultStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = null) { listWithDefaultStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = null) { listWithDefaultStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = null) { listWithDefaultStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String] = [null]) { listWithDefaultStringField(param: $param) }""",
            None,
            {"data": {"listWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = [null]) { listWithDefaultStringField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = [null]) { listWithDefaultStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = [null]) { listWithDefaultStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = [null]) { listWithDefaultStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = [null]) { listWithDefaultStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String] = "varDefault") { listWithDefaultStringField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[vardefault-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = "varDefault") { listWithDefaultStringField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = "varDefault") { listWithDefaultStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = "varDefault") { listWithDefaultStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = "varDefault") { listWithDefaultStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = "varDefault") { listWithDefaultStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault"]) { listWithDefaultStringField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[vardefault-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault"]) { listWithDefaultStringField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = ["varDefault"]) { listWithDefaultStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = ["varDefault"]) { listWithDefaultStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault"]) { listWithDefaultStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault"]) { listWithDefaultStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { listWithDefaultStringField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[vardefault-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { listWithDefaultStringField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { listWithDefaultStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { listWithDefaultStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { listWithDefaultStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { listWithDefaultStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String]!) { listWithDefaultStringField(param: $param) }""",
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
            """query ($param: [String]!) { listWithDefaultStringField(param: $param) }""",
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
            """query ($param: [String]!) { listWithDefaultStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String]!) { listWithDefaultStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String]!) { listWithDefaultStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String]!) { listWithDefaultStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String!]) { listWithDefaultStringField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[defaultstring-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String!]) { listWithDefaultStringField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String!]) { listWithDefaultStringField(param: $param) }""",
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
            """query ($param: [String!]) { listWithDefaultStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String!]) { listWithDefaultStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String!]) { listWithDefaultStringField(param: $param) }""",
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
            """query ($param: [String!]!) { listWithDefaultStringField(param: $param) }""",
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
            """query ($param: [String!]!) { listWithDefaultStringField(param: $param) }""",
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
            """query ($param: [String!]!) { listWithDefaultStringField(param: $param) }""",
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
            """query ($param: [String!]!) { listWithDefaultStringField(param: $param) }""",
            {"param": "varValue"},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String!]!) { listWithDefaultStringField(param: $param) }""",
            {"param": ["varValue"]},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: [String!]!) { listWithDefaultStringField(param: $param) }""",
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
            """query ($item: String) { listWithDefaultStringField(param: ["paramDefaultValue", $item]) }""",
            None,
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($item: String) { listWithDefaultStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": None},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($item: String) { listWithDefaultStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": "varValue"},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
        (
            """query ($item: String = null) { listWithDefaultStringField(param: ["paramDefaultValue", $item]) }""",
            None,
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($item: String = null) { listWithDefaultStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": None},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($item: String = null) { listWithDefaultStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": "varValue"},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
        (
            """query ($item: String = "varDefault") { listWithDefaultStringField(param: ["paramDefaultValue", $item]) }""",
            None,
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar-vardefault-scalar]"
                }
            },
        ),
        (
            """query ($item: String = "varDefault") { listWithDefaultStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": None},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($item: String = "varDefault") { listWithDefaultStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": "varValue"},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
        (
            """query ($item: String!) { listWithDefaultStringField(param: ["paramDefaultValue", $item]) }""",
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
            """query ($item: String!) { listWithDefaultStringField(param: ["paramDefaultValue", $item]) }""",
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
            """query ($item: String!) { listWithDefaultStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": "varValue"},
            {
                "data": {
                    "listWithDefaultStringField": "SUCCESS-[paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
    ],
)
async def test_coercion_list_with_default_string_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
