import pytest

from tests.functional.coercers.common import resolve_list_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.listWithDefaultNonNullBooleanField": resolve_list_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { listWithDefaultNonNullBooleanField }""",
            None,
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query { listWithDefaultNonNullBooleanField(param: null) }""",
            None,
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query { listWithDefaultNonNullBooleanField(param: [null]) }""",
            None,
            {
                "data": {"listWithDefaultNonNullBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [null] >.",
                        "path": ["listWithDefaultNonNullBooleanField"],
                        "locations": [{"line": 1, "column": 51}],
                    }
                ],
            },
        ),
        (
            """query { listWithDefaultNonNullBooleanField(param: false) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[False]"
                }
            },
        ),
        (
            """query { listWithDefaultNonNullBooleanField(param: [false]) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[False]"
                }
            },
        ),
        (
            """query { listWithDefaultNonNullBooleanField(param: [false, null]) }""",
            None,
            {
                "data": {"listWithDefaultNonNullBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [false, null] >.",
                        "path": ["listWithDefaultNonNullBooleanField"],
                        "locations": [{"line": 1, "column": 51}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            None,
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True, None]},
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[True-None]"
                }
            },
        ),
        (
            """query ($param: [Boolean] = null) { listWithDefaultNonNullBooleanField(param: $param) }""",
            None,
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = null) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = null) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = null) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = null) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = null) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True, None]},
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[True-None]"
                }
            },
        ),
        (
            """query ($param: [Boolean] = [null]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            None,
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True, None]},
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[True-None]"
                }
            },
        ),
        (
            """query ($param: [Boolean] = false) { listWithDefaultNonNullBooleanField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[False]"
                }
            },
        ),
        (
            """query ($param: [Boolean] = false) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = false) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = false) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = false) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = false) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True, None]},
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[True-None]"
                }
            },
        ),
        (
            """query ($param: [Boolean] = [false]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[False]"
                }
            },
        ),
        (
            """query ($param: [Boolean] = [false]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True, None]},
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[True-None]"
                }
            },
        ),
        (
            """query ($param: [Boolean] = [false, null]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[False-None]"
                }
            },
        ),
        (
            """query ($param: [Boolean] = [false, null]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True, None]},
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[True-None]"
                }
            },
        ),
        (
            """query ($param: [Boolean]!) { listWithDefaultNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean]!) { listWithDefaultNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean]!) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]!) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]!) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]!) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True, None]},
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[True-None]"
                }
            },
        ),
        (
            """query ($param: [Boolean!]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            None,
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean!]) { listWithDefaultNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]) { listWithDefaultNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { listWithDefaultNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { listWithDefaultNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { listWithDefaultNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]!) { listWithDefaultNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listWithDefaultNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]!) { listWithDefaultNonNullBooleanField(param: $param) }""",
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
            """query ($item: Boolean) { listWithDefaultNonNullBooleanField(param: [false, $item]) }""",
            None,
            {
                "data": {"listWithDefaultNonNullBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [false, $item] >.",
                        "path": ["listWithDefaultNonNullBooleanField"],
                        "locations": [{"line": 1, "column": 68}],
                    }
                ],
            },
        ),
        (
            """query ($item: Boolean) { listWithDefaultNonNullBooleanField(param: [false, $item]) }""",
            {"item": None},
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[False-None]"
                }
            },
        ),
        (
            """query ($item: Boolean) { listWithDefaultNonNullBooleanField(param: [false, $item]) }""",
            {"item": True},
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[False-True]"
                }
            },
        ),
        (
            """query ($item: Boolean = null) { listWithDefaultNonNullBooleanField(param: [false, $item]) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[False-None]"
                }
            },
        ),
        (
            """query ($item: Boolean = null) { listWithDefaultNonNullBooleanField(param: [false, $item]) }""",
            {"item": None},
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[False-None]"
                }
            },
        ),
        (
            """query ($item: Boolean = null) { listWithDefaultNonNullBooleanField(param: [false, $item]) }""",
            {"item": True},
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[False-True]"
                }
            },
        ),
        (
            """query ($item: Boolean = false) { listWithDefaultNonNullBooleanField(param: [false, $item]) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[False-False]"
                }
            },
        ),
        (
            """query ($item: Boolean = false) { listWithDefaultNonNullBooleanField(param: [false, $item]) }""",
            {"item": None},
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[False-None]"
                }
            },
        ),
        (
            """query ($item: Boolean = false) { listWithDefaultNonNullBooleanField(param: [false, $item]) }""",
            {"item": True},
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[False-True]"
                }
            },
        ),
        (
            """query ($item: Boolean!) { listWithDefaultNonNullBooleanField(param: [false, $item]) }""",
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
            """query ($item: Boolean!) { listWithDefaultNonNullBooleanField(param: [false, $item]) }""",
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
            """query ($item: Boolean!) { listWithDefaultNonNullBooleanField(param: [false, $item]) }""",
            {"item": True},
            {
                "data": {
                    "listWithDefaultNonNullBooleanField": "SUCCESS-[False-True]"
                }
            },
        ),
    ],
)
async def test_coercion_list_with_default_non_null_boolean_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
