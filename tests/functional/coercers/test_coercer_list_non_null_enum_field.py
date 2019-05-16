import pytest

from tests.functional.coercers.common import resolve_list_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.listNonNullEnumField": resolve_list_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { listNonNullEnumField }""",
            None,
            {"data": {"listNonNullEnumField": "SUCCESS"}},
        ),
        (
            """query { listNonNullEnumField(param: null) }""",
            None,
            {"data": {"listNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query { listNonNullEnumField(param: [null]) }""",
            None,
            {
                "data": {"listNonNullEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [null] >.",
                        "path": ["listNonNullEnumField"],
                        "locations": [{"line": 1, "column": 37}],
                    }
                ],
            },
        ),
        (
            """query { listNonNullEnumField(param: ENUM_2) }""",
            None,
            {"data": {"listNonNullEnumField": "SUCCESS-[enum_2_2-myenum]"}},
        ),
        (
            """query { listNonNullEnumField(param: [ENUM_2]) }""",
            None,
            {"data": {"listNonNullEnumField": "SUCCESS-[enum_2_2-myenum]"}},
        ),
        (
            """query { listNonNullEnumField(param: [ENUM_2, null]) }""",
            None,
            {
                "data": {"listNonNullEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [ENUM_2, null] >.",
                        "path": ["listNonNullEnumField"],
                        "locations": [{"line": 1, "column": 37}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum]) { listNonNullEnumField(param: $param) }""",
            None,
            {"data": {"listNonNullEnumField": "SUCCESS"}},
        ),
        (
            """query ($param: [MyEnum]) { listNonNullEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum]) { listNonNullEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum]) { listNonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"listNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum]) { listNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"listNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum]) { listNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "listNonNullEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = null) { listNonNullEnumField(param: $param) }""",
            None,
            {"data": {"listNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = null) { listNonNullEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = null) { listNonNullEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = null) { listNonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"listNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = null) { listNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"listNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = null) { listNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "listNonNullEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [null]) { listNonNullEnumField(param: $param) }""",
            None,
            {"data": {"listNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [null]) { listNonNullEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [null]) { listNonNullEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [null]) { listNonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"listNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = [null]) { listNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"listNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = [null]) { listNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "listNonNullEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { listNonNullEnumField(param: $param) }""",
            None,
            {"data": {"listNonNullEnumField": "SUCCESS-[enum_4_4-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { listNonNullEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { listNonNullEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { listNonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"listNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { listNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"listNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { listNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "listNonNullEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { listNonNullEnumField(param: $param) }""",
            None,
            {"data": {"listNonNullEnumField": "SUCCESS-[enum_4_4-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { listNonNullEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { listNonNullEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { listNonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"listNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { listNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"listNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { listNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "listNonNullEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { listNonNullEnumField(param: $param) }""",
            None,
            {
                "data": {
                    "listNonNullEnumField": "SUCCESS-[enum_4_4-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { listNonNullEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { listNonNullEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { listNonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"listNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { listNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"listNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { listNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "listNonNullEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum]!) { listNonNullEnumField(param: $param) }""",
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
            """query ($param: [MyEnum]!) { listNonNullEnumField(param: $param) }""",
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
            """query ($param: [MyEnum]!) { listNonNullEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"listNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum]!) { listNonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"listNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum]!) { listNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"listNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum]!) { listNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {
                "data": {
                    "listNonNullEnumField": "SUCCESS-[enum_3_3-myenum-None]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!]) { listNonNullEnumField(param: $param) }""",
            None,
            {"data": {"listNonNullEnumField": "SUCCESS"}},
        ),
        (
            """query ($param: [MyEnum!]) { listNonNullEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum!]) { listNonNullEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]) { listNonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"listNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum!]) { listNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"listNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum!]) { listNonNullEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]!) { listNonNullEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]!) { listNonNullEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]!) { listNonNullEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]!) { listNonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"listNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum!]!) { listNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"listNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum!]!) { listNonNullEnumField(param: $param) }""",
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
            """query ($item: MyEnum) { listNonNullEnumField(param: [ENUM_2, $item]) }""",
            None,
            {
                "data": {"listNonNullEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [ENUM_2, $item] >.",
                        "path": ["listNonNullEnumField"],
                        "locations": [{"line": 1, "column": 53}],
                    }
                ],
            },
        ),
        (
            """query ($item: MyEnum) { listNonNullEnumField(param: [ENUM_2, $item]) }""",
            {"item": None},
            {
                "data": {
                    "listNonNullEnumField": "SUCCESS-[enum_2_2-myenum-None]"
                }
            },
        ),
        (
            """query ($item: MyEnum) { listNonNullEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": {
                    "listNonNullEnumField": "SUCCESS-[enum_2_2-myenum-enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($item: MyEnum = null) { listNonNullEnumField(param: [ENUM_2, $item]) }""",
            None,
            {
                "data": {
                    "listNonNullEnumField": "SUCCESS-[enum_2_2-myenum-None]"
                }
            },
        ),
        (
            """query ($item: MyEnum = null) { listNonNullEnumField(param: [ENUM_2, $item]) }""",
            {"item": None},
            {
                "data": {
                    "listNonNullEnumField": "SUCCESS-[enum_2_2-myenum-None]"
                }
            },
        ),
        (
            """query ($item: MyEnum = null) { listNonNullEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": {
                    "listNonNullEnumField": "SUCCESS-[enum_2_2-myenum-enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($item: MyEnum = ENUM_4) { listNonNullEnumField(param: [ENUM_2, $item]) }""",
            None,
            {
                "data": {
                    "listNonNullEnumField": "SUCCESS-[enum_2_2-myenum-enum_4_4-myenum]"
                }
            },
        ),
        (
            """query ($item: MyEnum = ENUM_4) { listNonNullEnumField(param: [ENUM_2, $item]) }""",
            {"item": None},
            {
                "data": {
                    "listNonNullEnumField": "SUCCESS-[enum_2_2-myenum-None]"
                }
            },
        ),
        (
            """query ($item: MyEnum = ENUM_4) { listNonNullEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": {
                    "listNonNullEnumField": "SUCCESS-[enum_2_2-myenum-enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($item: MyEnum!) { listNonNullEnumField(param: [ENUM_2, $item]) }""",
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
            """query ($item: MyEnum!) { listNonNullEnumField(param: [ENUM_2, $item]) }""",
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
            """query ($item: MyEnum!) { listNonNullEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": {
                    "listNonNullEnumField": "SUCCESS-[enum_2_2-myenum-enum_3_3-myenum]"
                }
            },
        ),
    ],
)
async def test_coercion_list_non_null_enum_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
