import pytest

from tests.functional.coercers.common import resolve_list_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.nonNullListBooleanField": resolve_list_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullListBooleanField }""",
            None,
            {
                "data": {"nonNullListBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < [Boolean]! > was not provided.",
                        "path": ["nonNullListBooleanField"],
                        "locations": [{"line": 1, "column": 9}],
                    }
                ],
            },
        ),
        (
            """query { nonNullListBooleanField(param: null) }""",
            None,
            {
                "data": {"nonNullListBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Boolean]! > must not be null.",
                        "path": ["nonNullListBooleanField"],
                        "locations": [{"line": 1, "column": 40}],
                    }
                ],
            },
        ),
        (
            """query { nonNullListBooleanField(param: [null]) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query { nonNullListBooleanField(param: false) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query { nonNullListBooleanField(param: [false]) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query { nonNullListBooleanField(param: [false, null]) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($param: [Boolean]) { nonNullListBooleanField(param: $param) }""",
            None,
            {
                "data": {"nonNullListBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < [Boolean]! > was provided the variable < $param > which was not provided a runtime value.",
                        "path": ["nonNullListBooleanField"],
                        "locations": [{"line": 1, "column": 60}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean]) { nonNullListBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Boolean]! > must not be null.",
                        "path": ["nonNullListBooleanField"],
                        "locations": [{"line": 1, "column": 60}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean]) { nonNullListBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]) { nonNullListBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]) { nonNullListBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]) { nonNullListBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean] = null) { nonNullListBooleanField(param: $param) }""",
            None,
            {
                "data": {"nonNullListBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Boolean]! > must not be null.",
                        "path": ["nonNullListBooleanField"],
                        "locations": [{"line": 1, "column": 67}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean] = null) { nonNullListBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Boolean]! > must not be null.",
                        "path": ["nonNullListBooleanField"],
                        "locations": [{"line": 1, "column": 67}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean] = null) { nonNullListBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = null) { nonNullListBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = null) { nonNullListBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = null) { nonNullListBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { nonNullListBooleanField(param: $param) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { nonNullListBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Boolean]! > must not be null.",
                        "path": ["nonNullListBooleanField"],
                        "locations": [{"line": 1, "column": 69}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean] = [null]) { nonNullListBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { nonNullListBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { nonNullListBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [null]) { nonNullListBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean] = false) { nonNullListBooleanField(param: $param) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query ($param: [Boolean] = false) { nonNullListBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Boolean]! > must not be null.",
                        "path": ["nonNullListBooleanField"],
                        "locations": [{"line": 1, "column": 68}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean] = false) { nonNullListBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = false) { nonNullListBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = false) { nonNullListBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = false) { nonNullListBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { nonNullListBooleanField(param: $param) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { nonNullListBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Boolean]! > must not be null.",
                        "path": ["nonNullListBooleanField"],
                        "locations": [{"line": 1, "column": 70}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean] = [false]) { nonNullListBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { nonNullListBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { nonNullListBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [false]) { nonNullListBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { nonNullListBooleanField(param: $param) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { nonNullListBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Boolean]! > must not be null.",
                        "path": ["nonNullListBooleanField"],
                        "locations": [{"line": 1, "column": 76}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean] = [false, null]) { nonNullListBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { nonNullListBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { nonNullListBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean] = [false, null]) { nonNullListBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean]!) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean]!) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean]!) { nonNullListBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]!) { nonNullListBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]!) { nonNullListBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]!) { nonNullListBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean!]) { nonNullListBooleanField(param: $param) }""",
            None,
            {
                "data": {"nonNullListBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < [Boolean]! > was provided the variable < $param > which was not provided a runtime value.",
                        "path": ["nonNullListBooleanField"],
                        "locations": [{"line": 1, "column": 61}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean!]) { nonNullListBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Boolean]! > must not be null.",
                        "path": ["nonNullListBooleanField"],
                        "locations": [{"line": 1, "column": 61}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean!]) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]) { nonNullListBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]) { nonNullListBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean!]!) { nonNullListBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]!) { nonNullListBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean!]!) { nonNullListBooleanField(param: $param) }""",
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
            """query ($item: Boolean) { nonNullListBooleanField(param: [false, $item]) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($item: Boolean) { nonNullListBooleanField(param: [false, $item]) }""",
            {"item": None},
            {"data": {"nonNullListBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($item: Boolean) { nonNullListBooleanField(param: [false, $item]) }""",
            {"item": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[False-True]"}},
        ),
        (
            """query ($item: Boolean = null) { nonNullListBooleanField(param: [false, $item]) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($item: Boolean = null) { nonNullListBooleanField(param: [false, $item]) }""",
            {"item": None},
            {"data": {"nonNullListBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($item: Boolean = null) { nonNullListBooleanField(param: [false, $item]) }""",
            {"item": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[False-True]"}},
        ),
        (
            """query ($item: Boolean = false) { nonNullListBooleanField(param: [false, $item]) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[False-False]"}},
        ),
        (
            """query ($item: Boolean = false) { nonNullListBooleanField(param: [false, $item]) }""",
            {"item": None},
            {"data": {"nonNullListBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($item: Boolean = false) { nonNullListBooleanField(param: [false, $item]) }""",
            {"item": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[False-True]"}},
        ),
        (
            """query ($item: Boolean!) { nonNullListBooleanField(param: [false, $item]) }""",
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
            """query ($item: Boolean!) { nonNullListBooleanField(param: [false, $item]) }""",
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
            """query ($item: Boolean!) { nonNullListBooleanField(param: [false, $item]) }""",
            {"item": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[False-True]"}},
        ),
    ],
)
async def test_coercion_non_null_list_boolean_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
