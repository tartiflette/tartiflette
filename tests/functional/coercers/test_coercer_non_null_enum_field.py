import pytest

from tests.functional.coercers.common import resolve_unwrapped_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.nonNullEnumField": resolve_unwrapped_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullEnumField }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Field < nonNullEnumField > argument < param > of type < MyEnum! > is required, but it was not provided.",
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
            """query { nonNullEnumField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 33}],
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
            """query { nonNullEnumField(param: ENUM_2) }""",
            None,
            {
                "data": {
                    "nonNullEnumField": "SUCCESS-ENUM_2_2-MyEnum-nonNullEnumField"
                }
            },
        ),
        (
            """query ($param: MyEnum!) { nonNullEnumField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < MyEnum! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum!) { nonNullEnumField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < MyEnum! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum!) { nonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "nonNullEnumField": "SUCCESS-ENUM_3_3-MyEnum-nonNullEnumField"
                }
            },
        ),
        (
            """query ($param: MyEnum! = null) { nonNullEnumField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 26}],
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
            """query ($param: MyEnum! = null) { nonNullEnumField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 26}],
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
            """query ($param: MyEnum! = null) { nonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 26}],
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
            """query ($param: MyEnum! = ENUM_4) { nonNullEnumField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullEnumField": "SUCCESS-ENUM_4_4-MyEnum-nonNullEnumField"
                }
            },
        ),
        (
            """query ($param: MyEnum! = ENUM_4) { nonNullEnumField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < MyEnum! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum! = ENUM_4) { nonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "nonNullEnumField": "SUCCESS-ENUM_3_3-MyEnum-nonNullEnumField"
                }
            },
        ),
        (
            """query ($param: MyEnum!) { nonNullEnumField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < MyEnum! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum!) { nonNullEnumField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < MyEnum! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum!) { nonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "nonNullEnumField": "SUCCESS-ENUM_3_3-MyEnum-nonNullEnumField"
                }
            },
        ),
    ],
)
async def test_coercion_non_null_enum_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
