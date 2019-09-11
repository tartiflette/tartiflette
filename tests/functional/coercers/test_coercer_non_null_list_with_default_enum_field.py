import pytest

from tests.functional.coercers.common import resolve_list_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.nonNullListWithDefaultEnumField": resolve_list_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullListWithDefaultEnumField }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_1_1-myenum-None]"
                }
            },
        ),
        (
            """query { nonNullListWithDefaultEnumField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [MyEnum]! > must not be null.",
                        "path": ["nonNullListWithDefaultEnumField"],
                        "locations": [{"line": 1, "column": 41}],
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
            """query { nonNullListWithDefaultEnumField(param: [null]) }""",
            None,
            {"data": {"nonNullListWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query { nonNullListWithDefaultEnumField(param: ENUM_2) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum]"
                }
            },
        ),
        (
            """query { nonNullListWithDefaultEnumField(param: [ENUM_2]) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum]"
                }
            },
        ),
        (
            """query { nonNullListWithDefaultEnumField(param: [ENUM_2, null]) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum]) { nonNullListWithDefaultEnumField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_1_1-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum]) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [MyEnum]! > must not be null.",
                        "path": ["nonNullListWithDefaultEnumField"],
                        "locations": [{"line": 1, "column": 67}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum]) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum]) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum]) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum]) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = null) { nonNullListWithDefaultEnumField(param: $param) }""",
            None,
            {
                "data": {"nonNullListWithDefaultEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [MyEnum]! > must not be null.",
                        "path": ["nonNullListWithDefaultEnumField"],
                        "locations": [{"line": 1, "column": 74}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum] = null) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [MyEnum]! > must not be null.",
                        "path": ["nonNullListWithDefaultEnumField"],
                        "locations": [{"line": 1, "column": 74}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum] = null) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = null) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = null) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = null) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [null]) { nonNullListWithDefaultEnumField(param: $param) }""",
            None,
            {"data": {"nonNullListWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [null]) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [MyEnum]! > must not be null.",
                        "path": ["nonNullListWithDefaultEnumField"],
                        "locations": [{"line": 1, "column": 76}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum] = [null]) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [null]) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [null]) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [null]) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { nonNullListWithDefaultEnumField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_4_4-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [MyEnum]! > must not be null.",
                        "path": ["nonNullListWithDefaultEnumField"],
                        "locations": [{"line": 1, "column": 76}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { nonNullListWithDefaultEnumField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_4_4-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [MyEnum]! > must not be null.",
                        "path": ["nonNullListWithDefaultEnumField"],
                        "locations": [{"line": 1, "column": 78}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { nonNullListWithDefaultEnumField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_4_4-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [MyEnum]! > must not be null.",
                        "path": ["nonNullListWithDefaultEnumField"],
                        "locations": [{"line": 1, "column": 84}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum]!) { nonNullListWithDefaultEnumField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < [MyEnum]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum]!) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < [MyEnum]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum]!) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum]!) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum]!) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum]!) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!]) { nonNullListWithDefaultEnumField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_1_1-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!]) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListWithDefaultEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [MyEnum]! > must not be null.",
                        "path": ["nonNullListWithDefaultEnumField"],
                        "locations": [{"line": 1, "column": 68}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum!]) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": [None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [None] >; Expected non-nullable type < MyEnum! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum!]) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!]) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!]) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < ['ENUM_3', None] >; Expected non-nullable type < MyEnum! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum!]!) { nonNullListWithDefaultEnumField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < [MyEnum!]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum!]!) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < [MyEnum!]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum!]!) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": [None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [None] >; Expected non-nullable type < MyEnum! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum!]!) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!]!) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!]!) { nonNullListWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < ['ENUM_3', None] >; Expected non-nullable type < MyEnum! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($item: MyEnum) { nonNullListWithDefaultEnumField(param: [ENUM_2, $item]) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum-None]"
                }
            },
        ),
        (
            """query ($item: MyEnum) { nonNullListWithDefaultEnumField(param: [ENUM_2, $item]) }""",
            {"item": None},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum-None]"
                }
            },
        ),
        (
            """query ($item: MyEnum) { nonNullListWithDefaultEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum-enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($item: MyEnum = null) { nonNullListWithDefaultEnumField(param: [ENUM_2, $item]) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum-None]"
                }
            },
        ),
        (
            """query ($item: MyEnum = null) { nonNullListWithDefaultEnumField(param: [ENUM_2, $item]) }""",
            {"item": None},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum-None]"
                }
            },
        ),
        (
            """query ($item: MyEnum = null) { nonNullListWithDefaultEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum-enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($item: MyEnum = ENUM_4) { nonNullListWithDefaultEnumField(param: [ENUM_2, $item]) }""",
            None,
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum-enum_4_4-myenum]"
                }
            },
        ),
        (
            """query ($item: MyEnum = ENUM_4) { nonNullListWithDefaultEnumField(param: [ENUM_2, $item]) }""",
            {"item": None},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum-None]"
                }
            },
        ),
        (
            """query ($item: MyEnum = ENUM_4) { nonNullListWithDefaultEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum-enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($item: MyEnum!) { nonNullListWithDefaultEnumField(param: [ENUM_2, $item]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of required type < MyEnum! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($item: MyEnum!) { nonNullListWithDefaultEnumField(param: [ENUM_2, $item]) }""",
            {"item": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of non-null type < MyEnum! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($item: MyEnum!) { nonNullListWithDefaultEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": {
                    "nonNullListWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum-enum_3_3-myenum]"
                }
            },
        ),
    ],
)
async def test_coercion_non_null_list_with_default_enum_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
