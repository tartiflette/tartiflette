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
                "data": None,
                "errors": [
                    {
                        "message": "Missing mandatory argument < param > in field < Query.nonNullListBooleanField >.",
                        "path": ["nonNullListBooleanField"],
                        "locations": [{"line": 1, "column": 9}],
                        "extensions": {
                            "rule": "5.4.2.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Required-Arguments",
                            "tag": "required-arguments",
                        },
                    }
                ],
            },
        ),
        (
            """query { nonNullListBooleanField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [Boolean]! > must not be null.",
                        "path": ["nonNullListBooleanField"],
                        "locations": [{"line": 1, "column": 33}],
                        "extensions": {
                            "rule": "5.6.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Values-of-Correct-Type",
                            "tag": "values-of-correct-type",
                        },
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
            """query ($param: [Boolean]! = null) { nonNullListBooleanField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid default value < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 29}],
                    }
                ],
            },
        ),
        (
            """query ($param: [Boolean]! = null) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean]! = null) { nonNullListBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]! = null) { nonNullListBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]! = null) { nonNullListBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]! = null) { nonNullListBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean]! = [null]) { nonNullListBooleanField(param: $param) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]! = [null]) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean]! = [null]) { nonNullListBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]! = [null]) { nonNullListBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]! = [null]) { nonNullListBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]! = [null]) { nonNullListBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean]! = false) { nonNullListBooleanField(param: $param) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query ($param: [Boolean]! = false) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean]! = false) { nonNullListBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]! = false) { nonNullListBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]! = false) { nonNullListBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]! = false) { nonNullListBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean]! = [false]) { nonNullListBooleanField(param: $param) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[False]"}},
        ),
        (
            """query ($param: [Boolean]! = [false]) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean]! = [false]) { nonNullListBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]! = [false]) { nonNullListBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]! = [false]) { nonNullListBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]! = [false]) { nonNullListBooleanField(param: $param) }""",
            {"param": [True, None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True-None]"}},
        ),
        (
            """query ($param: [Boolean]! = [false, null]) { nonNullListBooleanField(param: $param) }""",
            None,
            {"data": {"nonNullListBooleanField": "SUCCESS-[False-None]"}},
        ),
        (
            """query ($param: [Boolean]! = [false, null]) { nonNullListBooleanField(param: $param) }""",
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
            """query ($param: [Boolean]! = [false, null]) { nonNullListBooleanField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [Boolean]! = [false, null]) { nonNullListBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]! = [false, null]) { nonNullListBooleanField(param: $param) }""",
            {"param": [True]},
            {"data": {"nonNullListBooleanField": "SUCCESS-[True]"}},
        ),
        (
            """query ($param: [Boolean]! = [false, null]) { nonNullListBooleanField(param: $param) }""",
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
