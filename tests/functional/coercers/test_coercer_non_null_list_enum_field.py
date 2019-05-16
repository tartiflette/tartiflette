import pytest

from tests.functional.coercers.common import resolve_list_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.nonNullListEnumField": resolve_list_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullListEnumField }""",
            None,
            {
                "data": {"nonNullListEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < [MyEnum]! > was not provided.",
                        "path": ["nonNullListEnumField"],
                        "locations": [{"line": 1, "column": 9}],
                    }
                ],
            },
        ),
        (
            """query { nonNullListEnumField(param: null) }""",
            None,
            {
                "data": {"nonNullListEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [MyEnum]! > must not be null.",
                        "path": ["nonNullListEnumField"],
                        "locations": [{"line": 1, "column": 37}],
                    }
                ],
            },
        ),
        (
            """query { nonNullListEnumField(param: [null]) }""",
            None,
            {"data": {"nonNullListEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query { nonNullListEnumField(param: ENUM_2) }""",
            None,
            {"data": {"nonNullListEnumField": "SUCCESS-[enum_2_2-myenum]"}},
        ),
        (
            """query { nonNullListEnumField(param: [ENUM_2]) }""",
            None,
            {"data": {"nonNullListEnumField": "SUCCESS-[enum_2_2-myenum]"}},
        ),
        (
            """query { nonNullListEnumField(param: [ENUM_2, null]) }""",
            None,
            {
                "data": {
                    "nonNullListEnumField": "SUCCESS-[enum_2_2-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum]) { nonNullListEnumField(param: $param) }""",
            None,
            {
                "data": {"nonNullListEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < [MyEnum]! > was provided the variable < $param > which was not provided a runtime value.",
                        "path": ["nonNullListEnumField"],
                        "locations": [{"line": 1, "column": 56}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum]) { nonNullListEnumField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [MyEnum]! > must not be null.",
                        "path": ["nonNullListEnumField"],
                        "locations": [{"line": 1, "column": 56}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum]) { nonNullListEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum]) { nonNullListEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"nonNullListEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum]) { nonNullListEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"nonNullListEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum]) { nonNullListEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "nonNullListEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = null) { nonNullListEnumField(param: $param) }""",
            None,
            {
                "data": {"nonNullListEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [MyEnum]! > must not be null.",
                        "path": ["nonNullListEnumField"],
                        "locations": [{"line": 1, "column": 63}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum] = null) { nonNullListEnumField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [MyEnum]! > must not be null.",
                        "path": ["nonNullListEnumField"],
                        "locations": [{"line": 1, "column": 63}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum] = null) { nonNullListEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = null) { nonNullListEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"nonNullListEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = null) { nonNullListEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"nonNullListEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = null) { nonNullListEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "nonNullListEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [null]) { nonNullListEnumField(param: $param) }""",
            None,
            {"data": {"nonNullListEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [null]) { nonNullListEnumField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [MyEnum]! > must not be null.",
                        "path": ["nonNullListEnumField"],
                        "locations": [{"line": 1, "column": 65}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum] = [null]) { nonNullListEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [null]) { nonNullListEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"nonNullListEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = [null]) { nonNullListEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"nonNullListEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = [null]) { nonNullListEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "nonNullListEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { nonNullListEnumField(param: $param) }""",
            None,
            {"data": {"nonNullListEnumField": "SUCCESS-[enum_4_4-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { nonNullListEnumField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [MyEnum]! > must not be null.",
                        "path": ["nonNullListEnumField"],
                        "locations": [{"line": 1, "column": 65}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { nonNullListEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { nonNullListEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"nonNullListEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { nonNullListEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"nonNullListEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { nonNullListEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "nonNullListEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { nonNullListEnumField(param: $param) }""",
            None,
            {"data": {"nonNullListEnumField": "SUCCESS-[enum_4_4-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { nonNullListEnumField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [MyEnum]! > must not be null.",
                        "path": ["nonNullListEnumField"],
                        "locations": [{"line": 1, "column": 67}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { nonNullListEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { nonNullListEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"nonNullListEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { nonNullListEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"nonNullListEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { nonNullListEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "nonNullListEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { nonNullListEnumField(param: $param) }""",
            None,
            {
                "data": {
                    "nonNullListEnumField": "SUCCESS-[enum_4_4-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { nonNullListEnumField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [MyEnum]! > must not be null.",
                        "path": ["nonNullListEnumField"],
                        "locations": [{"line": 1, "column": 73}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { nonNullListEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { nonNullListEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"nonNullListEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { nonNullListEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"nonNullListEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { nonNullListEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "nonNullListEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum]!) { nonNullListEnumField(param: $param) }""",
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
            """query ($param: [MyEnum]!) { nonNullListEnumField(param: $param) }""",
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
            """query ($param: [MyEnum]!) { nonNullListEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"nonNullListEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum]!) { nonNullListEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"nonNullListEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum]!) { nonNullListEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"nonNullListEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum]!) { nonNullListEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "nonNullListEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!]) { nonNullListEnumField(param: $param) }""",
            None,
            {
                "data": {"nonNullListEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < [MyEnum]! > was provided the variable < $param > which was not provided a runtime value.",
                        "path": ["nonNullListEnumField"],
                        "locations": [{"line": 1, "column": 57}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum!]) { nonNullListEnumField(param: $param) }""",
            {"param": None},
            {
                "data": {"nonNullListEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < [MyEnum]! > must not be null.",
                        "path": ["nonNullListEnumField"],
                        "locations": [{"line": 1, "column": 57}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum!]) { nonNullListEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]) { nonNullListEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"nonNullListEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum!]) { nonNullListEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"nonNullListEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum!]) { nonNullListEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]!) { nonNullListEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]!) { nonNullListEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]!) { nonNullListEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]!) { nonNullListEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"nonNullListEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum!]!) { nonNullListEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"nonNullListEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum!]!) { nonNullListEnumField(param: $param) }""",
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
            """query ($item: MyEnum) { nonNullListEnumField(param: [ENUM_2, $item]) }""",
            None,
            {
                "data": {
                    "nonNullListEnumField": "SUCCESS-[enum_2_2-myenum-None]"
                }
            },
        ),
        (
            """query ($item: MyEnum) { nonNullListEnumField(param: [ENUM_2, $item]) }""",
            {"item": None},
            {
                "data": {
                    "nonNullListEnumField": "SUCCESS-[enum_2_2-myenum-None]"
                }
            },
        ),
        (
            """query ($item: MyEnum) { nonNullListEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": {
                    "nonNullListEnumField": "SUCCESS-[enum_2_2-myenum-enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($item: MyEnum = null) { nonNullListEnumField(param: [ENUM_2, $item]) }""",
            None,
            {
                "data": {
                    "nonNullListEnumField": "SUCCESS-[enum_2_2-myenum-None]"
                }
            },
        ),
        (
            """query ($item: MyEnum = null) { nonNullListEnumField(param: [ENUM_2, $item]) }""",
            {"item": None},
            {
                "data": {
                    "nonNullListEnumField": "SUCCESS-[enum_2_2-myenum-None]"
                }
            },
        ),
        (
            """query ($item: MyEnum = null) { nonNullListEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": {
                    "nonNullListEnumField": "SUCCESS-[enum_2_2-myenum-enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($item: MyEnum = ENUM_4) { nonNullListEnumField(param: [ENUM_2, $item]) }""",
            None,
            {
                "data": {
                    "nonNullListEnumField": "SUCCESS-[enum_2_2-myenum-enum_4_4-myenum]"
                }
            },
        ),
        (
            """query ($item: MyEnum = ENUM_4) { nonNullListEnumField(param: [ENUM_2, $item]) }""",
            {"item": None},
            {
                "data": {
                    "nonNullListEnumField": "SUCCESS-[enum_2_2-myenum-None]"
                }
            },
        ),
        (
            """query ($item: MyEnum = ENUM_4) { nonNullListEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": {
                    "nonNullListEnumField": "SUCCESS-[enum_2_2-myenum-enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($item: MyEnum!) { nonNullListEnumField(param: [ENUM_2, $item]) }""",
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
            """query ($item: MyEnum!) { nonNullListEnumField(param: [ENUM_2, $item]) }""",
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
            """query ($item: MyEnum!) { nonNullListEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": {
                    "nonNullListEnumField": "SUCCESS-[enum_2_2-myenum-enum_3_3-myenum]"
                }
            },
        ),
    ],
)
async def test_coercion_non_null_list_enum_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
