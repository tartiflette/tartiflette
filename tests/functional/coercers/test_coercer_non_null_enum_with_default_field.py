import pytest

from tests.functional.coercers.common import resolve_unwrapped_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.nonNullEnumWithDefaultField": resolve_unwrapped_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullEnumWithDefaultField }""",
            None,
            {
                "data": {
                    "nonNullEnumWithDefaultField": "SUCCESS-ENUM_1_1-MyEnum-nonNullEnumWithDefaultField"
                }
            },
        ),
        (
            """query { nonNullEnumWithDefaultField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < MyEnum! > must not be null.",
                        "path": ["nonNullEnumWithDefaultField"],
                        "locations": [{"line": 1, "column": 37}],
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
            """query { nonNullEnumWithDefaultField(param: ENUM_2) }""",
            None,
            {
                "data": {
                    "nonNullEnumWithDefaultField": "SUCCESS-ENUM_2_2-MyEnum-nonNullEnumWithDefaultField"
                }
            },
        ),
        (
            """query ($param: MyEnum) { nonNullEnumWithDefaultField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullEnumWithDefaultField": "SUCCESS-ENUM_1_1-MyEnum-nonNullEnumWithDefaultField"
                }
            },
        ),
        (
            """query ($param: MyEnum) { nonNullEnumWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullEnumWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < MyEnum! > must not be null.",
                        "path": ["nonNullEnumWithDefaultField"],
                        "locations": [{"line": 1, "column": 61}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum) { nonNullEnumWithDefaultField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "nonNullEnumWithDefaultField": "SUCCESS-ENUM_3_3-MyEnum-nonNullEnumWithDefaultField"
                }
            },
        ),
        (
            """query ($param: MyEnum = null) { nonNullEnumWithDefaultField(param: $param) }""",
            None,
            {
                "data": {"nonNullEnumWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < MyEnum! > must not be null.",
                        "path": ["nonNullEnumWithDefaultField"],
                        "locations": [{"line": 1, "column": 68}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum = null) { nonNullEnumWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullEnumWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < MyEnum! > must not be null.",
                        "path": ["nonNullEnumWithDefaultField"],
                        "locations": [{"line": 1, "column": 68}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum = null) { nonNullEnumWithDefaultField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "nonNullEnumWithDefaultField": "SUCCESS-ENUM_3_3-MyEnum-nonNullEnumWithDefaultField"
                }
            },
        ),
        (
            """query ($param: MyEnum = ENUM_4) { nonNullEnumWithDefaultField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullEnumWithDefaultField": "SUCCESS-ENUM_4_4-MyEnum-nonNullEnumWithDefaultField"
                }
            },
        ),
        (
            """query ($param: MyEnum = ENUM_4) { nonNullEnumWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullEnumWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < MyEnum! > must not be null.",
                        "path": ["nonNullEnumWithDefaultField"],
                        "locations": [{"line": 1, "column": 70}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum = ENUM_4) { nonNullEnumWithDefaultField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "nonNullEnumWithDefaultField": "SUCCESS-ENUM_3_3-MyEnum-nonNullEnumWithDefaultField"
                }
            },
        ),
        (
            """query ($param: MyEnum!) { nonNullEnumWithDefaultField(param: $param) }""",
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
            """query ($param: MyEnum!) { nonNullEnumWithDefaultField(param: $param) }""",
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
            """query ($param: MyEnum!) { nonNullEnumWithDefaultField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "nonNullEnumWithDefaultField": "SUCCESS-ENUM_3_3-MyEnum-nonNullEnumWithDefaultField"
                }
            },
        ),
    ],
)
async def test_coercion_non_null_enum_with_default_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
