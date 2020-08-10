import pytest

from tests.functional.coercers.common import resolve_unwrapped_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.nonNullFloatField": resolve_unwrapped_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullFloatField }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Field < nonNullFloatField > argument < param > of type < Float! > is required, but it was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 9}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.4.2.1",
                            "tag": "required-arguments",
                            "details": "https://spec.graphql.org/June2018/#sec-Required-Arguments",
                        },
                    }
                ],
            },
        ),
        (
            """query { nonNullFloatField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 34}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    }
                ],
            },
        ),
        (
            """query { nonNullFloatField(param: 23456.789e2) }""",
            None,
            {"data": {"nonNullFloatField": "SUCCESS-2345681.9"}},
        ),
        (
            """query ($param: Float!) { nonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"nonNullFloatField": "SUCCESS-345681.9"}},
        ),
        (
            """query ($param: Float! = null) { nonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 25}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    }
                ],
            },
        ),
        (
            """query ($param: Float! = 456.789e2) { nonNullFloatField(param: $param) }""",
            None,
            {"data": {"nonNullFloatField": "SUCCESS-45681.9"}},
        ),
        (
            """query ($param: Float! = 456.789e2) { nonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"nonNullFloatField": "SUCCESS-345681.9"}},
        ),
        (
            """query ($param: Float!) { nonNullFloatField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < Float! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float!) { nonNullFloatField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < Float! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float!) { nonNullFloatField(param: $param) }""",
            {"param": 3456.789e2},
            {"data": {"nonNullFloatField": "SUCCESS-345681.9"}},
        ),
    ],
)
async def test_coercion_non_null_float_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
