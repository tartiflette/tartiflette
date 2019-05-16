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
                "data": {"nonNullEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < MyEnum! > was not provided.",
                        "path": ["nonNullEnumField"],
                        "locations": [{"line": 1, "column": 9}],
                    }
                ],
            },
        ),
        (
            """query { nonNullEnumField(param: null) }""",
            None,
            {
                "data": {"nonNullEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < MyEnum! > must not be null.",
                        "path": ["nonNullEnumField"],
                        "locations": [{"line": 1, "column": 33}],
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
            """query ($param: MyEnum) { nonNullEnumField(param: $param) }""",
            None,
            {
                "data": {"nonNullEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < MyEnum! > was provided the variable < $param > which was not provided a runtime value.",
                        "path": ["nonNullEnumField"],
                        "locations": [{"line": 1, "column": 50}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum) { nonNullEnumField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < MyEnum! > must not be null.",
                        "path": ["nonNullEnumField"],
                        "locations": [{"line": 1, "column": 50}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum) { nonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "nonNullEnumField": "SUCCESS-ENUM_3_3-MyEnum-nonNullEnumField"
                }
            },
        ),
        (
            """query ($param: MyEnum = null) { nonNullEnumField(param: $param) }""",
            None,
            {
                "data": {"nonNullEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < MyEnum! > must not be null.",
                        "path": ["nonNullEnumField"],
                        "locations": [{"line": 1, "column": 57}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum = null) { nonNullEnumField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < MyEnum! > must not be null.",
                        "path": ["nonNullEnumField"],
                        "locations": [{"line": 1, "column": 57}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum = null) { nonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "nonNullEnumField": "SUCCESS-ENUM_3_3-MyEnum-nonNullEnumField"
                }
            },
        ),
        (
            """query ($param: MyEnum = ENUM_4) { nonNullEnumField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullEnumField": "SUCCESS-ENUM_4_4-MyEnum-nonNullEnumField"
                }
            },
        ),
        (
            """query ($param: MyEnum = ENUM_4) { nonNullEnumField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < MyEnum! > must not be null.",
                        "path": ["nonNullEnumField"],
                        "locations": [{"line": 1, "column": 59}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum = ENUM_4) { nonNullEnumField(param: $param) }""",
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
