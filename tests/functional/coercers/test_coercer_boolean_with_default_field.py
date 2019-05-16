import pytest

from tests.functional.coercers.common import resolve_unwrapped_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.booleanWithDefaultField": resolve_unwrapped_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { booleanWithDefaultField }""",
            None,
            {"data": {"booleanWithDefaultField": "SUCCESS-True"}},
        ),
        (
            """query { booleanWithDefaultField(param: null) }""",
            None,
            {"data": {"booleanWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query { booleanWithDefaultField(param: false) }""",
            None,
            {"data": {"booleanWithDefaultField": "SUCCESS-False"}},
        ),
        (
            """query ($param: Boolean) { booleanWithDefaultField(param: $param) }""",
            None,
            {"data": {"booleanWithDefaultField": "SUCCESS-True"}},
        ),
        (
            """query ($param: Boolean) { booleanWithDefaultField(param: $param) }""",
            {"param": None},
            {"data": {"booleanWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query ($param: Boolean) { booleanWithDefaultField(param: $param) }""",
            {"param": True},
            {"data": {"booleanWithDefaultField": "SUCCESS-True"}},
        ),
        (
            """query ($param: Boolean = null) { booleanWithDefaultField(param: $param) }""",
            None,
            {"data": {"booleanWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query ($param: Boolean = null) { booleanWithDefaultField(param: $param) }""",
            {"param": None},
            {"data": {"booleanWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query ($param: Boolean = null) { booleanWithDefaultField(param: $param) }""",
            {"param": True},
            {"data": {"booleanWithDefaultField": "SUCCESS-True"}},
        ),
        (
            """query ($param: Boolean = false) { booleanWithDefaultField(param: $param) }""",
            None,
            {"data": {"booleanWithDefaultField": "SUCCESS-False"}},
        ),
        (
            """query ($param: Boolean = false) { booleanWithDefaultField(param: $param) }""",
            {"param": None},
            {"data": {"booleanWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query ($param: Boolean = false) { booleanWithDefaultField(param: $param) }""",
            {"param": True},
            {"data": {"booleanWithDefaultField": "SUCCESS-True"}},
        ),
        (
            """query ($param: Boolean!) { booleanWithDefaultField(param: $param) }""",
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
            """query ($param: Boolean!) { booleanWithDefaultField(param: $param) }""",
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
            """query ($param: Boolean!) { booleanWithDefaultField(param: $param) }""",
            {"param": True},
            {"data": {"booleanWithDefaultField": "SUCCESS-True"}},
        ),
    ],
)
async def test_coercion_boolean_with_default_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
