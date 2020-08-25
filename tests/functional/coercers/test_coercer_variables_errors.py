import pytest

from tartiflette import Directive, Scalar
from tartiflette.scalar.builtins.string import ScalarString
from tartiflette.types.exceptions.tartiflette import CoercionError


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query ($param: Boolean!) { booleanField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < Boolean! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean!) { booleanField(param: $param) }""",
            {},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < Boolean! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean!) { booleanField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < Boolean! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean) { booleanField(param: $param) }""",
            {"param": "ENUM_1"},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < ENUM_1 >; Expected type < Boolean >; Boolean cannot represent a non boolean value: < ENUM_1 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean) { booleanField(param: $param) }""",
            {"param": 23456.789e2},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < 2345678.9 >; Expected type < Boolean >; Boolean cannot represent a non boolean value: < 2345678.9 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean) { booleanField(param: $param) }""",
            {"param": 10},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < 10 >; Expected type < Boolean >; Boolean cannot represent a non boolean value: < 10 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean) { booleanField(param: $param) }""",
            {"param": "paramValue"},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < paramValue >; Expected type < Boolean >; Boolean cannot represent a non boolean value: < paramValue >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean) { booleanField(param: $param) }""",
            {"param": [None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [None] >; Expected type < Boolean >; Boolean cannot represent a non boolean value: < [None] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean) { booleanField(param: $param) }""",
            {"param": [True]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [True] >; Expected type < Boolean >; Boolean cannot represent a non boolean value: < [True] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean) { booleanField(param: $param) }""",
            {"param": ["ENUM_1"]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < ['ENUM_1'] >; Expected type < Boolean >; Boolean cannot represent a non boolean value: < ['ENUM_1'] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean) { booleanField(param: $param) }""",
            {"param": [23456.789e2]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [2345678.9] >; Expected type < Boolean >; Boolean cannot represent a non boolean value: < [2345678.9] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean) { booleanField(param: $param) }""",
            {"param": [10]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [10] >; Expected type < Boolean >; Boolean cannot represent a non boolean value: < [10] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean) { booleanField(param: $param) }""",
            {"param": ["paramValue"]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < ['paramValue'] >; Expected type < Boolean >; Boolean cannot represent a non boolean value: < ['paramValue'] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean) { booleanField(param: $param) }""",
            {"param": {}},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < {} >; Expected type < Boolean >; Boolean cannot represent a non boolean value: < {} >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
    ],
)
async def test_coercion_boolean_field_variables_errors(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query ($param: MyEnum!) { enumField(param: $param) }""",
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
            """query ($param: MyEnum!) { enumField(param: $param) }""",
            {},
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
            """query ($param: MyEnum!) { enumField(param: $param) }""",
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
            """query ($param: MyEnum) { enumField(param: $param) }""",
            {"param": True},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < True >; Expected type < MyEnum >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum) { enumField(param: $param) }""",
            {"param": 23456.789e2},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < 2345678.9 >; Expected type < MyEnum >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum) { enumField(param: $param) }""",
            {"param": 10},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < 10 >; Expected type < MyEnum >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum) { enumField(param: $param) }""",
            {"param": "paramValue"},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < paramValue >; Expected type < MyEnum >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum) { enumField(param: $param) }""",
            {"param": [None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [None] >; Expected type < MyEnum >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum) { enumField(param: $param) }""",
            {"param": [True]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [True] >; Expected type < MyEnum >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum) { enumField(param: $param) }""",
            {"param": ["ENUM_1"]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < ['ENUM_1'] >; Expected type < MyEnum >; Did you mean ENUM_1, ENUM_4, ENUM_3, or ENUM_2?",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum) { enumField(param: $param) }""",
            {"param": [23456.789e2]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [2345678.9] >; Expected type < MyEnum >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum) { enumField(param: $param) }""",
            {"param": [10]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [10] >; Expected type < MyEnum >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum) { enumField(param: $param) }""",
            {"param": ["paramValue"]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < ['paramValue'] >; Expected type < MyEnum >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum) { enumField(param: $param) }""",
            {"param": {}},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < {} >; Expected type < MyEnum >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
    ],
)
async def test_coercion_enum_field_variables_errors(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query ($param: Float!) { floatField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < Float! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float!) { floatField(param: $param) }""",
            {},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < Float! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float!) { floatField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < Float! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float) { floatField(param: $param) }""",
            {"param": True},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < True >; Expected type < Float >; Float cannot represent non numeric value: < True >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float) { floatField(param: $param) }""",
            {"param": "ENUM_1"},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < ENUM_1 >; Expected type < Float >; Float cannot represent non numeric value: < ENUM_1 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float) { floatField(param: $param) }""",
            {"param": "paramValue"},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < paramValue >; Expected type < Float >; Float cannot represent non numeric value: < paramValue >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float) { floatField(param: $param) }""",
            {"param": [None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [None] >; Expected type < Float >; Float cannot represent non numeric value: < [None] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float) { floatField(param: $param) }""",
            {"param": [True]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [True] >; Expected type < Float >; Float cannot represent non numeric value: < [True] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float) { floatField(param: $param) }""",
            {"param": ["ENUM_1"]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < ['ENUM_1'] >; Expected type < Float >; Float cannot represent non numeric value: < ['ENUM_1'] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float) { floatField(param: $param) }""",
            {"param": [23456.789e2]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [2345678.9] >; Expected type < Float >; Float cannot represent non numeric value: < [2345678.9] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float) { floatField(param: $param) }""",
            {"param": [10]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [10] >; Expected type < Float >; Float cannot represent non numeric value: < [10] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float) { floatField(param: $param) }""",
            {"param": ["paramValue"]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < ['paramValue'] >; Expected type < Float >; Float cannot represent non numeric value: < ['paramValue'] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float) { floatField(param: $param) }""",
            {"param": {}},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < {} >; Expected type < Float >; Float cannot represent non numeric value: < {} >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
    ],
)
async def test_coercion_float_field_variables_errors(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query ($param: Int!) { intField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < Int! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int!) { intField(param: $param) }""",
            {},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < Int! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int!) { intField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < Int! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int) { intField(param: $param) }""",
            {"param": True},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < True >; Expected type < Int >; Int cannot represent non-integer value: < True >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int) { intField(param: $param) }""",
            {"param": "ENUM_1"},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < ENUM_1 >; Expected type < Int >; Int cannot represent non-integer value: < ENUM_1 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int) { intField(param: $param) }""",
            {"param": 23456.789e2},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < 2345678.9 >; Expected type < Int >; Int cannot represent non-integer value: < 2345678.9 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int) { intField(param: $param) }""",
            {"param": "paramValue"},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < paramValue >; Expected type < Int >; Int cannot represent non-integer value: < paramValue >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int) { intField(param: $param) }""",
            {"param": [None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [None] >; Expected type < Int >; Int cannot represent non-integer value: < [None] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int) { intField(param: $param) }""",
            {"param": [True]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [True] >; Expected type < Int >; Int cannot represent non-integer value: < [True] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int) { intField(param: $param) }""",
            {"param": ["ENUM_1"]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < ['ENUM_1'] >; Expected type < Int >; Int cannot represent non-integer value: < ['ENUM_1'] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int) { intField(param: $param) }""",
            {"param": [23456.789e2]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [2345678.9] >; Expected type < Int >; Int cannot represent non-integer value: < [2345678.9] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int) { intField(param: $param) }""",
            {"param": [10]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [10] >; Expected type < Int >; Int cannot represent non-integer value: < [10] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int) { intField(param: $param) }""",
            {"param": ["paramValue"]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < ['paramValue'] >; Expected type < Int >; Int cannot represent non-integer value: < ['paramValue'] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int) { intField(param: $param) }""",
            {"param": {}},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < {} >; Expected type < Int >; Int cannot represent non-integer value: < {} >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
    ],
)
async def test_coercion_int_field_variables_errors(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query ($param: String!) { stringField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < String! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: String!) { stringField(param: $param) }""",
            {},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < String! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: String!) { stringField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < String! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: String) { stringField(param: $param) }""",
            {"param": True},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < True >; Expected type < String >; String cannot represent a non string value: < True >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: String) { stringField(param: $param) }""",
            {"param": 23456.789e2},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < 2345678.9 >; Expected type < String >; String cannot represent a non string value: < 2345678.9 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: String) { stringField(param: $param) }""",
            {"param": 10},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < 10 >; Expected type < String >; String cannot represent a non string value: < 10 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: String) { stringField(param: $param) }""",
            {"param": [None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [None] >; Expected type < String >; String cannot represent a non string value: < [None] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: String) { stringField(param: $param) }""",
            {"param": [True]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [True] >; Expected type < String >; String cannot represent a non string value: < [True] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: String) { stringField(param: $param) }""",
            {"param": ["ENUM_1"]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < ['ENUM_1'] >; Expected type < String >; String cannot represent a non string value: < ['ENUM_1'] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: String) { stringField(param: $param) }""",
            {"param": [23456.789e2]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [2345678.9] >; Expected type < String >; String cannot represent a non string value: < [2345678.9] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: String) { stringField(param: $param) }""",
            {"param": [10]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [10] >; Expected type < String >; String cannot represent a non string value: < [10] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: String) { stringField(param: $param) }""",
            {"param": ["paramValue"]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < ['paramValue'] >; Expected type < String >; String cannot represent a non string value: < ['paramValue'] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: String) { stringField(param: $param) }""",
            {"param": {}},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < {} >; Expected type < String >; String cannot represent a non string value: < {} >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
    ],
)
async def test_coercion_string_field_variables_errors(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query ($param: MyInput!) { inputObjectField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < MyInput! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyInput!) { inputObjectField(param: $param) }""",
            {},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < MyInput! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyInput!) { inputObjectField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < MyInput! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyInput) { inputObjectField(param: $param) }""",
            {"param": True},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < True >; Expected type < MyInput > to be an object.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyInput) { inputObjectField(param: $param) }""",
            {"param": "ENUM_1"},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < ENUM_1 >; Expected type < MyInput > to be an object.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyInput) { inputObjectField(param: $param) }""",
            {"param": 23456.789e2},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < 2345678.9 >; Expected type < MyInput > to be an object.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyInput) { inputObjectField(param: $param) }""",
            {"param": 10},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < 10 >; Expected type < MyInput > to be an object.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyInput) { inputObjectField(param: $param) }""",
            {"param": "paramValue"},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < paramValue >; Expected type < MyInput > to be an object.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyInput) { inputObjectField(param: $param) }""",
            {"param": [None]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [None] >; Expected type < MyInput > to be an object.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyInput) { inputObjectField(param: $param) }""",
            {"param": [True]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [True] >; Expected type < MyInput > to be an object.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyInput) { inputObjectField(param: $param) }""",
            {"param": ["ENUM_1"]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < ['ENUM_1'] >; Expected type < MyInput > to be an object.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyInput) { inputObjectField(param: $param) }""",
            {"param": [23456.789e2]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [2345678.9] >; Expected type < MyInput > to be an object.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyInput) { inputObjectField(param: $param) }""",
            {"param": [10]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < [10] >; Expected type < MyInput > to be an object.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyInput) { inputObjectField(param: $param) }""",
            {"param": ["paramValue"]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < ['paramValue'] >; Expected type < MyInput > to be an object.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyInput) { inputObjectField(param: $param) }""",
            {
                "param": {
                    "undefinedField1": "value1",
                    "undefinedField2": "value2",
                }
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < {'undefinedField1': 'value1', 'undefinedField2': 'value2'} >; Field < undefinedField1 > is not defined by type < MyInput >; Did you mean intField?",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'undefinedField1': 'value1', 'undefinedField2': 'value2'} >; Field < undefinedField2 > is not defined by type < MyInput >; Did you mean intField?",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                ],
            },
        ),
        (
            """query ($param: WrapperNonNullMyInput) { wrapperNonNullInputObjectField(param: $param) }""",
            {"param": {}},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.booleanField > of required type < Boolean! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.enumField > of required type < MyEnum! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.floatField > of required type < Float! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.intField > of required type < Int! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.stringField > of required type < String! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.listBooleanField > of required type < [Boolean]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.listEnumField > of required type < [MyEnum]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.listFloatField > of required type < [Float]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.listIntField > of required type < [Int]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.listStringField > of required type < [String]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                ],
            },
        ),
        (
            """query ($param: WrapperNonNullMyInput) { wrapperNonNullInputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": None,
                    "enumField": None,
                    "floatField": None,
                    "intField": None,
                    "stringField": None,
                    "listBooleanField": None,
                    "listEnumField": None,
                    "listFloatField": None,
                    "listIntField": None,
                    "listStringField": None,
                }
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < Boolean! > not to be null at value.booleanField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < MyEnum! > not to be null at value.enumField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < Float! > not to be null at value.floatField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < Int! > not to be null at value.intField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < String! > not to be null at value.stringField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < [Boolean]! > not to be null at value.listBooleanField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < [MyEnum]! > not to be null at value.listEnumField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < [Float]! > not to be null at value.listFloatField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < [Int]! > not to be null at value.listIntField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < [String]! > not to be null at value.listStringField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                ],
            },
        ),
        (
            """query ($param: MyInput) { inputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": True,
                    "floatField": True,
                    "intField": True,
                    "stringField": True,
                    "listBooleanField": True,
                    "listEnumField": True,
                    "listFloatField": True,
                    "listIntField": True,
                    "listStringField": True,
                }
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': True, 'enumField': True, 'floatField': True, 'intField': True, 'stringField': True, 'listBooleanField': True, 'listEnumField': True, 'listFloatField': True, 'listIntField': True, 'listStringField': True} >; Expected type < MyEnum > at value.enumField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': True, 'enumField': True, 'floatField': True, 'intField': True, 'stringField': True, 'listBooleanField': True, 'listEnumField': True, 'listFloatField': True, 'listIntField': True, 'listStringField': True} >; Expected type < Float > at value.floatField; Float cannot represent non numeric value: < True >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': True, 'enumField': True, 'floatField': True, 'intField': True, 'stringField': True, 'listBooleanField': True, 'listEnumField': True, 'listFloatField': True, 'listIntField': True, 'listStringField': True} >; Expected type < Int > at value.intField; Int cannot represent non-integer value: < True >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': True, 'enumField': True, 'floatField': True, 'intField': True, 'stringField': True, 'listBooleanField': True, 'listEnumField': True, 'listFloatField': True, 'listIntField': True, 'listStringField': True} >; Expected type < String > at value.stringField; String cannot represent a non string value: < True >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': True, 'enumField': True, 'floatField': True, 'intField': True, 'stringField': True, 'listBooleanField': True, 'listEnumField': True, 'listFloatField': True, 'listIntField': True, 'listStringField': True} >; Expected type < MyEnum > at value.listEnumField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': True, 'enumField': True, 'floatField': True, 'intField': True, 'stringField': True, 'listBooleanField': True, 'listEnumField': True, 'listFloatField': True, 'listIntField': True, 'listStringField': True} >; Expected type < Float > at value.listFloatField; Float cannot represent non numeric value: < True >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': True, 'enumField': True, 'floatField': True, 'intField': True, 'stringField': True, 'listBooleanField': True, 'listEnumField': True, 'listFloatField': True, 'listIntField': True, 'listStringField': True} >; Expected type < Int > at value.listIntField; Int cannot represent non-integer value: < True >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': True, 'enumField': True, 'floatField': True, 'intField': True, 'stringField': True, 'listBooleanField': True, 'listEnumField': True, 'listFloatField': True, 'listIntField': True, 'listStringField': True} >; Expected type < String > at value.listStringField; String cannot represent a non string value: < True >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                ],
            },
        ),
        (
            """query ($param: MyInput) { inputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": "ENUM_1",
                    "enumField": "ENUM_1",
                    "floatField": "ENUM_1",
                    "intField": "ENUM_1",
                    "stringField": "ENUM_1",
                    "listBooleanField": "ENUM_1",
                    "listEnumField": "ENUM_1",
                    "listFloatField": "ENUM_1",
                    "listIntField": "ENUM_1",
                    "listStringField": "ENUM_1",
                }
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 'ENUM_1', 'enumField': 'ENUM_1', 'floatField': 'ENUM_1', 'intField': 'ENUM_1', 'stringField': 'ENUM_1', 'listBooleanField': 'ENUM_1', 'listEnumField': 'ENUM_1', 'listFloatField': 'ENUM_1', 'listIntField': 'ENUM_1', 'listStringField': 'ENUM_1'} >; Expected type < Boolean > at value.booleanField; Boolean cannot represent a non boolean value: < ENUM_1 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 'ENUM_1', 'enumField': 'ENUM_1', 'floatField': 'ENUM_1', 'intField': 'ENUM_1', 'stringField': 'ENUM_1', 'listBooleanField': 'ENUM_1', 'listEnumField': 'ENUM_1', 'listFloatField': 'ENUM_1', 'listIntField': 'ENUM_1', 'listStringField': 'ENUM_1'} >; Expected type < Float > at value.floatField; Float cannot represent non numeric value: < ENUM_1 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 'ENUM_1', 'enumField': 'ENUM_1', 'floatField': 'ENUM_1', 'intField': 'ENUM_1', 'stringField': 'ENUM_1', 'listBooleanField': 'ENUM_1', 'listEnumField': 'ENUM_1', 'listFloatField': 'ENUM_1', 'listIntField': 'ENUM_1', 'listStringField': 'ENUM_1'} >; Expected type < Int > at value.intField; Int cannot represent non-integer value: < ENUM_1 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 'ENUM_1', 'enumField': 'ENUM_1', 'floatField': 'ENUM_1', 'intField': 'ENUM_1', 'stringField': 'ENUM_1', 'listBooleanField': 'ENUM_1', 'listEnumField': 'ENUM_1', 'listFloatField': 'ENUM_1', 'listIntField': 'ENUM_1', 'listStringField': 'ENUM_1'} >; Expected type < Boolean > at value.listBooleanField; Boolean cannot represent a non boolean value: < ENUM_1 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 'ENUM_1', 'enumField': 'ENUM_1', 'floatField': 'ENUM_1', 'intField': 'ENUM_1', 'stringField': 'ENUM_1', 'listBooleanField': 'ENUM_1', 'listEnumField': 'ENUM_1', 'listFloatField': 'ENUM_1', 'listIntField': 'ENUM_1', 'listStringField': 'ENUM_1'} >; Expected type < Float > at value.listFloatField; Float cannot represent non numeric value: < ENUM_1 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 'ENUM_1', 'enumField': 'ENUM_1', 'floatField': 'ENUM_1', 'intField': 'ENUM_1', 'stringField': 'ENUM_1', 'listBooleanField': 'ENUM_1', 'listEnumField': 'ENUM_1', 'listFloatField': 'ENUM_1', 'listIntField': 'ENUM_1', 'listStringField': 'ENUM_1'} >; Expected type < Int > at value.listIntField; Int cannot represent non-integer value: < ENUM_1 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                ],
            },
        ),
        (
            """query ($param: MyInput) { inputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": 23456.789e2,
                    "enumField": 23456.789e2,
                    "floatField": 23456.789e2,
                    "intField": 23456.789e2,
                    "stringField": 23456.789e2,
                    "listBooleanField": 23456.789e2,
                    "listEnumField": 23456.789e2,
                    "listFloatField": 23456.789e2,
                    "listIntField": 23456.789e2,
                    "listStringField": 23456.789e2,
                }
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 2345678.9, 'enumField': 2345678.9, 'floatField': 2345678.9, 'intField': 2345678.9, 'stringField': 2345678.9, 'listBooleanField': 2345678.9, 'listEnumField': 2345678.9, 'listFloatField': 2345678.9, 'listIntField': 2345678.9, 'listStringField': 2345678.9} >; Expected type < Boolean > at value.booleanField; Boolean cannot represent a non boolean value: < 2345678.9 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 2345678.9, 'enumField': 2345678.9, 'floatField': 2345678.9, 'intField': 2345678.9, 'stringField': 2345678.9, 'listBooleanField': 2345678.9, 'listEnumField': 2345678.9, 'listFloatField': 2345678.9, 'listIntField': 2345678.9, 'listStringField': 2345678.9} >; Expected type < MyEnum > at value.enumField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 2345678.9, 'enumField': 2345678.9, 'floatField': 2345678.9, 'intField': 2345678.9, 'stringField': 2345678.9, 'listBooleanField': 2345678.9, 'listEnumField': 2345678.9, 'listFloatField': 2345678.9, 'listIntField': 2345678.9, 'listStringField': 2345678.9} >; Expected type < Int > at value.intField; Int cannot represent non-integer value: < 2345678.9 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 2345678.9, 'enumField': 2345678.9, 'floatField': 2345678.9, 'intField': 2345678.9, 'stringField': 2345678.9, 'listBooleanField': 2345678.9, 'listEnumField': 2345678.9, 'listFloatField': 2345678.9, 'listIntField': 2345678.9, 'listStringField': 2345678.9} >; Expected type < String > at value.stringField; String cannot represent a non string value: < 2345678.9 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 2345678.9, 'enumField': 2345678.9, 'floatField': 2345678.9, 'intField': 2345678.9, 'stringField': 2345678.9, 'listBooleanField': 2345678.9, 'listEnumField': 2345678.9, 'listFloatField': 2345678.9, 'listIntField': 2345678.9, 'listStringField': 2345678.9} >; Expected type < Boolean > at value.listBooleanField; Boolean cannot represent a non boolean value: < 2345678.9 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 2345678.9, 'enumField': 2345678.9, 'floatField': 2345678.9, 'intField': 2345678.9, 'stringField': 2345678.9, 'listBooleanField': 2345678.9, 'listEnumField': 2345678.9, 'listFloatField': 2345678.9, 'listIntField': 2345678.9, 'listStringField': 2345678.9} >; Expected type < MyEnum > at value.listEnumField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 2345678.9, 'enumField': 2345678.9, 'floatField': 2345678.9, 'intField': 2345678.9, 'stringField': 2345678.9, 'listBooleanField': 2345678.9, 'listEnumField': 2345678.9, 'listFloatField': 2345678.9, 'listIntField': 2345678.9, 'listStringField': 2345678.9} >; Expected type < Int > at value.listIntField; Int cannot represent non-integer value: < 2345678.9 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 2345678.9, 'enumField': 2345678.9, 'floatField': 2345678.9, 'intField': 2345678.9, 'stringField': 2345678.9, 'listBooleanField': 2345678.9, 'listEnumField': 2345678.9, 'listFloatField': 2345678.9, 'listIntField': 2345678.9, 'listStringField': 2345678.9} >; Expected type < String > at value.listStringField; String cannot represent a non string value: < 2345678.9 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                ],
            },
        ),
        (
            """query ($param: MyInput) { inputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": 10,
                    "enumField": 10,
                    "floatField": 10,
                    "intField": 10,
                    "stringField": 10,
                    "listBooleanField": 10,
                    "listEnumField": 10,
                    "listFloatField": 10,
                    "listIntField": 10,
                    "listStringField": 10,
                }
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 10, 'enumField': 10, 'floatField': 10, 'intField': 10, 'stringField': 10, 'listBooleanField': 10, 'listEnumField': 10, 'listFloatField': 10, 'listIntField': 10, 'listStringField': 10} >; Expected type < Boolean > at value.booleanField; Boolean cannot represent a non boolean value: < 10 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 10, 'enumField': 10, 'floatField': 10, 'intField': 10, 'stringField': 10, 'listBooleanField': 10, 'listEnumField': 10, 'listFloatField': 10, 'listIntField': 10, 'listStringField': 10} >; Expected type < MyEnum > at value.enumField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 10, 'enumField': 10, 'floatField': 10, 'intField': 10, 'stringField': 10, 'listBooleanField': 10, 'listEnumField': 10, 'listFloatField': 10, 'listIntField': 10, 'listStringField': 10} >; Expected type < String > at value.stringField; String cannot represent a non string value: < 10 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 10, 'enumField': 10, 'floatField': 10, 'intField': 10, 'stringField': 10, 'listBooleanField': 10, 'listEnumField': 10, 'listFloatField': 10, 'listIntField': 10, 'listStringField': 10} >; Expected type < Boolean > at value.listBooleanField; Boolean cannot represent a non boolean value: < 10 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 10, 'enumField': 10, 'floatField': 10, 'intField': 10, 'stringField': 10, 'listBooleanField': 10, 'listEnumField': 10, 'listFloatField': 10, 'listIntField': 10, 'listStringField': 10} >; Expected type < MyEnum > at value.listEnumField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 10, 'enumField': 10, 'floatField': 10, 'intField': 10, 'stringField': 10, 'listBooleanField': 10, 'listEnumField': 10, 'listFloatField': 10, 'listIntField': 10, 'listStringField': 10} >; Expected type < String > at value.listStringField; String cannot represent a non string value: < 10 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                ],
            },
        ),
        (
            """query ($param: MyInput) { inputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": "paramValue",
                    "enumField": "paramValue",
                    "floatField": "paramValue",
                    "intField": "paramValue",
                    "stringField": "paramValue",
                    "listBooleanField": "paramValue",
                    "listEnumField": "paramValue",
                    "listFloatField": "paramValue",
                    "listIntField": "paramValue",
                    "listStringField": "paramValue",
                }
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 'paramValue', 'enumField': 'paramValue', 'floatField': 'paramValue', 'intField': 'paramValue', 'stringField': 'paramValue', 'listBooleanField': 'paramValue', 'listEnumField': 'paramValue', 'listFloatField': 'paramValue', 'listIntField': 'paramValue', 'listStringField': 'paramValue'} >; Expected type < Boolean > at value.booleanField; Boolean cannot represent a non boolean value: < paramValue >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 'paramValue', 'enumField': 'paramValue', 'floatField': 'paramValue', 'intField': 'paramValue', 'stringField': 'paramValue', 'listBooleanField': 'paramValue', 'listEnumField': 'paramValue', 'listFloatField': 'paramValue', 'listIntField': 'paramValue', 'listStringField': 'paramValue'} >; Expected type < MyEnum > at value.enumField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 'paramValue', 'enumField': 'paramValue', 'floatField': 'paramValue', 'intField': 'paramValue', 'stringField': 'paramValue', 'listBooleanField': 'paramValue', 'listEnumField': 'paramValue', 'listFloatField': 'paramValue', 'listIntField': 'paramValue', 'listStringField': 'paramValue'} >; Expected type < Float > at value.floatField; Float cannot represent non numeric value: < paramValue >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 'paramValue', 'enumField': 'paramValue', 'floatField': 'paramValue', 'intField': 'paramValue', 'stringField': 'paramValue', 'listBooleanField': 'paramValue', 'listEnumField': 'paramValue', 'listFloatField': 'paramValue', 'listIntField': 'paramValue', 'listStringField': 'paramValue'} >; Expected type < Int > at value.intField; Int cannot represent non-integer value: < paramValue >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 'paramValue', 'enumField': 'paramValue', 'floatField': 'paramValue', 'intField': 'paramValue', 'stringField': 'paramValue', 'listBooleanField': 'paramValue', 'listEnumField': 'paramValue', 'listFloatField': 'paramValue', 'listIntField': 'paramValue', 'listStringField': 'paramValue'} >; Expected type < Boolean > at value.listBooleanField; Boolean cannot represent a non boolean value: < paramValue >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 'paramValue', 'enumField': 'paramValue', 'floatField': 'paramValue', 'intField': 'paramValue', 'stringField': 'paramValue', 'listBooleanField': 'paramValue', 'listEnumField': 'paramValue', 'listFloatField': 'paramValue', 'listIntField': 'paramValue', 'listStringField': 'paramValue'} >; Expected type < MyEnum > at value.listEnumField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 'paramValue', 'enumField': 'paramValue', 'floatField': 'paramValue', 'intField': 'paramValue', 'stringField': 'paramValue', 'listBooleanField': 'paramValue', 'listEnumField': 'paramValue', 'listFloatField': 'paramValue', 'listIntField': 'paramValue', 'listStringField': 'paramValue'} >; Expected type < Float > at value.listFloatField; Float cannot represent non numeric value: < paramValue >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': 'paramValue', 'enumField': 'paramValue', 'floatField': 'paramValue', 'intField': 'paramValue', 'stringField': 'paramValue', 'listBooleanField': 'paramValue', 'listEnumField': 'paramValue', 'listFloatField': 'paramValue', 'listIntField': 'paramValue', 'listStringField': 'paramValue'} >; Expected type < Int > at value.listIntField; Int cannot represent non-integer value: < paramValue >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                ],
            },
        ),
        (
            """query ($param: MyInput) { inputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": [None],
                    "enumField": [None],
                    "floatField": [None],
                    "intField": [None],
                    "stringField": [None],
                    "listBooleanField": [None],
                    "listEnumField": [None],
                    "listFloatField": [None],
                    "listIntField": [None],
                    "listStringField": [None],
                }
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [None], 'enumField': [None], 'floatField': [None], 'intField': [None], 'stringField': [None], 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected type < Boolean > at value.booleanField; Boolean cannot represent a non boolean value: < [None] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [None], 'enumField': [None], 'floatField': [None], 'intField': [None], 'stringField': [None], 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected type < MyEnum > at value.enumField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [None], 'enumField': [None], 'floatField': [None], 'intField': [None], 'stringField': [None], 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected type < Float > at value.floatField; Float cannot represent non numeric value: < [None] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [None], 'enumField': [None], 'floatField': [None], 'intField': [None], 'stringField': [None], 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected type < Int > at value.intField; Int cannot represent non-integer value: < [None] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [None], 'enumField': [None], 'floatField': [None], 'intField': [None], 'stringField': [None], 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected type < String > at value.stringField; String cannot represent a non string value: < [None] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                ],
            },
        ),
        (
            """query ($param: MyInput) { inputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": [True],
                    "enumField": [True],
                    "floatField": [True],
                    "intField": [True],
                    "stringField": [True],
                    "listBooleanField": [True],
                    "listEnumField": [True],
                    "listFloatField": [True],
                    "listIntField": [True],
                    "listStringField": [True],
                }
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [True], 'enumField': [True], 'floatField': [True], 'intField': [True], 'stringField': [True], 'listBooleanField': [True], 'listEnumField': [True], 'listFloatField': [True], 'listIntField': [True], 'listStringField': [True]} >; Expected type < Boolean > at value.booleanField; Boolean cannot represent a non boolean value: < [True] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [True], 'enumField': [True], 'floatField': [True], 'intField': [True], 'stringField': [True], 'listBooleanField': [True], 'listEnumField': [True], 'listFloatField': [True], 'listIntField': [True], 'listStringField': [True]} >; Expected type < MyEnum > at value.enumField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [True], 'enumField': [True], 'floatField': [True], 'intField': [True], 'stringField': [True], 'listBooleanField': [True], 'listEnumField': [True], 'listFloatField': [True], 'listIntField': [True], 'listStringField': [True]} >; Expected type < Float > at value.floatField; Float cannot represent non numeric value: < [True] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [True], 'enumField': [True], 'floatField': [True], 'intField': [True], 'stringField': [True], 'listBooleanField': [True], 'listEnumField': [True], 'listFloatField': [True], 'listIntField': [True], 'listStringField': [True]} >; Expected type < Int > at value.intField; Int cannot represent non-integer value: < [True] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [True], 'enumField': [True], 'floatField': [True], 'intField': [True], 'stringField': [True], 'listBooleanField': [True], 'listEnumField': [True], 'listFloatField': [True], 'listIntField': [True], 'listStringField': [True]} >; Expected type < String > at value.stringField; String cannot represent a non string value: < [True] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [True], 'enumField': [True], 'floatField': [True], 'intField': [True], 'stringField': [True], 'listBooleanField': [True], 'listEnumField': [True], 'listFloatField': [True], 'listIntField': [True], 'listStringField': [True]} >; Expected type < MyEnum > at value.listEnumField[0].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [True], 'enumField': [True], 'floatField': [True], 'intField': [True], 'stringField': [True], 'listBooleanField': [True], 'listEnumField': [True], 'listFloatField': [True], 'listIntField': [True], 'listStringField': [True]} >; Expected type < Float > at value.listFloatField[0]; Float cannot represent non numeric value: < True >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [True], 'enumField': [True], 'floatField': [True], 'intField': [True], 'stringField': [True], 'listBooleanField': [True], 'listEnumField': [True], 'listFloatField': [True], 'listIntField': [True], 'listStringField': [True]} >; Expected type < Int > at value.listIntField[0]; Int cannot represent non-integer value: < True >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [True], 'enumField': [True], 'floatField': [True], 'intField': [True], 'stringField': [True], 'listBooleanField': [True], 'listEnumField': [True], 'listFloatField': [True], 'listIntField': [True], 'listStringField': [True]} >; Expected type < String > at value.listStringField[0]; String cannot represent a non string value: < True >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                ],
            },
        ),
        (
            """query ($param: MyInput) { inputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": ["ENUM_1"],
                    "enumField": ["ENUM_1"],
                    "floatField": ["ENUM_1"],
                    "intField": ["ENUM_1"],
                    "stringField": ["ENUM_1"],
                    "listBooleanField": ["ENUM_1"],
                    "listEnumField": ["ENUM_1"],
                    "listFloatField": ["ENUM_1"],
                    "listIntField": ["ENUM_1"],
                    "listStringField": ["ENUM_1"],
                }
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': ['ENUM_1'], 'enumField': ['ENUM_1'], 'floatField': ['ENUM_1'], 'intField': ['ENUM_1'], 'stringField': ['ENUM_1'], 'listBooleanField': ['ENUM_1'], 'listEnumField': ['ENUM_1'], 'listFloatField': ['ENUM_1'], 'listIntField': ['ENUM_1'], 'listStringField': ['ENUM_1']} >; Expected type < Boolean > at value.booleanField; Boolean cannot represent a non boolean value: < ['ENUM_1'] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': ['ENUM_1'], 'enumField': ['ENUM_1'], 'floatField': ['ENUM_1'], 'intField': ['ENUM_1'], 'stringField': ['ENUM_1'], 'listBooleanField': ['ENUM_1'], 'listEnumField': ['ENUM_1'], 'listFloatField': ['ENUM_1'], 'listIntField': ['ENUM_1'], 'listStringField': ['ENUM_1']} >; Expected type < MyEnum > at value.enumField; Did you mean ENUM_1, ENUM_4, ENUM_3, or ENUM_2?",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': ['ENUM_1'], 'enumField': ['ENUM_1'], 'floatField': ['ENUM_1'], 'intField': ['ENUM_1'], 'stringField': ['ENUM_1'], 'listBooleanField': ['ENUM_1'], 'listEnumField': ['ENUM_1'], 'listFloatField': ['ENUM_1'], 'listIntField': ['ENUM_1'], 'listStringField': ['ENUM_1']} >; Expected type < Float > at value.floatField; Float cannot represent non numeric value: < ['ENUM_1'] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': ['ENUM_1'], 'enumField': ['ENUM_1'], 'floatField': ['ENUM_1'], 'intField': ['ENUM_1'], 'stringField': ['ENUM_1'], 'listBooleanField': ['ENUM_1'], 'listEnumField': ['ENUM_1'], 'listFloatField': ['ENUM_1'], 'listIntField': ['ENUM_1'], 'listStringField': ['ENUM_1']} >; Expected type < Int > at value.intField; Int cannot represent non-integer value: < ['ENUM_1'] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': ['ENUM_1'], 'enumField': ['ENUM_1'], 'floatField': ['ENUM_1'], 'intField': ['ENUM_1'], 'stringField': ['ENUM_1'], 'listBooleanField': ['ENUM_1'], 'listEnumField': ['ENUM_1'], 'listFloatField': ['ENUM_1'], 'listIntField': ['ENUM_1'], 'listStringField': ['ENUM_1']} >; Expected type < String > at value.stringField; String cannot represent a non string value: < ['ENUM_1'] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': ['ENUM_1'], 'enumField': ['ENUM_1'], 'floatField': ['ENUM_1'], 'intField': ['ENUM_1'], 'stringField': ['ENUM_1'], 'listBooleanField': ['ENUM_1'], 'listEnumField': ['ENUM_1'], 'listFloatField': ['ENUM_1'], 'listIntField': ['ENUM_1'], 'listStringField': ['ENUM_1']} >; Expected type < Boolean > at value.listBooleanField[0]; Boolean cannot represent a non boolean value: < ENUM_1 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': ['ENUM_1'], 'enumField': ['ENUM_1'], 'floatField': ['ENUM_1'], 'intField': ['ENUM_1'], 'stringField': ['ENUM_1'], 'listBooleanField': ['ENUM_1'], 'listEnumField': ['ENUM_1'], 'listFloatField': ['ENUM_1'], 'listIntField': ['ENUM_1'], 'listStringField': ['ENUM_1']} >; Expected type < Float > at value.listFloatField[0]; Float cannot represent non numeric value: < ENUM_1 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': ['ENUM_1'], 'enumField': ['ENUM_1'], 'floatField': ['ENUM_1'], 'intField': ['ENUM_1'], 'stringField': ['ENUM_1'], 'listBooleanField': ['ENUM_1'], 'listEnumField': ['ENUM_1'], 'listFloatField': ['ENUM_1'], 'listIntField': ['ENUM_1'], 'listStringField': ['ENUM_1']} >; Expected type < Int > at value.listIntField[0]; Int cannot represent non-integer value: < ENUM_1 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                ],
            },
        ),
        (
            """query ($param: MyInput) { inputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": [23456.789e2],
                    "enumField": [23456.789e2],
                    "floatField": [23456.789e2],
                    "intField": [23456.789e2],
                    "stringField": [23456.789e2],
                    "listBooleanField": [23456.789e2],
                    "listEnumField": [23456.789e2],
                    "listFloatField": [23456.789e2],
                    "listIntField": [23456.789e2],
                    "listStringField": [23456.789e2],
                }
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [2345678.9], 'enumField': [2345678.9], 'floatField': [2345678.9], 'intField': [2345678.9], 'stringField': [2345678.9], 'listBooleanField': [2345678.9], 'listEnumField': [2345678.9], 'listFloatField': [2345678.9], 'listIntField': [2345678.9], 'listStringField': [2345678.9]} >; Expected type < Boolean > at value.booleanField; Boolean cannot represent a non boolean value: < [2345678.9] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [2345678.9], 'enumField': [2345678.9], 'floatField': [2345678.9], 'intField': [2345678.9], 'stringField': [2345678.9], 'listBooleanField': [2345678.9], 'listEnumField': [2345678.9], 'listFloatField': [2345678.9], 'listIntField': [2345678.9], 'listStringField': [2345678.9]} >; Expected type < MyEnum > at value.enumField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [2345678.9], 'enumField': [2345678.9], 'floatField': [2345678.9], 'intField': [2345678.9], 'stringField': [2345678.9], 'listBooleanField': [2345678.9], 'listEnumField': [2345678.9], 'listFloatField': [2345678.9], 'listIntField': [2345678.9], 'listStringField': [2345678.9]} >; Expected type < Float > at value.floatField; Float cannot represent non numeric value: < [2345678.9] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [2345678.9], 'enumField': [2345678.9], 'floatField': [2345678.9], 'intField': [2345678.9], 'stringField': [2345678.9], 'listBooleanField': [2345678.9], 'listEnumField': [2345678.9], 'listFloatField': [2345678.9], 'listIntField': [2345678.9], 'listStringField': [2345678.9]} >; Expected type < Int > at value.intField; Int cannot represent non-integer value: < [2345678.9] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [2345678.9], 'enumField': [2345678.9], 'floatField': [2345678.9], 'intField': [2345678.9], 'stringField': [2345678.9], 'listBooleanField': [2345678.9], 'listEnumField': [2345678.9], 'listFloatField': [2345678.9], 'listIntField': [2345678.9], 'listStringField': [2345678.9]} >; Expected type < String > at value.stringField; String cannot represent a non string value: < [2345678.9] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [2345678.9], 'enumField': [2345678.9], 'floatField': [2345678.9], 'intField': [2345678.9], 'stringField': [2345678.9], 'listBooleanField': [2345678.9], 'listEnumField': [2345678.9], 'listFloatField': [2345678.9], 'listIntField': [2345678.9], 'listStringField': [2345678.9]} >; Expected type < Boolean > at value.listBooleanField[0]; Boolean cannot represent a non boolean value: < 2345678.9 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [2345678.9], 'enumField': [2345678.9], 'floatField': [2345678.9], 'intField': [2345678.9], 'stringField': [2345678.9], 'listBooleanField': [2345678.9], 'listEnumField': [2345678.9], 'listFloatField': [2345678.9], 'listIntField': [2345678.9], 'listStringField': [2345678.9]} >; Expected type < MyEnum > at value.listEnumField[0].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [2345678.9], 'enumField': [2345678.9], 'floatField': [2345678.9], 'intField': [2345678.9], 'stringField': [2345678.9], 'listBooleanField': [2345678.9], 'listEnumField': [2345678.9], 'listFloatField': [2345678.9], 'listIntField': [2345678.9], 'listStringField': [2345678.9]} >; Expected type < Int > at value.listIntField[0]; Int cannot represent non-integer value: < 2345678.9 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [2345678.9], 'enumField': [2345678.9], 'floatField': [2345678.9], 'intField': [2345678.9], 'stringField': [2345678.9], 'listBooleanField': [2345678.9], 'listEnumField': [2345678.9], 'listFloatField': [2345678.9], 'listIntField': [2345678.9], 'listStringField': [2345678.9]} >; Expected type < String > at value.listStringField[0]; String cannot represent a non string value: < 2345678.9 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                ],
            },
        ),
        (
            """query ($param: MyInput) { inputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": [10],
                    "enumField": [10],
                    "floatField": [10],
                    "intField": [10],
                    "stringField": [10],
                    "listBooleanField": [10],
                    "listEnumField": [10],
                    "listFloatField": [10],
                    "listIntField": [10],
                    "listStringField": [10],
                }
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [10], 'enumField': [10], 'floatField': [10], 'intField': [10], 'stringField': [10], 'listBooleanField': [10], 'listEnumField': [10], 'listFloatField': [10], 'listIntField': [10], 'listStringField': [10]} >; Expected type < Boolean > at value.booleanField; Boolean cannot represent a non boolean value: < [10] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [10], 'enumField': [10], 'floatField': [10], 'intField': [10], 'stringField': [10], 'listBooleanField': [10], 'listEnumField': [10], 'listFloatField': [10], 'listIntField': [10], 'listStringField': [10]} >; Expected type < MyEnum > at value.enumField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [10], 'enumField': [10], 'floatField': [10], 'intField': [10], 'stringField': [10], 'listBooleanField': [10], 'listEnumField': [10], 'listFloatField': [10], 'listIntField': [10], 'listStringField': [10]} >; Expected type < Float > at value.floatField; Float cannot represent non numeric value: < [10] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [10], 'enumField': [10], 'floatField': [10], 'intField': [10], 'stringField': [10], 'listBooleanField': [10], 'listEnumField': [10], 'listFloatField': [10], 'listIntField': [10], 'listStringField': [10]} >; Expected type < Int > at value.intField; Int cannot represent non-integer value: < [10] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [10], 'enumField': [10], 'floatField': [10], 'intField': [10], 'stringField': [10], 'listBooleanField': [10], 'listEnumField': [10], 'listFloatField': [10], 'listIntField': [10], 'listStringField': [10]} >; Expected type < String > at value.stringField; String cannot represent a non string value: < [10] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [10], 'enumField': [10], 'floatField': [10], 'intField': [10], 'stringField': [10], 'listBooleanField': [10], 'listEnumField': [10], 'listFloatField': [10], 'listIntField': [10], 'listStringField': [10]} >; Expected type < Boolean > at value.listBooleanField[0]; Boolean cannot represent a non boolean value: < 10 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [10], 'enumField': [10], 'floatField': [10], 'intField': [10], 'stringField': [10], 'listBooleanField': [10], 'listEnumField': [10], 'listFloatField': [10], 'listIntField': [10], 'listStringField': [10]} >; Expected type < MyEnum > at value.listEnumField[0].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': [10], 'enumField': [10], 'floatField': [10], 'intField': [10], 'stringField': [10], 'listBooleanField': [10], 'listEnumField': [10], 'listFloatField': [10], 'listIntField': [10], 'listStringField': [10]} >; Expected type < String > at value.listStringField[0]; String cannot represent a non string value: < 10 >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                ],
            },
        ),
        (
            """query ($param: MyInput) { inputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": ["paramValue"],
                    "enumField": ["paramValue"],
                    "floatField": ["paramValue"],
                    "intField": ["paramValue"],
                    "stringField": ["paramValue"],
                    "listBooleanField": ["paramValue"],
                    "listEnumField": ["paramValue"],
                    "listFloatField": ["paramValue"],
                    "listIntField": ["paramValue"],
                    "listStringField": ["paramValue"],
                }
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': ['paramValue'], 'enumField': ['paramValue'], 'floatField': ['paramValue'], 'intField': ['paramValue'], 'stringField': ['paramValue'], 'listBooleanField': ['paramValue'], 'listEnumField': ['paramValue'], 'listFloatField': ['paramValue'], 'listIntField': ['paramValue'], 'listStringField': ['paramValue']} >; Expected type < Boolean > at value.booleanField; Boolean cannot represent a non boolean value: < ['paramValue'] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': ['paramValue'], 'enumField': ['paramValue'], 'floatField': ['paramValue'], 'intField': ['paramValue'], 'stringField': ['paramValue'], 'listBooleanField': ['paramValue'], 'listEnumField': ['paramValue'], 'listFloatField': ['paramValue'], 'listIntField': ['paramValue'], 'listStringField': ['paramValue']} >; Expected type < MyEnum > at value.enumField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': ['paramValue'], 'enumField': ['paramValue'], 'floatField': ['paramValue'], 'intField': ['paramValue'], 'stringField': ['paramValue'], 'listBooleanField': ['paramValue'], 'listEnumField': ['paramValue'], 'listFloatField': ['paramValue'], 'listIntField': ['paramValue'], 'listStringField': ['paramValue']} >; Expected type < Float > at value.floatField; Float cannot represent non numeric value: < ['paramValue'] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': ['paramValue'], 'enumField': ['paramValue'], 'floatField': ['paramValue'], 'intField': ['paramValue'], 'stringField': ['paramValue'], 'listBooleanField': ['paramValue'], 'listEnumField': ['paramValue'], 'listFloatField': ['paramValue'], 'listIntField': ['paramValue'], 'listStringField': ['paramValue']} >; Expected type < Int > at value.intField; Int cannot represent non-integer value: < ['paramValue'] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': ['paramValue'], 'enumField': ['paramValue'], 'floatField': ['paramValue'], 'intField': ['paramValue'], 'stringField': ['paramValue'], 'listBooleanField': ['paramValue'], 'listEnumField': ['paramValue'], 'listFloatField': ['paramValue'], 'listIntField': ['paramValue'], 'listStringField': ['paramValue']} >; Expected type < String > at value.stringField; String cannot represent a non string value: < ['paramValue'] >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': ['paramValue'], 'enumField': ['paramValue'], 'floatField': ['paramValue'], 'intField': ['paramValue'], 'stringField': ['paramValue'], 'listBooleanField': ['paramValue'], 'listEnumField': ['paramValue'], 'listFloatField': ['paramValue'], 'listIntField': ['paramValue'], 'listStringField': ['paramValue']} >; Expected type < Boolean > at value.listBooleanField[0]; Boolean cannot represent a non boolean value: < paramValue >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': ['paramValue'], 'enumField': ['paramValue'], 'floatField': ['paramValue'], 'intField': ['paramValue'], 'stringField': ['paramValue'], 'listBooleanField': ['paramValue'], 'listEnumField': ['paramValue'], 'listFloatField': ['paramValue'], 'listIntField': ['paramValue'], 'listStringField': ['paramValue']} >; Expected type < MyEnum > at value.listEnumField[0].",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': ['paramValue'], 'enumField': ['paramValue'], 'floatField': ['paramValue'], 'intField': ['paramValue'], 'stringField': ['paramValue'], 'listBooleanField': ['paramValue'], 'listEnumField': ['paramValue'], 'listFloatField': ['paramValue'], 'listIntField': ['paramValue'], 'listStringField': ['paramValue']} >; Expected type < Float > at value.listFloatField[0]; Float cannot represent non numeric value: < paramValue >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': ['paramValue'], 'enumField': ['paramValue'], 'floatField': ['paramValue'], 'intField': ['paramValue'], 'stringField': ['paramValue'], 'listBooleanField': ['paramValue'], 'listEnumField': ['paramValue'], 'listFloatField': ['paramValue'], 'listIntField': ['paramValue'], 'listStringField': ['paramValue']} >; Expected type < Int > at value.listIntField[0]; Int cannot represent non-integer value: < paramValue >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                ],
            },
        ),
        (
            """query ($param: MyInput) { inputObjectField(param: $param) }""",
            {
                "param": {
                    "booleanField": {},
                    "enumField": {},
                    "floatField": {},
                    "intField": {},
                    "stringField": {},
                    "listBooleanField": {},
                    "listEnumField": {},
                    "listFloatField": {},
                    "listIntField": {},
                    "listStringField": {},
                }
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': {}, 'enumField': {}, 'floatField': {}, 'intField': {}, 'stringField': {}, 'listBooleanField': {}, 'listEnumField': {}, 'listFloatField': {}, 'listIntField': {}, 'listStringField': {}} >; Expected type < Boolean > at value.booleanField; Boolean cannot represent a non boolean value: < {} >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': {}, 'enumField': {}, 'floatField': {}, 'intField': {}, 'stringField': {}, 'listBooleanField': {}, 'listEnumField': {}, 'listFloatField': {}, 'listIntField': {}, 'listStringField': {}} >; Expected type < MyEnum > at value.enumField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': {}, 'enumField': {}, 'floatField': {}, 'intField': {}, 'stringField': {}, 'listBooleanField': {}, 'listEnumField': {}, 'listFloatField': {}, 'listIntField': {}, 'listStringField': {}} >; Expected type < Float > at value.floatField; Float cannot represent non numeric value: < {} >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': {}, 'enumField': {}, 'floatField': {}, 'intField': {}, 'stringField': {}, 'listBooleanField': {}, 'listEnumField': {}, 'listFloatField': {}, 'listIntField': {}, 'listStringField': {}} >; Expected type < Int > at value.intField; Int cannot represent non-integer value: < {} >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': {}, 'enumField': {}, 'floatField': {}, 'intField': {}, 'stringField': {}, 'listBooleanField': {}, 'listEnumField': {}, 'listFloatField': {}, 'listIntField': {}, 'listStringField': {}} >; Expected type < String > at value.stringField; String cannot represent a non string value: < {} >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': {}, 'enumField': {}, 'floatField': {}, 'intField': {}, 'stringField': {}, 'listBooleanField': {}, 'listEnumField': {}, 'listFloatField': {}, 'listIntField': {}, 'listStringField': {}} >; Expected type < Boolean > at value.listBooleanField; Boolean cannot represent a non boolean value: < {} >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': {}, 'enumField': {}, 'floatField': {}, 'intField': {}, 'stringField': {}, 'listBooleanField': {}, 'listEnumField': {}, 'listFloatField': {}, 'listIntField': {}, 'listStringField': {}} >; Expected type < MyEnum > at value.listEnumField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': {}, 'enumField': {}, 'floatField': {}, 'intField': {}, 'stringField': {}, 'listBooleanField': {}, 'listEnumField': {}, 'listFloatField': {}, 'listIntField': {}, 'listStringField': {}} >; Expected type < Float > at value.listFloatField; Float cannot represent non numeric value: < {} >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': {}, 'enumField': {}, 'floatField': {}, 'intField': {}, 'stringField': {}, 'listBooleanField': {}, 'listEnumField': {}, 'listFloatField': {}, 'listIntField': {}, 'listStringField': {}} >; Expected type < Int > at value.listIntField; Int cannot represent non-integer value: < {} >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': {}, 'enumField': {}, 'floatField': {}, 'intField': {}, 'stringField': {}, 'listBooleanField': {}, 'listEnumField': {}, 'listFloatField': {}, 'listIntField': {}, 'listStringField': {}} >; Expected type < String > at value.listStringField; String cannot represent a non string value: < {} >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                ],
            },
        ),
    ],
)
async def test_coercion_input_object_field_variables_errors(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected


def bakery(schema_name):
    @Directive("internalCoercionError", schema_name=schema_name)
    class InternalCoercionError:
        async def on_post_input_coercion(
            self, directive_args, next_directive, parent_node, value, ctx
        ):
            raise CoercionError("Oopsie")

    @Directive("customCoercionError", schema_name=schema_name)
    class CustomCoercionError:
        async def on_post_input_coercion(
            self, directive_args, next_directive, parent_node, value, ctx
        ):
            raise ValueError("Oopsie")

    @Scalar("FirstErrorScalar", schema_name=schema_name)
    @Scalar("SecondErrorScalar", schema_name=schema_name)
    class ErrorScalars(ScalarString):
        pass


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    directive @internalCoercionError on INPUT_FIELD_DEFINITION | SCALAR
    directive @customCoercionError on INPUT_FIELD_DEFINITION | SCALAR

    scalar FirstErrorScalar @internalCoercionError
    scalar SecondErrorScalar @customCoercionError

    input FirstInputField {
      inputField: String @internalCoercionError
    }

    input SecondInputField {
      inputField: String @customCoercionError
    }

    type Query {
      field(
        firstInput: FirstInputField
        secondInput: SecondInputField
        firstErrorScalar: FirstErrorScalar
        secondErrorScalar: SecondErrorScalar
      ): String
    }
    """,
    bakery=bakery,
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """
            query ($firstInput: FirstInputField!) {
              field(firstInput: $firstInput)
            }
            """,
            {"firstInput": {"inputField": "aValue"}},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Oopsie",
                        "path": None,
                        "locations": [{"line": 2, "column": 20}],
                    }
                ],
            },
        ),
        (
            """
            query ($secondInput: SecondInputField!) {
              field(secondInput: $secondInput)
            }
            """,
            {"secondInput": {"inputField": "aValue"}},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Oopsie",
                        "path": None,
                        "locations": [{"line": 2, "column": 20}],
                    }
                ],
            },
        ),
        (
            """
            query ($firstErrorScalar: FirstErrorScalar) {
              field(firstErrorScalar: $firstErrorScalar)
            }
            """,
            {"firstErrorScalar": "aValue"},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Oopsie",
                        "path": None,
                        "locations": [{"line": 2, "column": 20}],
                    }
                ],
            },
        ),
        (
            """
            query ($secondErrorScalar: SecondErrorScalar) {
              field(secondErrorScalar: $secondErrorScalar)
            }
            """,
            {"secondErrorScalar": "aValue"},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Oopsie",
                        "path": None,
                        "locations": [{"line": 2, "column": 20}],
                    }
                ],
            },
        ),
    ],
)
async def test_coercion_variables_errors(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected
