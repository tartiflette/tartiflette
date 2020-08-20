import pytest


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { listWithDefaultBooleanField }""",
            None,
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query { listWithDefaultBooleanField(param: null) }""",
            None,
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query { listWithDefaultBooleanField(param: [null]) }""",
            None,
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query { listWithDefaultBooleanField(param: false) }""",
            None,
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query { listWithDefaultBooleanField(param: [false]) }""",
            None,
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query { listWithDefaultBooleanField(param: [false, null]) }""",
            None,
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($param: [Boolean]) { listWithDefaultBooleanField(param: $param) }""",
            None,
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean]) { listWithDefaultBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]) { listWithDefaultBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]) { listWithDefaultBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]) { listWithDefaultBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]) { listWithDefaultBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean] = null) { listWithDefaultBooleanField(param: $param) }""",
            None,
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = null) { listWithDefaultBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = null) { listWithDefaultBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = null) { listWithDefaultBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = null) { listWithDefaultBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = null) { listWithDefaultBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { listWithDefaultBooleanField(param: $param) }""",
            None,
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { listWithDefaultBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { listWithDefaultBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { listWithDefaultBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { listWithDefaultBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { listWithDefaultBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean] = false) { listWithDefaultBooleanField(param: $param) }""",
            None,
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query ($param: [Boolean] = false) { listWithDefaultBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = false) { listWithDefaultBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = false) { listWithDefaultBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = false) { listWithDefaultBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = false) { listWithDefaultBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { listWithDefaultBooleanField(param: $param) }""",
            None,
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { listWithDefaultBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { listWithDefaultBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { listWithDefaultBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { listWithDefaultBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { listWithDefaultBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { listWithDefaultBooleanField(param: $param) }""",
            None,
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { listWithDefaultBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { listWithDefaultBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { listWithDefaultBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { listWithDefaultBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { listWithDefaultBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean]!) { listWithDefaultBooleanField(param: $param) }""",
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
            """query ($param: [Boolean]!) { listWithDefaultBooleanField(param: $param) }""",
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
            """query ($param: [Boolean]!) { listWithDefaultBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]!) { listWithDefaultBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]!) { listWithDefaultBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]!) { listWithDefaultBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean!]) { listWithDefaultBooleanField(param: $param) }""",
            None,
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean!]) { listWithDefaultBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean!]) { listWithDefaultBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]) { listWithDefaultBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]) { listWithDefaultBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]) { listWithDefaultBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { listWithDefaultBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { listWithDefaultBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { listWithDefaultBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { listWithDefaultBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]!) { listWithDefaultBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]!) { listWithDefaultBooleanField(param: $param) }""",
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
            """query ($item: Boolean) { listWithDefaultBooleanField(param: [false, $item]) }""",
            None,
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($item: Boolean) { listWithDefaultBooleanField(param: [false, $item]) }""",
            {"item": None},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($item: Boolean) { listWithDefaultBooleanField(param: [false, $item]) }""",
            {"item": True},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[False-True]"}},
        ),
        (
            """query ($item: Boolean = null) { listWithDefaultBooleanField(param: [false, $item]) }""",
            None,
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($item: Boolean = null) { listWithDefaultBooleanField(param: [false, $item]) }""",
            {"item": None},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($item: Boolean = null) { listWithDefaultBooleanField(param: [false, $item]) }""",
            {"item": True},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[False-True]"}},
        ),
        (
            """query ($item: Boolean = false) { listWithDefaultBooleanField(param: [false, $item]) }""",
            None,
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[False-False]"}},
        ),
        (
            """query ($item: Boolean = false) { listWithDefaultBooleanField(param: [false, $item]) }""",
            {"item": None},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($item: Boolean = false) { listWithDefaultBooleanField(param: [false, $item]) }""",
            {"item": True},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[False-True]"}},
        ),
        (
            """query ($item: Boolean!) { listWithDefaultBooleanField(param: [false, $item]) }""",
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
            """query ($item: Boolean!) { listWithDefaultBooleanField(param: [false, $item]) }""",
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
            """query ($item: Boolean!) { listWithDefaultBooleanField(param: [false, $item]) }""",
            {"item": True},
            {"data": {"listWithDefaultBooleanField": "SUCCESS-[False-True]"}},
        ),
    ],
)
async def test_coercion_list_with_default_boolean_field(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected
