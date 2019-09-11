import pytest

from tests.functional.coercers.common import resolve_unwrapped_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={
        "Query.nonNullBooleanWithDefaultField": resolve_unwrapped_field
    },
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullBooleanWithDefaultField }""",
            None,
            {"data": {"nonNullBooleanWithDefaultField": "SUCCESS-True"}},
        ),
        (
            """query { nonNullBooleanWithDefaultField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Boolean! > must not be null.",
                        "path": ["nonNullBooleanWithDefaultField"],
                        "locations": [{"line": 1, "column": 40}],
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
            """query { nonNullBooleanWithDefaultField(param: false) }""",
            None,
            {"data": {"nonNullBooleanWithDefaultField": "SUCCESS-False"}},
        ),
        (
            """query ($param: Boolean) { nonNullBooleanWithDefaultField(param: $param) }""",
            None,
            {"data": {"nonNullBooleanWithDefaultField": "SUCCESS-True"}},
        ),
        (
            """query ($param: Boolean) { nonNullBooleanWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullBooleanWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Boolean! > must not be null.",
                        "path": ["nonNullBooleanWithDefaultField"],
                        "locations": [{"line": 1, "column": 65}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean) { nonNullBooleanWithDefaultField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullBooleanWithDefaultField": "SUCCESS-True"}},
        ),
        (
            """query ($param: Boolean = null) { nonNullBooleanWithDefaultField(param: $param) }""",
            None,
            {
                "data": {"nonNullBooleanWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Boolean! > must not be null.",
                        "path": ["nonNullBooleanWithDefaultField"],
                        "locations": [{"line": 1, "column": 72}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean = null) { nonNullBooleanWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullBooleanWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Boolean! > must not be null.",
                        "path": ["nonNullBooleanWithDefaultField"],
                        "locations": [{"line": 1, "column": 72}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean = null) { nonNullBooleanWithDefaultField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullBooleanWithDefaultField": "SUCCESS-True"}},
        ),
        (
            """query ($param: Boolean = false) { nonNullBooleanWithDefaultField(param: $param) }""",
            None,
            {"data": {"nonNullBooleanWithDefaultField": "SUCCESS-False"}},
        ),
        (
            """query ($param: Boolean = false) { nonNullBooleanWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullBooleanWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Boolean! > must not be null.",
                        "path": ["nonNullBooleanWithDefaultField"],
                        "locations": [{"line": 1, "column": 73}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean = false) { nonNullBooleanWithDefaultField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullBooleanWithDefaultField": "SUCCESS-True"}},
        ),
        (
            """query ($param: Boolean!) { nonNullBooleanWithDefaultField(param: $param) }""",
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
            """query ($param: Boolean!) { nonNullBooleanWithDefaultField(param: $param) }""",
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
            """query ($param: Boolean!) { nonNullBooleanWithDefaultField(param: $param) }""",
            {"param": True},
            {"data": {"nonNullBooleanWithDefaultField": "SUCCESS-True"}},
        ),
    ],
)
async def test_coercion_non_null_boolean_with_default_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
