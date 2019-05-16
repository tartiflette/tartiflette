import pytest

from tests.functional.coercers.common import resolve_unwrapped_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.intWithDefaultField": resolve_unwrapped_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { intWithDefaultField }""",
            None,
            {"data": {"intWithDefaultField": "SUCCESS-123459"}},
        ),
        (
            """query { intWithDefaultField(param: null) }""",
            None,
            {"data": {"intWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query { intWithDefaultField(param: 10) }""",
            None,
            {"data": {"intWithDefaultField": "SUCCESS-13"}},
        ),
        (
            """query ($param: Int) { intWithDefaultField(param: $param) }""",
            None,
            {"data": {"intWithDefaultField": "SUCCESS-123459"}},
        ),
        (
            """query ($param: Int) { intWithDefaultField(param: $param) }""",
            {"param": None},
            {"data": {"intWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query ($param: Int) { intWithDefaultField(param: $param) }""",
            {"param": 20},
            {"data": {"intWithDefaultField": "SUCCESS-23"}},
        ),
        (
            """query ($param: Int = null) { intWithDefaultField(param: $param) }""",
            None,
            {"data": {"intWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query ($param: Int = null) { intWithDefaultField(param: $param) }""",
            {"param": None},
            {"data": {"intWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query ($param: Int = null) { intWithDefaultField(param: $param) }""",
            {"param": 20},
            {"data": {"intWithDefaultField": "SUCCESS-23"}},
        ),
        (
            """query ($param: Int = 30) { intWithDefaultField(param: $param) }""",
            None,
            {"data": {"intWithDefaultField": "SUCCESS-33"}},
        ),
        (
            """query ($param: Int = 30) { intWithDefaultField(param: $param) }""",
            {"param": None},
            {"data": {"intWithDefaultField": "SUCCESS-None"}},
        ),
        (
            """query ($param: Int = 30) { intWithDefaultField(param: $param) }""",
            {"param": 20},
            {"data": {"intWithDefaultField": "SUCCESS-23"}},
        ),
        (
            """query ($param: Int!) { intWithDefaultField(param: $param) }""",
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
            """query ($param: Int!) { intWithDefaultField(param: $param) }""",
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
            """query ($param: Int!) { intWithDefaultField(param: $param) }""",
            {"param": 20},
            {"data": {"intWithDefaultField": "SUCCESS-23"}},
        ),
    ],
)
async def test_coercion_int_with_default_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
