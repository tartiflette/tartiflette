import pytest

from tests.functional.coercers.common import resolve_list_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.listNonNullBooleanField": resolve_list_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { listNonNullBooleanField }""",
            None,
            {"data": {"listNonNullBooleanField": "SUCCESS"}},
        ),
        (
            """query { listNonNullBooleanField(param: null) }""",
            None,
            {"data": {"listNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query { listNonNullBooleanField(param: [null]) }""",
            None,
            {
                "data": {"listNonNullBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [null] >.",
                        "path": ["listNonNullBooleanField"],
                        "locations": [{"line": 1, "column": 40}],
                    }
                ],
            },
        ),
        (
            """query { listNonNullBooleanField(param: false) }""",
            None,
            {"data": {"listNonNullBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query { listNonNullBooleanField(param: [false]) }""",
            None,
            {"data": {"listNonNullBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query { listNonNullBooleanField(param: [false, null]) }""",
            None,
            {
                "data": {"listNonNullBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [false, null] >.",
                        "path": ["listNonNullBooleanField"],
                        "locations": [{"line": 1, "column": 40}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean]) { listNonNullBooleanField(param: $param) }""",
            None,
            {"data": {"listNonNullBooleanField": "SUCCESS"}},
        ),
        (
            """query ($param: [Boolean]) { listNonNullBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]) { listNonNullBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]) { listNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]) { listNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]) { listNonNullBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean] = null) { listNonNullBooleanField(param: $param) }""",
            None,
            {"data": {"listNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = null) { listNonNullBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = null) { listNonNullBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = null) { listNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = null) { listNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = null) { listNonNullBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { listNonNullBooleanField(param: $param) }""",
            None,
            {"data": {"listNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { listNonNullBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { listNonNullBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { listNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { listNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { listNonNullBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean] = false) { listNonNullBooleanField(param: $param) }""",
            None,
            {"data": {"listNonNullBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query ($param: [Boolean] = false) { listNonNullBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = false) { listNonNullBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = false) { listNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = false) { listNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = false) { listNonNullBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { listNonNullBooleanField(param: $param) }""",
            None,
            {"data": {"listNonNullBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { listNonNullBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { listNonNullBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { listNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { listNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { listNonNullBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { listNonNullBooleanField(param: $param) }""",
            None,
            {"data": {"listNonNullBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { listNonNullBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { listNonNullBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { listNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { listNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { listNonNullBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean]!) { listNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean]!) { listNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean]!) { listNonNullBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]!) { listNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]!) { listNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]!) { listNonNullBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean!]) { listNonNullBooleanField(param: $param) }""",
            None,
            {"data": {"listNonNullBooleanField": "SUCCESS"}},
        ),
        (
            """query ($param: [Boolean!]) { listNonNullBooleanField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean!]) { listNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]) { listNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]) { listNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]) { listNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { listNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { listNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { listNonNullBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { listNonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]!) { listNonNullBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"listNonNullBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]!) { listNonNullBooleanField(param: $param) }""",
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
            """query ($item: Boolean) { listNonNullBooleanField(param: [false, $item]) }""",
            None,
            {
                "data": {"listNonNullBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [false, $item] >.",
                        "path": ["listNonNullBooleanField"],
                        "locations": [{"line": 1, "column": 57}],
                    }
                ],
            },
        ),
        (
            """query ($item: Boolean) { listNonNullBooleanField(param: [false, $item]) }""",
            {"item": None},
            {"data": {"listNonNullBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($item: Boolean) { listNonNullBooleanField(param: [false, $item]) }""",
            {"item": True},
            {"data": {"listNonNullBooleanField": "SUCCESS-[False-True]"}},
        ),
        (
            """query ($item: Boolean = null) { listNonNullBooleanField(param: [false, $item]) }""",
            None,
            {"data": {"listNonNullBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($item: Boolean = null) { listNonNullBooleanField(param: [false, $item]) }""",
            {"item": None},
            {"data": {"listNonNullBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($item: Boolean = null) { listNonNullBooleanField(param: [false, $item]) }""",
            {"item": True},
            {"data": {"listNonNullBooleanField": "SUCCESS-[False-True]"}},
        ),
        (
            """query ($item: Boolean = false) { listNonNullBooleanField(param: [false, $item]) }""",
            None,
            {"data": {"listNonNullBooleanField": "SUCCESS-[False-False]"}},
        ),
        (
            """query ($item: Boolean = false) { listNonNullBooleanField(param: [false, $item]) }""",
            {"item": None},
            {"data": {"listNonNullBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($item: Boolean = false) { listNonNullBooleanField(param: [false, $item]) }""",
            {"item": True},
            {"data": {"listNonNullBooleanField": "SUCCESS-[False-True]"}},
        ),
        (
            """query ($item: Boolean!) { listNonNullBooleanField(param: [false, $item]) }""",
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
            """query ($item: Boolean!) { listNonNullBooleanField(param: [false, $item]) }""",
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
            """query ($item: Boolean!) { listNonNullBooleanField(param: [false, $item]) }""",
            {"item": True},
            {"data": {"listNonNullBooleanField": "SUCCESS-[False-True]"}},
        ),
    ],
)
async def test_coercion_list_non_null_boolean_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
