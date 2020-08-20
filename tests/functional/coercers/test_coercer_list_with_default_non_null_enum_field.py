import pytest


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
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
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 49}],
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
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 57}],
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
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 29}],
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
            """query ($param: [MyEnum!] = [null]) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 29}],
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
            """query ($param: [MyEnum!] = [null]) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 29}],
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
            """query ($param: [MyEnum!] = [null]) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 29}],
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
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 37}],
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
            """query ($param: [MyEnum!] = [ENUM_4, null]) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 37}],
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
            """query ($param: [MyEnum!] = [ENUM_4, null]) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": "ENUM_3"},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 37}],
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
            """query ($param: [MyEnum!] = [ENUM_4, null]) { listWithDefaultNonNullEnumField(param: $param) }""",
            {"param": ["ENUM_3"]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 37}],
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
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 1, "column": 8},
                            {"line": 1, "column": 73},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    }
                ],
            },
        ),
        (
            """query ($item: MyEnum) { listWithDefaultNonNullEnumField(param: [ENUM_2, $item]) }""",
            {"item": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 1, "column": 8},
                            {"line": 1, "column": 73},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    }
                ],
            },
        ),
        (
            """query ($item: MyEnum) { listWithDefaultNonNullEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 1, "column": 8},
                            {"line": 1, "column": 73},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    }
                ],
            },
        ),
        (
            """query ($item: MyEnum = null) { listWithDefaultNonNullEnumField(param: [ENUM_2, $item]) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 1, "column": 8},
                            {"line": 1, "column": 80},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    }
                ],
            },
        ),
        (
            """query ($item: MyEnum = null) { listWithDefaultNonNullEnumField(param: [ENUM_2, $item]) }""",
            {"item": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 1, "column": 8},
                            {"line": 1, "column": 80},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    }
                ],
            },
        ),
        (
            """query ($item: MyEnum = null) { listWithDefaultNonNullEnumField(param: [ENUM_2, $item]) }""",
            {"item": "ENUM_3"},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $item > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 1, "column": 8},
                            {"line": 1, "column": 80},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    }
                ],
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
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected
