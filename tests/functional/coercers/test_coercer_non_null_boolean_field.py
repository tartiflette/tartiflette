import pytest

from tests.functional.coercers.common import resolve_unwrapped_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.nonNullBooleanField": resolve_unwrapped_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullBooleanField }""",
            None,
            {
                "data": {"nonNullBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < Boolean! > was not provided.",
                        "path": ["nonNullBooleanField"],
                        "locations": [{"line": 1, "column": 9}],
                    }
                ],
            },
        ),
        (
            """query { nonNullBooleanField(param: null) }""",
            None,
            {
                "data": {"nonNullBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Boolean! > must not be null.",
                        "path": ["nonNullBooleanField"],
                        "locations": [{"line": 1, "column": 36}],
                    }
                ],
            },
        ),
        (
            """query { nonNullBooleanField(param: false) }""",
            None,
            {"data": {"nonNullBooleanField": "SUCCESS-False"}},
        ),
        (
            """query ($param: Boolean) { nonNullBooleanField(param: $param) }""",
            None,
            {
                "data": {"nonNullBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < Boolean! > was provided the variable < $param > which was not provided a runtime value.",
                        "path": ["nonNullBooleanField"],
                        "locations": [{"line": 1, "column": 54}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean) { nonNullBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Boolean! > must not be null.",
                        "path": ["nonNullBooleanField"],
                        "locations": [{"line": 1, "column": 54}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean) { nonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullBooleanField": "SUCCESS-True"}},
        ),
        (
            """query ($param: Boolean = null) { nonNullBooleanField(param: $param) }""",
            None,
            {
                "data": {"nonNullBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Boolean! > must not be null.",
                        "path": ["nonNullBooleanField"],
                        "locations": [{"line": 1, "column": 61}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean = null) { nonNullBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Boolean! > must not be null.",
                        "path": ["nonNullBooleanField"],
                        "locations": [{"line": 1, "column": 61}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean = null) { nonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullBooleanField": "SUCCESS-True"}},
        ),
        (
            """query ($param: Boolean = false) { nonNullBooleanField(param: $param) }""",
            None,
            {"data": {"nonNullBooleanField": "SUCCESS-False"}},
        ),
        (
            """query ($param: Boolean = false) { nonNullBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Boolean! > must not be null.",
                        "path": ["nonNullBooleanField"],
                        "locations": [{"line": 1, "column": 62}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean = false) { nonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullBooleanField": "SUCCESS-True"}},
        ),
        (
            """query ($param: Boolean!) { nonNullBooleanField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < Boolean! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean!) { nonNullBooleanField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < Boolean! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean!) { nonNullBooleanField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullBooleanField": "SUCCESS-True"}},
        ),
    ],
)
async def test_coercion_non_null_boolean_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
