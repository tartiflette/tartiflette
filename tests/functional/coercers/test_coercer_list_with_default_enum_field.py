import pytest

from tests.functional.coercers.common import resolve_list_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.listWithDefaultEnumField": resolve_list_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { listWithDefaultEnumField }""",
            None,
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_1_1-myenum-None]"
                }
            },
        ),
        (
            """query { listWithDefaultEnumField(param: null) }""",
            None,
            {"data": {"listWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query { listWithDefaultEnumField(param: [null]) }""",
            None,
            {"data": {"listWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query { listWithDefaultEnumField(param: ENUM_2) }""",
            None,
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum]"
                }
            },
        ),
        (
            """query { listWithDefaultEnumField(param: [ENUM_2]) }""",
            None,
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum]"
                }
            },
        ),
        (
            """query { listWithDefaultEnumField(param: [ENUM_2, null]) }""",
            None,
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum]) { listWithDefaultEnumField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_1_1-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum]) { listWithDefaultEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum]) { listWithDefaultEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum]) { listWithDefaultEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum]) { listWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum]) { listWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = null) { listWithDefaultEnumField(param: $param) }""",
            None,
            {"data": {"listWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = null) { listWithDefaultEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = null) { listWithDefaultEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = null) { listWithDefaultEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = null) { listWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = null) { listWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [null]) { listWithDefaultEnumField(param: $param) }""",
            None,
            {"data": {"listWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [null]) { listWithDefaultEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [null]) { listWithDefaultEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [null]) { listWithDefaultEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [null]) { listWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [null]) { listWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { listWithDefaultEnumField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_4_4-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { listWithDefaultEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { listWithDefaultEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { listWithDefaultEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { listWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { listWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { listWithDefaultEnumField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_4_4-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { listWithDefaultEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { listWithDefaultEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { listWithDefaultEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { listWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { listWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { listWithDefaultEnumField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_4_4-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { listWithDefaultEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { listWithDefaultEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { listWithDefaultEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { listWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { listWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum]!) { listWithDefaultEnumField(param: $param) }""",
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
            """query ($param: [MyEnum]!) { listWithDefaultEnumField(param: $param) }""",
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
            """query ($param: [MyEnum]!) { listWithDefaultEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"listWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum]!) { listWithDefaultEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum]!) { listWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum]!) { listWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!]) { listWithDefaultEnumField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_1_1-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!]) { listWithDefaultEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum!]) { listWithDefaultEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]) { listWithDefaultEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!]) { listWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!]) { listWithDefaultEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]!) { listWithDefaultEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]!) { listWithDefaultEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]!) { listWithDefaultEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]!) { listWithDefaultEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!]!) { listWithDefaultEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!]!) { listWithDefaultEnumField(param: $param) }""",
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
            """query ($item: MyEnum) { listWithDefaultEnumField(param: [ENUM_2, $item]) }""",
            None,
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum-None]"
                }
            },
        ),
        (
            """query ($item: MyEnum) { listWithDefaultEnumField(param: [ENUM_2, $item]) }""",
            {"item": None},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum-None]"
                }
            },
        ),
        (
            """query ($item: MyEnum) { listWithDefaultEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum-enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($item: MyEnum = null) { listWithDefaultEnumField(param: [ENUM_2, $item]) }""",
            None,
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum-None]"
                }
            },
        ),
        (
            """query ($item: MyEnum = null) { listWithDefaultEnumField(param: [ENUM_2, $item]) }""",
            {"item": None},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum-None]"
                }
            },
        ),
        (
            """query ($item: MyEnum = null) { listWithDefaultEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum-enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($item: MyEnum = ENUM_4) { listWithDefaultEnumField(param: [ENUM_2, $item]) }""",
            None,
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum-enum_4_4-myenum]"
                }
            },
        ),
        (
            """query ($item: MyEnum = ENUM_4) { listWithDefaultEnumField(param: [ENUM_2, $item]) }""",
            {"item": None},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum-None]"
                }
            },
        ),
        (
            """query ($item: MyEnum = ENUM_4) { listWithDefaultEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum-enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($item: MyEnum!) { listWithDefaultEnumField(param: [ENUM_2, $item]) }""",
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
            """query ($item: MyEnum!) { listWithDefaultEnumField(param: [ENUM_2, $item]) }""",
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
            """query ($item: MyEnum!) { listWithDefaultEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultEnumField": "SUCCESS-[enum_2_2-myenum-enum_3_3-myenum]"
                }
            },
        ),
    ],
)
async def test_coercion_list_with_default_enum_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
