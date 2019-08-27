import pytest

from tests.functional.coercers.common import resolve_list_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.listWithDefaultNonNullEnumField": resolve_list_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { listWithDefaultNonNullEnumField }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_1_1-myenum]"
                }
            },
        ),
        (
            """query { listWithDefaultNonNullEnumField(param: null) }""",
            None,
            {"data": {"listWithDefaultNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query { listWithDefaultNonNullEnumField(param: [null]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < MyEnum! > must not be null.",
                        "path": ["listWithDefaultNonNullEnumField"],
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
            """query { listWithDefaultNonNullEnumField(param: ENUM_2) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_2_2-myenum]"
                }
            },
        ),
        (
            """query { listWithDefaultNonNullEnumField(param: [ENUM_2]) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_2_2-myenum]"
                }
            },
        ),
        (
            """query { listWithDefaultNonNullEnumField(param: [ENUM_2, null]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < MyEnum! > must not be null.",
                        "path": ["listWithDefaultNonNullEnumField"],
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
            """query ($param: [MyEnum!]) { listWithDefaultNonNullEnumField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_1_1-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!]) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum!]) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!]) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!] = null) { listWithDefaultNonNullEnumField(param: $param) }""",
            None,
            {"data": {"listWithDefaultNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum!] = null) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum!] = null) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!] = null) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!] = [null]) { listWithDefaultNonNullEnumField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid default value < [null] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 28}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum!] = [null]) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum!] = [null]) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!] = [null]) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!] = ENUM_4) { listWithDefaultNonNullEnumField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_4_4-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!] = ENUM_4) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum!] = ENUM_4) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!] = ENUM_4) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!] = [ENUM_4]) { listWithDefaultNonNullEnumField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_4_4-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!] = [ENUM_4]) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum!] = [ENUM_4]) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!] = [ENUM_4]) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!] = [ENUM_4, null]) { listWithDefaultNonNullEnumField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid default value < [ENUM_4, null] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 28}],
                    }
                ],
            },
        ),
        (
            """query ($param: [MyEnum!] = [ENUM_4, null]) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum!] = [ENUM_4, null]) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!] = [ENUM_4, null]) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!]!) { listWithDefaultNonNullEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]!) { listWithDefaultNonNullEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]!) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!]!) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!]) { listWithDefaultNonNullEnumField(param: $param) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_1_1-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!]) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": None},
            {"data": {"listWithDefaultNonNullEnumField": "SUCCESS-[None]"}},
        ),
        (
            """query ($param: [MyEnum!]) { listWithDefaultNonNullEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!]) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!]) { listWithDefaultNonNullEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]!) { listWithDefaultNonNullEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]!) { listWithDefaultNonNullEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]!) { listWithDefaultNonNullEnumField(param: $param) }""",
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
            """query ($param: [MyEnum!]!) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!]!) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($param: [MyEnum!]!) { listWithDefaultNonNullEnumField(param: $param) }""",
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
            """query ($item: MyEnum) { listWithDefaultNonNullEnumField(param: [ENUM_2, $item]) }""",
            None,
            {
                "data": {"listWithDefaultNonNullEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [ENUM_2, $item] >.",
                        "path": ["listWithDefaultNonNullEnumField"],
                        "locations": [{"line": 1, "column": 64}],
                    }
                ],
            },
        ),
        (
            """query ($item: MyEnum) { listWithDefaultNonNullEnumField(param: [ENUM_2, $item]) }""",
            {"item": None},
            {
                "data": {"listWithDefaultNonNullEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [ENUM_2, $item] >.",
                        "path": ["listWithDefaultNonNullEnumField"],
                        "locations": [{"line": 1, "column": 64}],
                    }
                ],
            },
        ),
        (
            """query ($item: MyEnum) { listWithDefaultNonNullEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_2_2-myenum-enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($item: MyEnum = null) { listWithDefaultNonNullEnumField(param: [ENUM_2, $item]) }""",
            None,
            {
                "data": {"listWithDefaultNonNullEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [ENUM_2, $item] >.",
                        "path": ["listWithDefaultNonNullEnumField"],
                        "locations": [{"line": 1, "column": 71}],
                    }
                ],
            },
        ),
        (
            """query ($item: MyEnum = null) { listWithDefaultNonNullEnumField(param: [ENUM_2, $item]) }""",
            {"item": None},
            {
                "data": {"listWithDefaultNonNullEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [ENUM_2, $item] >.",
                        "path": ["listWithDefaultNonNullEnumField"],
                        "locations": [{"line": 1, "column": 71}],
                    }
                ],
            },
        ),
        (
            """query ($item: MyEnum = null) { listWithDefaultNonNullEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_2_2-myenum-enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($item: MyEnum = ENUM_4) { listWithDefaultNonNullEnumField(param: [ENUM_2, $item]) }""",
            None,
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_2_2-myenum-enum_4_4-myenum]"
                }
            },
        ),
        (
            """query ($item: MyEnum = ENUM_4) { listWithDefaultNonNullEnumField(param: [ENUM_2, $item]) }""",
            {"item": None},
            {
                "data": {"listWithDefaultNonNullEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < [ENUM_2, $item] >.",
                        "path": ["listWithDefaultNonNullEnumField"],
                        "locations": [{"line": 1, "column": 73}],
                    }
                ],
            },
        ),
        (
            """query ($item: MyEnum = ENUM_4) { listWithDefaultNonNullEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_2_2-myenum-enum_3_3-myenum]"
                }
            },
        ),
        (
            """query ($item: MyEnum!) { listWithDefaultNonNullEnumField(param: [ENUM_2, $item]) }""",
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
            """query ($item: MyEnum!) { listWithDefaultNonNullEnumField(param: [ENUM_2, $item]) }""",
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
            """query ($item: MyEnum!) { listWithDefaultNonNullEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": {
                    "listWithDefaultNonNullEnumField": "SUCCESS-[enum_2_2-myenum-enum_3_3-myenum]"
                }
            },
        ),
    ],
)
async def test_coercion_list_with_default_non_null_enum_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
