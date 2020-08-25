import pytest


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { listBooleanField }""",
            None,
            {"data": {"listBooleanField": "SUCCESS"}},
        ),
        (
            """query { listBooleanField(param: null) }""",
            None,
            {"data": {"listBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query { listBooleanField(param: [null]) }""",
            None,
            {"data": {"listBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query { listBooleanField(param: false) }""",
            None,
            {"data": {"listBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query { listBooleanField(param: [false]) }""",
            None,
            {"data": {"listBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query { listBooleanField(param: [false, null]) }""",
            None,
            {"data": {"listBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($param: [Boolean]) { listBooleanField(param: $param) }""",
            None,
            {"data": {"listBooleanField": "SUCCESS"}},
        ),
        (
            """query ($param: [Boolean]) { listBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]) { listBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]) { listBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]) { listBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]) { listBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"listBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean] = null) { listBooleanField(param: $param) }""",
            None,
            {"data": {"listBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = null) { listBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = null) { listBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = null) { listBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = null) { listBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = null) { listBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"listBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { listBooleanField(param: $param) }""",
            None,
            {"data": {"listBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { listBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { listBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { listBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { listBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { listBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"listBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean] = false) { listBooleanField(param: $param) }""",
            None,
            {"data": {"listBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query ($param: [Boolean] = false) { listBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = false) { listBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = false) { listBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = false) { listBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = false) { listBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"listBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { listBooleanField(param: $param) }""",
            None,
            {"data": {"listBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { listBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { listBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { listBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { listBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { listBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"listBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { listBooleanField(param: $param) }""",
            None,
            {"data": {"listBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { listBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { listBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { listBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { listBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { listBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"listBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean]!) { listBooleanField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < [Boolean]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean]!) { listBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < [Boolean]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean]!) { listBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]!) { listBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]!) { listBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]!) { listBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"listBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean!]) { listBooleanField(param: $param) }""",
            None,
            {"data": {"listBooleanField": "SUCCESS"}},
        ),
        (
            """query ($param: [Boolean!]) { listBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean!]) { listBooleanField(param: $param) }""",
            {"param": [None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [None] >; Expected non-nullable type < Boolean! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean!]) { listBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]) { listBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]) { listBooleanField(param: $param) }""",
            {"param": [True, None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [True, None] >; Expected non-nullable type < Boolean! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean!]!) { listBooleanField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < [Boolean!]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean!]!) { listBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < [Boolean!]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean!]!) { listBooleanField(param: $param) }""",
            {"param": [None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [None] >; Expected non-nullable type < Boolean! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean!]!) { listBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]!) { listBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]!) { listBooleanField(param: $param) }""",
            {"param": [True, None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [True, None] >; Expected non-nullable type < Boolean! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($item: Boolean) { listBooleanField(param: [false, $item]) }""",
            None,
            {"data": {"listBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($item: Boolean) { listBooleanField(param: [false, $item]) }""",
            {"item": None},
            {"data": {"listBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($item: Boolean) { listBooleanField(param: [false, $item]) }""",
            {"item": True},
            {"data": {"listBooleanField": "SUCCESS-[False-True]"}},
        ),
        (
            """query ($item: Boolean = null) { listBooleanField(param: [false, $item]) }""",
            None,
            {"data": {"listBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($item: Boolean = null) { listBooleanField(param: [false, $item]) }""",
            {"item": None},
            {"data": {"listBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($item: Boolean = null) { listBooleanField(param: [false, $item]) }""",
            {"item": True},
            {"data": {"listBooleanField": "SUCCESS-[False-True]"}},
        ),
        (
            """query ($item: Boolean = false) { listBooleanField(param: [false, $item]) }""",
            None,
            {"data": {"listBooleanField": "SUCCESS-[False-False]"}},
        ),
        (
            """query ($item: Boolean = false) { listBooleanField(param: [false, $item]) }""",
            {"item": None},
            {"data": {"listBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($item: Boolean = false) { listBooleanField(param: [false, $item]) }""",
            {"item": True},
            {"data": {"listBooleanField": "SUCCESS-[False-True]"}},
        ),
        (
            """query ($item: Boolean!) { listBooleanField(param: [false, $item]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of required type < Boolean! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($item: Boolean!) { listBooleanField(param: [false, $item]) }""",
            {"item": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of non-null type < Boolean! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($item: Boolean!) { listBooleanField(param: [false, $item]) }""",
            {"item": True},
            {"data": {"listBooleanField": "SUCCESS-[False-True]"}},
        ),
    ],
)
async def test_coercion_list_boolean_field(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected
