import pytest

from tests.functional.coercers.common import resolve_unwrapped_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.nonNullIntField": resolve_unwrapped_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullIntField }""",
            None,
            {
                "data": {"nonNullIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < Int! > was not provided.",
                        "path": ["nonNullIntField"],
                        "locations": [{"line": 1, "column": 9}],
                    }
                ],
            },
        ),
        (
            """query { nonNullIntField(param: null) }""",
            None,
            {
                "data": {"nonNullIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Int! > must not be null.",
                        "path": ["nonNullIntField"],
                        "locations": [{"line": 1, "column": 32}],
                    }
                ],
            },
        ),
        (
            """query { nonNullIntField(param: 10) }""",
            None,
            {"data": {"nonNullIntField": "SUCCESS-13"}},
        ),
        (
            """query ($param: Int) { nonNullIntField(param: $param) }""",
            None,
            {
                "data": {"nonNullIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < Int! > was provided the variable < $param > which was not provided a runtime value.",
                        "path": ["nonNullIntField"],
                        "locations": [{"line": 1, "column": 46}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int) { nonNullIntField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Int! > must not be null.",
                        "path": ["nonNullIntField"],
                        "locations": [{"line": 1, "column": 46}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int) { nonNullIntField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullIntField": "SUCCESS-23"}},
        ),
        (
            """query ($param: Int = null) { nonNullIntField(param: $param) }""",
            None,
            {
                "data": {"nonNullIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Int! > must not be null.",
                        "path": ["nonNullIntField"],
                        "locations": [{"line": 1, "column": 53}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int = null) { nonNullIntField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Int! > must not be null.",
                        "path": ["nonNullIntField"],
                        "locations": [{"line": 1, "column": 53}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int = null) { nonNullIntField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullIntField": "SUCCESS-23"}},
        ),
        (
            """query ($param: Int = 30) { nonNullIntField(param: $param) }""",
            None,
            {"data": {"nonNullIntField": "SUCCESS-33"}},
        ),
        (
            """query ($param: Int = 30) { nonNullIntField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Int! > must not be null.",
                        "path": ["nonNullIntField"],
                        "locations": [{"line": 1, "column": 51}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int = 30) { nonNullIntField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullIntField": "SUCCESS-23"}},
        ),
        (
            """query ($param: Int!) { nonNullIntField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < Int! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int!) { nonNullIntField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < Int! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int!) { nonNullIntField(param: $param) }""",
            {"param": 20},
            {"data": {"nonNullIntField": "SUCCESS-23"}},
        ),
    ],
)
async def test_coercion_non_null_int_field(engine, query, variables, expected):
    assert await engine.execute(query, variables=variables) == expected
