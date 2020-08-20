import pytest


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { listStringField }""",
            None,
            {"data": {"listStringField": "SUCCESS"}},
        ),
        (
            """query { listStringField(param: null) }""",
            None,
            {"data": {"listStringField": "SUCCESS-[None]"}},
        ),
        (
            """query { listStringField(param: [null]) }""",
            None,
            {"data": {"listStringField": "SUCCESS-[None]"}},
        ),
        (
            """query { listStringField(param: "paramDefaultValue") }""",
            None,
            {
                "data": {
                    "listStringField": "SUCCESS-[paramdefaultvalue-scalar]"
                }
            },
        ),
        (
            """query { listStringField(param: ["paramDefaultValue"]) }""",
            None,
            {
                "data": {
                    "listStringField": "SUCCESS-[paramdefaultvalue-scalar]"
                }
            },
        ),
        (
            """query { listStringField(param: ["paramDefaultValue", null]) }""",
            None,
            {
                "data": {
                    "listStringField": "SUCCESS-[paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: [String]) { listStringField(param: $param) }""",
            None,
            {"data": {"listStringField": "SUCCESS"}},
        ),
        (
            """query ($param: [String]) { listStringField(param: $param) }""",
            {"param": None},
            {"data": {"listStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String]) { listStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String]) { listStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"listStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String]) { listStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"listStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String]) { listStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {"data": {"listStringField": "SUCCESS-[varvalue-scalar-None]"}},
        ),
        (
            """query ($param: [String] = null) { listStringField(param: $param) }""",
            None,
            {"data": {"listStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = null) { listStringField(param: $param) }""",
            {"param": None},
            {"data": {"listStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = null) { listStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = null) { listStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"listStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String] = null) { listStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"listStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String] = null) { listStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {"data": {"listStringField": "SUCCESS-[varvalue-scalar-None]"}},
        ),
        (
            """query ($param: [String] = [null]) { listStringField(param: $param) }""",
            None,
            {"data": {"listStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = [null]) { listStringField(param: $param) }""",
            {"param": None},
            {"data": {"listStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = [null]) { listStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = [null]) { listStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"listStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String] = [null]) { listStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"listStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String] = [null]) { listStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {"data": {"listStringField": "SUCCESS-[varvalue-scalar-None]"}},
        ),
        (
            """query ($param: [String] = "varDefault") { listStringField(param: $param) }""",
            None,
            {"data": {"listStringField": "SUCCESS-[vardefault-scalar]"}},
        ),
        (
            """query ($param: [String] = "varDefault") { listStringField(param: $param) }""",
            {"param": None},
            {"data": {"listStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = "varDefault") { listStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = "varDefault") { listStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"listStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String] = "varDefault") { listStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"listStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String] = "varDefault") { listStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {"data": {"listStringField": "SUCCESS-[varvalue-scalar-None]"}},
        ),
        (
            """query ($param: [String] = ["varDefault"]) { listStringField(param: $param) }""",
            None,
            {"data": {"listStringField": "SUCCESS-[vardefault-scalar]"}},
        ),
        (
            """query ($param: [String] = ["varDefault"]) { listStringField(param: $param) }""",
            {"param": None},
            {"data": {"listStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = ["varDefault"]) { listStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = ["varDefault"]) { listStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"listStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String] = ["varDefault"]) { listStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"listStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String] = ["varDefault"]) { listStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {"data": {"listStringField": "SUCCESS-[varvalue-scalar-None]"}},
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { listStringField(param: $param) }""",
            None,
            {"data": {"listStringField": "SUCCESS-[vardefault-scalar-None]"}},
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { listStringField(param: $param) }""",
            {"param": None},
            {"data": {"listStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { listStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { listStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"listStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { listStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"listStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String] = ["varDefault", null]) { listStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {"data": {"listStringField": "SUCCESS-[varvalue-scalar-None]"}},
        ),
        (
            """query ($param: [String]!) { listStringField(param: $param) }""",
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
            """query ($param: [String]!) { listStringField(param: $param) }""",
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
            """query ($param: [String]!) { listStringField(param: $param) }""",
            {"param": [None]},
            {"data": {"listStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String]!) { listStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"listStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String]!) { listStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"listStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String]!) { listStringField(param: $param) }""",
            {"param": ["varValue", None]},
            {"data": {"listStringField": "SUCCESS-[varvalue-scalar-None]"}},
        ),
        (
            """query ($param: [String!]) { listStringField(param: $param) }""",
            None,
            {"data": {"listStringField": "SUCCESS"}},
        ),
        (
            """query ($param: [String!]) { listStringField(param: $param) }""",
            {"param": None},
            {"data": {"listStringField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [String!]) { listStringField(param: $param) }""",
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
            """query ($param: [String!]) { listStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"listStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String!]) { listStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"listStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String!]) { listStringField(param: $param) }""",
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
            """query ($param: [String!]!) { listStringField(param: $param) }""",
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
            """query ($param: [String!]!) { listStringField(param: $param) }""",
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
            """query ($param: [String!]!) { listStringField(param: $param) }""",
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
            """query ($param: [String!]!) { listStringField(param: $param) }""",
            {"param": "varValue"},
            {"data": {"listStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String!]!) { listStringField(param: $param) }""",
            {"param": ["varValue"]},
            {"data": {"listStringField": "SUCCESS-[varvalue-scalar]"}},
        ),
        (
            """query ($param: [String!]!) { listStringField(param: $param) }""",
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
            """query ($item: String) { listStringField(param: ["paramDefaultValue", $item]) }""",
            None,
            {
                "data": {
                    "listStringField": "SUCCESS-[paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($item: String) { listStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": None},
            {
                "data": {
                    "listStringField": "SUCCESS-[paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($item: String) { listStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": "varValue"},
            {
                "data": {
                    "listStringField": "SUCCESS-[paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
        (
            """query ($item: String = null) { listStringField(param: ["paramDefaultValue", $item]) }""",
            None,
            {
                "data": {
                    "listStringField": "SUCCESS-[paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($item: String = null) { listStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": None},
            {
                "data": {
                    "listStringField": "SUCCESS-[paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($item: String = null) { listStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": "varValue"},
            {
                "data": {
                    "listStringField": "SUCCESS-[paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
        (
            """query ($item: String = "varDefault") { listStringField(param: ["paramDefaultValue", $item]) }""",
            None,
            {
                "data": {
                    "listStringField": "SUCCESS-[paramdefaultvalue-scalar-vardefault-scalar]"
                }
            },
        ),
        (
            """query ($item: String = "varDefault") { listStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": None},
            {
                "data": {
                    "listStringField": "SUCCESS-[paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($item: String = "varDefault") { listStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": "varValue"},
            {
                "data": {
                    "listStringField": "SUCCESS-[paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
        (
            """query ($item: String!) { listStringField(param: ["paramDefaultValue", $item]) }""",
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
            """query ($item: String!) { listStringField(param: ["paramDefaultValue", $item]) }""",
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
            """query ($item: String!) { listStringField(param: ["paramDefaultValue", $item]) }""",
            {"item": "varValue"},
            {
                "data": {
                    "listStringField": "SUCCESS-[paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
    ],
)
async def test_coercion_list_string_field(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected
