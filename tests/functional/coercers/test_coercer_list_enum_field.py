import pytest


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { listEnumField }""",
            None,
            {"data": {"listEnumField": "SUCCESS"}},
        ),
        (
            """query { listEnumField(param: null) }""",
            None,
            {"data": {"listEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query { listEnumField(param: [null]) }""",
            None,
            {"data": {"listEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query { listEnumField(param: ENUM_2) }""",
            None,
            {"data": {"listEnumField": "SUCCESS-[enum_2_2-myenum]"}},
        ),
        (
            """query { listEnumField(param: [ENUM_2]) }""",
            None,
            {"data": {"listEnumField": "SUCCESS-[enum_2_2-myenum]"}},
        ),
        (
            """query { listEnumField(param: [ENUM_2, null]) }""",
            None,
            {"data": {"listEnumField": "SUCCESS-[enum_2_2-myenum-None]"}},
        ),
        (
            """query ($param: [MyEnum]) { listEnumField(param: $param) }""",
            None,
            {"data": {"listEnumField": "SUCCESS"}},
        ),
        (
            """query ($param: [MyEnum]) { listEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum]) { listEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"listEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum]) { listEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"listEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum]) { listEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"listEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum]) { listEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {"data": {"listEnumField": "SUCCESS-[enum_3_3-myenum-None]"}},
        ),
        (
            """query ($param: [MyEnum] = null) { listEnumField(param: $param) }""",
            None,
            {"data": {"listEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = null) { listEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = null) { listEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"listEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = null) { listEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"listEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = null) { listEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"listEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = null) { listEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {"data": {"listEnumField": "SUCCESS-[enum_3_3-myenum-None]"}},
        ),
        (
            """query ($param: [MyEnum] = [null]) { listEnumField(param: $param) }""",
            None,
            {"data": {"listEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [null]) { listEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [null]) { listEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"listEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [null]) { listEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"listEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = [null]) { listEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"listEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = [null]) { listEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {"data": {"listEnumField": "SUCCESS-[enum_3_3-myenum-None]"}},
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { listEnumField(param: $param) }""",
            None,
            {"data": {"listEnumField": "SUCCESS-[enum_4_4-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { listEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { listEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"listEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { listEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"listEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { listEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"listEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = ENUM_4) { listEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {"data": {"listEnumField": "SUCCESS-[enum_3_3-myenum-None]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { listEnumField(param: $param) }""",
            None,
            {"data": {"listEnumField": "SUCCESS-[enum_4_4-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { listEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { listEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"listEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { listEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"listEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { listEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"listEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4]) { listEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {"data": {"listEnumField": "SUCCESS-[enum_3_3-myenum-None]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { listEnumField(param: $param) }""",
            None,
            {"data": {"listEnumField": "SUCCESS-[enum_4_4-myenum-None]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { listEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { listEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"listEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { listEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"listEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { listEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"listEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum] = [ENUM_4, null]) { listEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {"data": {"listEnumField": "SUCCESS-[enum_3_3-myenum-None]"}},
        ),
        (
            """query ($param: [MyEnum]!) { listEnumField(param: $param) }""",
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
            """query ($param: [MyEnum]!) { listEnumField(param: $param) }""",
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
            """query ($param: [MyEnum]!) { listEnumField(param: $param) }""",
            {"param": [None]},
            {"data": {"listEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum]!) { listEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"listEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum]!) { listEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"listEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum]!) { listEnumField(param: $param) }""",
            {"param": ["ENUM_3", None]},
            {"data": {"listEnumField": "SUCCESS-[enum_3_3-myenum-None]"}},
        ),
        (
            """query ($param: [MyEnum!]) { listEnumField(param: $param) }""",
            None,
            {"data": {"listEnumField": "SUCCESS"}},
        ),
        (
            """query ($param: [MyEnum!]) { listEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum!]) { listEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]) { listEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"listEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum!]) { listEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"listEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum!]) { listEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]!) { listEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]!) { listEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]!) { listEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]!) { listEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {"data": {"listEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum!]!) { listEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {"data": {"listEnumField": "SUCCESS-[enum_3_3-myenum]"}},
        ),
        (
            """query ($param: [MyEnum!]!) { listEnumField(param: $param) }""",
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
            """query ($item: MyEnum) { listEnumField(param: [ENUM_2, $item]) }""",
            None,
            {"data": {"listEnumField": "SUCCESS-[enum_2_2-myenum-None]"}},
        ),
        (
            """query ($item: MyEnum) { listEnumField(param: [ENUM_2, $item]) }""",
            {"item": None},
            {"data": {"listEnumField": "SUCCESS-[enum_2_2-myenum-None]"}},
        ),
        (
            """query ($item: MyEnum) { listEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": {
                    "listEnumField": "SUCCESS-[enum_2_2-myenum-enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($item: MyEnum = null) { listEnumField(param: [ENUM_2, $item]) }""",
            None,
            {"data": {"listEnumField": "SUCCESS-[enum_2_2-myenum-None]"}},
        ),
        (
            """query ($item: MyEnum = null) { listEnumField(param: [ENUM_2, $item]) }""",
            {"item": None},
            {"data": {"listEnumField": "SUCCESS-[enum_2_2-myenum-None]"}},
        ),
        (
            """query ($item: MyEnum = null) { listEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": {
                    "listEnumField": "SUCCESS-[enum_2_2-myenum-enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($item: MyEnum = ENUM_4) { listEnumField(param: [ENUM_2, $item]) }""",
            None,
            {
                "data": {
                    "listEnumField": "SUCCESS-[enum_2_2-myenum-enum_4_4-myenum]"
                }
            },
        ),
        (
            """query ($item: MyEnum = ENUM_4) { listEnumField(param: [ENUM_2, $item]) }""",
            {"item": None},
            {"data": {"listEnumField": "SUCCESS-[enum_2_2-myenum-None]"}},
        ),
        (
            """query ($item: MyEnum = ENUM_4) { listEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": {
                    "listEnumField": "SUCCESS-[enum_2_2-myenum-enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($item: MyEnum!) { listEnumField(param: [ENUM_2, $item]) }""",
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
            """query ($item: MyEnum!) { listEnumField(param: [ENUM_2, $item]) }""",
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
            """query ($item: MyEnum!) { listEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": {
                    "listEnumField": "SUCCESS-[enum_2_2-myenum-enum_3_3-myenum]"
                }
            },
        ),
    ],
)
async def test_coercion_list_enum_field(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected
