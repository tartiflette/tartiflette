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
                "data": None,
                "errors": [
                    {
                        "message": "Field < nonNullIntField > argument < param > of type < Int! > is required, but it was not provided.",
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
            """query { nonNullIntField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 32}],
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
            """query { nonNullIntField(param: 10) }""",
            None,
            {"data": {"nonNullIntField": "SUCCESS-13"}},
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
        (
            """query ($param: Int! = null) { nonNullIntField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 23}],
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
            """query ($param: Int! = null) { nonNullIntField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 23}],
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
            """query ($param: Int! = null) { nonNullIntField(param: $param) }""",
            {"param": 20},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 23}],
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
            """query ($param: Int! = 30) { nonNullIntField(param: $param) }""",
            None,
            {"data": {"nonNullIntField": "SUCCESS-33"}},
        ),
        (
            """query ($param: Int! = 30) { nonNullIntField(param: $param) }""",
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
            """query ($param: Int! = 30) { nonNullIntField(param: $param) }""",
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
