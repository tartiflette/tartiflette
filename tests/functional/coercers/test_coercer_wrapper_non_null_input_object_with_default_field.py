import pytest

from tests.functional.coercers.common import resolve_input_object_field


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={
        "Query.wrapperNonNullInputObjectWithDefaultField": resolve_input_object_field
    },
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { wrapperNonNullInputObjectWithDefaultField }""",
            None,
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_1_1-MyEnum-enumField]-[floatField:12345681.9]-[intField:123459]-[stringField:defaultstring-scalar-stringField]-[listBooleanField:True-None]-[listEnumField:enum_1_1-myenum-None]-[listFloatField:12345681.9-None]-[listIntField:123459-None]-[listStringField:defaultstring-scalar-None]"
                }
            },
        ),
        (
            """query { wrapperNonNullInputObjectWithDefaultField(param: null) }""",
            None,
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-None"
                }
            },
        ),
        (
            """query { wrapperNonNullInputObjectWithDefaultField(param: {}) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Field < WrapperNonNullMyInput.booleanField > of required type < Boolean! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 58}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Field < WrapperNonNullMyInput.enumField > of required type < MyEnum! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 58}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Field < WrapperNonNullMyInput.floatField > of required type < Float! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 58}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Field < WrapperNonNullMyInput.intField > of required type < Int! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 58}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Field < WrapperNonNullMyInput.stringField > of required type < String! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 58}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Field < WrapperNonNullMyInput.listBooleanField > of required type < [Boolean]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 58}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Field < WrapperNonNullMyInput.listEnumField > of required type < [MyEnum]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 58}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Field < WrapperNonNullMyInput.listFloatField > of required type < [Float]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 58}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Field < WrapperNonNullMyInput.listIntField > of required type < [Int]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 58}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Field < WrapperNonNullMyInput.listStringField > of required type < [String]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 58}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                ],
            },
        ),
        (
            """
            query {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: null
                listEnumField: null
                listFloatField: null
                listIntField: null
                listStringField: null
              })
            }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 5, "column": 28}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 6, "column": 29}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 7, "column": 27}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < String! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 8, "column": 30}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Boolean]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 9, "column": 35}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [MyEnum]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 10, "column": 32}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Float]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 11, "column": 33}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Int]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 12, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [String]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 13, "column": 34}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                ],
            },
        ),
        (
            """
            query {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: [null]
                listEnumField: [null]
                listFloatField: [null]
                listIntField: [null]
                listStringField: [null]
              })
            }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 5, "column": 28}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 6, "column": 29}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 7, "column": 27}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < String! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 8, "column": 30}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                ],
            },
        ),
        (
            """
            query {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: false
                enumField: ENUM_2
                floatField: 23456.789e2
                intField: 10
                stringField: "paramDefaultValue"
                listBooleanField: false
                listEnumField: ENUM_2
                listFloatField: 23456.789e2
                listIntField: 10
                listStringField: "paramDefaultValue"
              })
            }""",
            None,
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:False]-[enumField:ENUM_2_2-MyEnum-enumField]-[floatField:2345681.9]-[intField:13]-[stringField:paramdefaultvalue-scalar-stringField]-[listBooleanField:False]-[listEnumField:enum_2_2-myenum]-[listFloatField:2345681.9]-[listIntField:13]-[listStringField:paramdefaultvalue-scalar]"
                }
            },
        ),
        (
            """
            query {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: false
                enumField: ENUM_2
                floatField: 23456.789e2
                intField: 10
                stringField: "paramDefaultValue"
                listBooleanField: [false]
                listEnumField: [ENUM_2]
                listFloatField: [23456.789e2]
                listIntField: [10]
                listStringField: ["paramDefaultValue"]
              })
            }""",
            None,
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:False]-[enumField:ENUM_2_2-MyEnum-enumField]-[floatField:2345681.9]-[intField:13]-[stringField:paramdefaultvalue-scalar-stringField]-[listBooleanField:False]-[listEnumField:enum_2_2-myenum]-[listFloatField:2345681.9]-[listIntField:13]-[listStringField:paramdefaultvalue-scalar]"
                }
            },
        ),
        (
            """
            query {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: false
                enumField: ENUM_2
                floatField: 23456.789e2
                intField: 10
                stringField: "paramDefaultValue"
                listBooleanField: [false, null]
                listEnumField: [ENUM_2, null]
                listFloatField: [23456.789e2, null]
                listIntField: [10, null]
                listStringField: ["paramDefaultValue", null]
              })
            }""",
            None,
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:False]-[enumField:ENUM_2_2-MyEnum-enumField]-[floatField:2345681.9]-[intField:13]-[stringField:paramdefaultvalue-scalar-stringField]-[listBooleanField:False-None]-[listEnumField:enum_2_2-myenum-None]-[listFloatField:2345681.9-None]-[listIntField:13-None]-[listStringField:paramdefaultvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: WrapperNonNullMyInput) { wrapperNonNullInputObjectWithDefaultField(param: $param) }""",
            None,
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_1_1-MyEnum-enumField]-[floatField:12345681.9]-[intField:123459]-[stringField:defaultstring-scalar-stringField]-[listBooleanField:True-None]-[listEnumField:enum_1_1-myenum-None]-[listFloatField:12345681.9-None]-[listIntField:123459-None]-[listStringField:defaultstring-scalar-None]"
                }
            },
        ),
        (
            """query ($param: WrapperNonNullMyInput) { wrapperNonNullInputObjectWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-None"
                }
            },
        ),
        (
            """query ($param: WrapperNonNullMyInput) { wrapperNonNullInputObjectWithDefaultField(param: $param) }""",
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
            """query ($param: WrapperNonNullMyInput) { wrapperNonNullInputObjectWithDefaultField(param: $param) }""",
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
            """query ($param: WrapperNonNullMyInput) { wrapperNonNullInputObjectWithDefaultField(param: $param) }""",
            {
                "param": {
                    "booleanField": None,
                    "enumField": None,
                    "floatField": None,
                    "intField": None,
                    "stringField": None,
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
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < Boolean! > not to be null at value.booleanField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < MyEnum! > not to be null at value.enumField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < Float! > not to be null at value.floatField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < Int! > not to be null at value.intField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < String! > not to be null at value.stringField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                ],
            },
        ),
        (
            """query ($param: WrapperNonNullMyInput) { wrapperNonNullInputObjectWithDefaultField(param: $param) }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": True,
                    "listEnumField": "ENUM_3",
                    "listFloatField": 3456.789e2,
                    "listIntField": 20,
                    "listStringField": "varValue",
                }
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True]-[listEnumField:enum_3_3-myenum]-[listFloatField:345681.9]-[listIntField:23]-[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: WrapperNonNullMyInput) { wrapperNonNullInputObjectWithDefaultField(param: $param) }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True],
                    "listEnumField": ["ENUM_3"],
                    "listFloatField": [3456.789e2],
                    "listIntField": [20],
                    "listStringField": ["varValue"],
                }
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True]-[listEnumField:enum_3_3-myenum]-[listFloatField:345681.9]-[listIntField:23]-[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: WrapperNonNullMyInput) { wrapperNonNullInputObjectWithDefaultField(param: $param) }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True, None],
                    "listEnumField": ["ENUM_3", None],
                    "listFloatField": [3456.789e2, None],
                    "listIntField": [20, None],
                    "listStringField": ["varValue", None],
                }
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True-None]-[listEnumField:enum_3_3-myenum-None]-[listFloatField:345681.9-None]-[listIntField:23-None]-[listStringField:varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: WrapperNonNullMyInput = null) { wrapperNonNullInputObjectWithDefaultField(param: $param) }""",
            None,
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-None"
                }
            },
        ),
        (
            """query ($param: WrapperNonNullMyInput = null) { wrapperNonNullInputObjectWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-None"
                }
            },
        ),
        (
            """query ($param: WrapperNonNullMyInput = null) { wrapperNonNullInputObjectWithDefaultField(param: $param) }""",
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
            """query ($param: WrapperNonNullMyInput = null) { wrapperNonNullInputObjectWithDefaultField(param: $param) }""",
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
            """query ($param: WrapperNonNullMyInput = null) { wrapperNonNullInputObjectWithDefaultField(param: $param) }""",
            {
                "param": {
                    "booleanField": None,
                    "enumField": None,
                    "floatField": None,
                    "intField": None,
                    "stringField": None,
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
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < Boolean! > not to be null at value.booleanField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < MyEnum! > not to be null at value.enumField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < Float! > not to be null at value.floatField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < Int! > not to be null at value.intField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < String! > not to be null at value.stringField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                ],
            },
        ),
        (
            """query ($param: WrapperNonNullMyInput = null) { wrapperNonNullInputObjectWithDefaultField(param: $param) }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": True,
                    "listEnumField": "ENUM_3",
                    "listFloatField": 3456.789e2,
                    "listIntField": 20,
                    "listStringField": "varValue",
                }
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True]-[listEnumField:enum_3_3-myenum]-[listFloatField:345681.9]-[listIntField:23]-[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: WrapperNonNullMyInput = null) { wrapperNonNullInputObjectWithDefaultField(param: $param) }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True],
                    "listEnumField": ["ENUM_3"],
                    "listFloatField": [3456.789e2],
                    "listIntField": [20],
                    "listStringField": ["varValue"],
                }
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True]-[listEnumField:enum_3_3-myenum]-[listFloatField:345681.9]-[listIntField:23]-[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: WrapperNonNullMyInput = null) { wrapperNonNullInputObjectWithDefaultField(param: $param) }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True, None],
                    "listEnumField": ["ENUM_3", None],
                    "listFloatField": [3456.789e2, None],
                    "listIntField": [20, None],
                    "listStringField": ["varValue", None],
                }
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True-None]-[listEnumField:enum_3_3-myenum-None]-[listFloatField:345681.9-None]-[listIntField:23-None]-[listStringField:varvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: null
                listEnumField: null
                listFloatField: null
                listIntField: null
                listStringField: null
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 3, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 28}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 5, "column": 29}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 6, "column": 27}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < String! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 7, "column": 30}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Boolean]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 8, "column": 35}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [MyEnum]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 9, "column": 32}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Float]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 10, "column": 33}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Int]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 11, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [String]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 12, "column": 34}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: null
                listEnumField: null
                listFloatField: null
                listIntField: null
                listStringField: null
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 3, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 28}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 5, "column": 29}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 6, "column": 27}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < String! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 7, "column": 30}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Boolean]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 8, "column": 35}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [MyEnum]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 9, "column": 32}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Float]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 10, "column": 33}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Int]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 11, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [String]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 12, "column": 34}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: null
                listEnumField: null
                listFloatField: null
                listIntField: null
                listStringField: null
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {"param": {}},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 3, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 28}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 5, "column": 29}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 6, "column": 27}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < String! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 7, "column": 30}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Boolean]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 8, "column": 35}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [MyEnum]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 9, "column": 32}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Float]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 10, "column": 33}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Int]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 11, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [String]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 12, "column": 34}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: null
                listEnumField: null
                listFloatField: null
                listIntField: null
                listStringField: null
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
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
                        "message": "Expected value of type < Boolean! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 3, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 28}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 5, "column": 29}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 6, "column": 27}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < String! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 7, "column": 30}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Boolean]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 8, "column": 35}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [MyEnum]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 9, "column": 32}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Float]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 10, "column": 33}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Int]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 11, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [String]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 12, "column": 34}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: null
                listEnumField: null
                listFloatField: null
                listIntField: null
                listStringField: null
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": None,
                    "enumField": None,
                    "floatField": None,
                    "intField": None,
                    "stringField": None,
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
                        "message": "Expected value of type < Boolean! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 3, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 28}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 5, "column": 29}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 6, "column": 27}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < String! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 7, "column": 30}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Boolean]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 8, "column": 35}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [MyEnum]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 9, "column": 32}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Float]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 10, "column": 33}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Int]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 11, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [String]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 12, "column": 34}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: null
                listEnumField: null
                listFloatField: null
                listIntField: null
                listStringField: null
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": True,
                    "listEnumField": "ENUM_3",
                    "listFloatField": 3456.789e2,
                    "listIntField": 20,
                    "listStringField": "varValue",
                }
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 3, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 28}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 5, "column": 29}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 6, "column": 27}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < String! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 7, "column": 30}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Boolean]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 8, "column": 35}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [MyEnum]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 9, "column": 32}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Float]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 10, "column": 33}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Int]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 11, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [String]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 12, "column": 34}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: null
                listEnumField: null
                listFloatField: null
                listIntField: null
                listStringField: null
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True],
                    "listEnumField": ["ENUM_3"],
                    "listFloatField": [3456.789e2],
                    "listIntField": [20],
                    "listStringField": ["varValue"],
                }
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 3, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 28}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 5, "column": 29}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 6, "column": 27}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < String! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 7, "column": 30}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Boolean]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 8, "column": 35}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [MyEnum]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 9, "column": 32}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Float]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 10, "column": 33}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Int]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 11, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [String]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 12, "column": 34}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: null
                listEnumField: null
                listFloatField: null
                listIntField: null
                listStringField: null
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True, None],
                    "listEnumField": ["ENUM_3", None],
                    "listFloatField": [3456.789e2, None],
                    "listIntField": [20, None],
                    "listStringField": ["varValue", None],
                }
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 3, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 28}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 5, "column": 29}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 6, "column": 27}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < String! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 7, "column": 30}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Boolean]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 8, "column": 35}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [MyEnum]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 9, "column": 32}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Float]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 10, "column": 33}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [Int]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 11, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < [String]! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 12, "column": 34}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: [null]
                listEnumField: [null]
                listFloatField: [null]
                listIntField: [null]
                listStringField: [null]
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 3, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 28}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 5, "column": 29}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 6, "column": 27}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < String! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 7, "column": 30}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: [null]
                listEnumField: [null]
                listFloatField: [null]
                listIntField: [null]
                listStringField: [null]
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 3, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 28}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 5, "column": 29}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 6, "column": 27}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < String! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 7, "column": 30}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: [null]
                listEnumField: [null]
                listFloatField: [null]
                listIntField: [null]
                listStringField: [null]
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {"param": {}},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 3, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 28}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 5, "column": 29}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 6, "column": 27}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < String! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 7, "column": 30}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: [null]
                listEnumField: [null]
                listFloatField: [null]
                listIntField: [null]
                listStringField: [null]
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
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
                        "message": "Expected value of type < Boolean! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 3, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 28}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 5, "column": 29}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 6, "column": 27}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < String! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 7, "column": 30}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: [null]
                listEnumField: [null]
                listFloatField: [null]
                listIntField: [null]
                listStringField: [null]
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": None,
                    "enumField": None,
                    "floatField": None,
                    "intField": None,
                    "stringField": None,
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
                        "message": "Expected value of type < Boolean! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 3, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 28}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 5, "column": 29}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 6, "column": 27}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < String! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 7, "column": 30}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: [null]
                listEnumField: [null]
                listFloatField: [null]
                listIntField: [null]
                listStringField: [null]
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": True,
                    "listEnumField": "ENUM_3",
                    "listFloatField": 3456.789e2,
                    "listIntField": 20,
                    "listStringField": "varValue",
                }
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 3, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 28}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 5, "column": 29}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 6, "column": 27}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < String! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 7, "column": 30}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: [null]
                listEnumField: [null]
                listFloatField: [null]
                listIntField: [null]
                listStringField: [null]
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True],
                    "listEnumField": ["ENUM_3"],
                    "listFloatField": [3456.789e2],
                    "listIntField": [20],
                    "listStringField": ["varValue"],
                }
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 3, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 28}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 5, "column": 29}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 6, "column": 27}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < String! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 7, "column": 30}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: null
                enumField: null
                floatField: null
                intField: null
                stringField: null
                listBooleanField: [null]
                listEnumField: [null]
                listFloatField: [null]
                listIntField: [null]
                listStringField: [null]
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True, None],
                    "listEnumField": ["ENUM_3", None],
                    "listFloatField": [3456.789e2, None],
                    "listIntField": [20, None],
                    "listStringField": ["varValue", None],
                }
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 3, "column": 31}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 28}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 5, "column": 29}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 6, "column": 27}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                    {
                        "message": "Expected value of type < String! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 7, "column": 30}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.1",
                            "tag": "values-of-correct-type",
                            "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: false
                listEnumField: ENUM_4
                listFloatField: 456.789e2
                listIntField: 30
                listStringField: "varDefault"
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            None,
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:False]-[enumField:ENUM_4_4-MyEnum-enumField]-[floatField:45681.9]-[intField:33]-[stringField:vardefault-scalar-stringField]-[listBooleanField:False]-[listEnumField:enum_4_4-myenum]-[listFloatField:45681.9]-[listIntField:33]-[listStringField:vardefault-scalar]"
                }
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: false
                listEnumField: ENUM_4
                listFloatField: 456.789e2
                listIntField: 30
                listStringField: "varDefault"
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {"param": None},
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-None"
                }
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: false
                listEnumField: ENUM_4
                listFloatField: 456.789e2
                listIntField: 30
                listStringField: "varDefault"
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {"param": {}},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.booleanField > of required type < Boolean! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.enumField > of required type < MyEnum! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.floatField > of required type < Float! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.intField > of required type < Int! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.stringField > of required type < String! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.listBooleanField > of required type < [Boolean]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.listEnumField > of required type < [MyEnum]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.listFloatField > of required type < [Float]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.listIntField > of required type < [Int]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.listStringField > of required type < [String]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: false
                listEnumField: ENUM_4
                listFloatField: 456.789e2
                listIntField: 30
                listStringField: "varDefault"
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
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
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < MyEnum! > not to be null at value.enumField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < Float! > not to be null at value.floatField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < Int! > not to be null at value.intField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < String! > not to be null at value.stringField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < [Boolean]! > not to be null at value.listBooleanField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < [MyEnum]! > not to be null at value.listEnumField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < [Float]! > not to be null at value.listFloatField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < [Int]! > not to be null at value.listIntField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < [String]! > not to be null at value.listStringField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: false
                listEnumField: ENUM_4
                listFloatField: 456.789e2
                listIntField: 30
                listStringField: "varDefault"
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": None,
                    "enumField": None,
                    "floatField": None,
                    "intField": None,
                    "stringField": None,
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
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < Boolean! > not to be null at value.booleanField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < MyEnum! > not to be null at value.enumField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < Float! > not to be null at value.floatField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < Int! > not to be null at value.intField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < String! > not to be null at value.stringField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: false
                listEnumField: ENUM_4
                listFloatField: 456.789e2
                listIntField: 30
                listStringField: "varDefault"
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": True,
                    "listEnumField": "ENUM_3",
                    "listFloatField": 3456.789e2,
                    "listIntField": 20,
                    "listStringField": "varValue",
                }
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True]-[listEnumField:enum_3_3-myenum]-[listFloatField:345681.9]-[listIntField:23]-[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: false
                listEnumField: ENUM_4
                listFloatField: 456.789e2
                listIntField: 30
                listStringField: "varDefault"
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True],
                    "listEnumField": ["ENUM_3"],
                    "listFloatField": [3456.789e2],
                    "listIntField": [20],
                    "listStringField": ["varValue"],
                }
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True]-[listEnumField:enum_3_3-myenum]-[listFloatField:345681.9]-[listIntField:23]-[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: false
                listEnumField: ENUM_4
                listFloatField: 456.789e2
                listIntField: 30
                listStringField: "varDefault"
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True, None],
                    "listEnumField": ["ENUM_3", None],
                    "listFloatField": [3456.789e2, None],
                    "listIntField": [20, None],
                    "listStringField": ["varValue", None],
                }
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True-None]-[listEnumField:enum_3_3-myenum-None]-[listFloatField:345681.9-None]-[listIntField:23-None]-[listStringField:varvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false]
                listEnumField: [ENUM_4]
                listFloatField: [456.789e2]
                listIntField: [30]
                listStringField: ["varDefault"]
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            None,
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:False]-[enumField:ENUM_4_4-MyEnum-enumField]-[floatField:45681.9]-[intField:33]-[stringField:vardefault-scalar-stringField]-[listBooleanField:False]-[listEnumField:enum_4_4-myenum]-[listFloatField:45681.9]-[listIntField:33]-[listStringField:vardefault-scalar]"
                }
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false]
                listEnumField: [ENUM_4]
                listFloatField: [456.789e2]
                listIntField: [30]
                listStringField: ["varDefault"]
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {"param": None},
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-None"
                }
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false]
                listEnumField: [ENUM_4]
                listFloatField: [456.789e2]
                listIntField: [30]
                listStringField: ["varDefault"]
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {"param": {}},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.booleanField > of required type < Boolean! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.enumField > of required type < MyEnum! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.floatField > of required type < Float! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.intField > of required type < Int! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.stringField > of required type < String! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.listBooleanField > of required type < [Boolean]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.listEnumField > of required type < [MyEnum]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.listFloatField > of required type < [Float]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.listIntField > of required type < [Int]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.listStringField > of required type < [String]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false]
                listEnumField: [ENUM_4]
                listFloatField: [456.789e2]
                listIntField: [30]
                listStringField: ["varDefault"]
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
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
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < MyEnum! > not to be null at value.enumField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < Float! > not to be null at value.floatField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < Int! > not to be null at value.intField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < String! > not to be null at value.stringField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < [Boolean]! > not to be null at value.listBooleanField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < [MyEnum]! > not to be null at value.listEnumField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < [Float]! > not to be null at value.listFloatField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < [Int]! > not to be null at value.listIntField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < [String]! > not to be null at value.listStringField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false]
                listEnumField: [ENUM_4]
                listFloatField: [456.789e2]
                listIntField: [30]
                listStringField: ["varDefault"]
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": None,
                    "enumField": None,
                    "floatField": None,
                    "intField": None,
                    "stringField": None,
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
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < Boolean! > not to be null at value.booleanField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < MyEnum! > not to be null at value.enumField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < Float! > not to be null at value.floatField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < Int! > not to be null at value.intField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < String! > not to be null at value.stringField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false]
                listEnumField: [ENUM_4]
                listFloatField: [456.789e2]
                listIntField: [30]
                listStringField: ["varDefault"]
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": True,
                    "listEnumField": "ENUM_3",
                    "listFloatField": 3456.789e2,
                    "listIntField": 20,
                    "listStringField": "varValue",
                }
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True]-[listEnumField:enum_3_3-myenum]-[listFloatField:345681.9]-[listIntField:23]-[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false]
                listEnumField: [ENUM_4]
                listFloatField: [456.789e2]
                listIntField: [30]
                listStringField: ["varDefault"]
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True],
                    "listEnumField": ["ENUM_3"],
                    "listFloatField": [3456.789e2],
                    "listIntField": [20],
                    "listStringField": ["varValue"],
                }
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True]-[listEnumField:enum_3_3-myenum]-[listFloatField:345681.9]-[listIntField:23]-[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false]
                listEnumField: [ENUM_4]
                listFloatField: [456.789e2]
                listIntField: [30]
                listStringField: ["varDefault"]
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True, None],
                    "listEnumField": ["ENUM_3", None],
                    "listFloatField": [3456.789e2, None],
                    "listIntField": [20, None],
                    "listStringField": ["varValue", None],
                }
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True-None]-[listEnumField:enum_3_3-myenum-None]-[listFloatField:345681.9-None]-[listIntField:23-None]-[listStringField:varvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false, null]
                listEnumField: [ENUM_4, null]
                listFloatField: [456.789e2, null]
                listIntField: [30, null]
                listStringField: ["varDefault", null]
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            None,
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:False]-[enumField:ENUM_4_4-MyEnum-enumField]-[floatField:45681.9]-[intField:33]-[stringField:vardefault-scalar-stringField]-[listBooleanField:False-None]-[listEnumField:enum_4_4-myenum-None]-[listFloatField:45681.9-None]-[listIntField:33-None]-[listStringField:vardefault-scalar-None]"
                }
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false, null]
                listEnumField: [ENUM_4, null]
                listFloatField: [456.789e2, null]
                listIntField: [30, null]
                listStringField: ["varDefault", null]
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {"param": None},
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-None"
                }
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false, null]
                listEnumField: [ENUM_4, null]
                listFloatField: [456.789e2, null]
                listIntField: [30, null]
                listStringField: ["varDefault", null]
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {"param": {}},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.booleanField > of required type < Boolean! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.enumField > of required type < MyEnum! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.floatField > of required type < Float! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.intField > of required type < Int! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.stringField > of required type < String! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.listBooleanField > of required type < [Boolean]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.listEnumField > of required type < [MyEnum]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.listFloatField > of required type < [Float]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.listIntField > of required type < [Int]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {} >; Field < value.listStringField > of required type < [String]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false, null]
                listEnumField: [ENUM_4, null]
                listFloatField: [456.789e2, null]
                listIntField: [30, null]
                listStringField: ["varDefault", null]
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
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
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < MyEnum! > not to be null at value.enumField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < Float! > not to be null at value.floatField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < Int! > not to be null at value.intField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < String! > not to be null at value.stringField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < [Boolean]! > not to be null at value.listBooleanField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < [MyEnum]! > not to be null at value.listEnumField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < [Float]! > not to be null at value.listFloatField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < [Int]! > not to be null at value.listIntField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': None, 'listEnumField': None, 'listFloatField': None, 'listIntField': None, 'listStringField': None} >; Expected non-nullable type < [String]! > not to be null at value.listStringField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false, null]
                listEnumField: [ENUM_4, null]
                listFloatField: [456.789e2, null]
                listIntField: [30, null]
                listStringField: ["varDefault", null]
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": None,
                    "enumField": None,
                    "floatField": None,
                    "intField": None,
                    "stringField": None,
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
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < Boolean! > not to be null at value.booleanField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < MyEnum! > not to be null at value.enumField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < Float! > not to be null at value.floatField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < Int! > not to be null at value.intField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < String! > not to be null at value.stringField.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false, null]
                listEnumField: [ENUM_4, null]
                listFloatField: [456.789e2, null]
                listIntField: [30, null]
                listStringField: ["varDefault", null]
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": True,
                    "listEnumField": "ENUM_3",
                    "listFloatField": 3456.789e2,
                    "listIntField": 20,
                    "listStringField": "varValue",
                }
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True]-[listEnumField:enum_3_3-myenum]-[listFloatField:345681.9]-[listIntField:23]-[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false, null]
                listEnumField: [ENUM_4, null]
                listFloatField: [456.789e2, null]
                listIntField: [30, null]
                listStringField: ["varDefault", null]
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True],
                    "listEnumField": ["ENUM_3"],
                    "listFloatField": [3456.789e2],
                    "listIntField": [20],
                    "listStringField": ["varValue"],
                }
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True]-[listEnumField:enum_3_3-myenum]-[listFloatField:345681.9]-[listIntField:23]-[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $param: WrapperNonNullMyInput = {
                booleanField: false
                enumField: ENUM_4
                floatField: 456.789e2
                intField: 30
                stringField: "varDefault"
                listBooleanField: [false, null]
                listEnumField: [ENUM_4, null]
                listFloatField: [456.789e2, null]
                listIntField: [30, null]
                listStringField: ["varDefault", null]
              }
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: $param)
            }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True, None],
                    "listEnumField": ["ENUM_3", None],
                    "listFloatField": [3456.789e2, None],
                    "listIntField": [20, None],
                    "listStringField": ["varValue", None],
                }
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True-None]-[listEnumField:enum_3_3-myenum-None]-[listFloatField:345681.9-None]-[listIntField:23-None]-[listStringField:varvalue-scalar-None]"
                }
            },
        ),
        (
            """query ($param: WrapperNonNullMyInput!) { wrapperNonNullInputObjectWithDefaultField(param: $param) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of required type < WrapperNonNullMyInput! > was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: WrapperNonNullMyInput!) { wrapperNonNullInputObjectWithDefaultField(param: $param) }""",
            {"param": None},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $param > of non-null type < WrapperNonNullMyInput! > must not be null.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    }
                ],
            },
        ),
        (
            """query ($param: WrapperNonNullMyInput!) { wrapperNonNullInputObjectWithDefaultField(param: $param) }""",
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
            """query ($param: WrapperNonNullMyInput!) { wrapperNonNullInputObjectWithDefaultField(param: $param) }""",
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
            """query ($param: WrapperNonNullMyInput!) { wrapperNonNullInputObjectWithDefaultField(param: $param) }""",
            {
                "param": {
                    "booleanField": None,
                    "enumField": None,
                    "floatField": None,
                    "intField": None,
                    "stringField": None,
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
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < Boolean! > not to be null at value.booleanField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < MyEnum! > not to be null at value.enumField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < Float! > not to be null at value.floatField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < Int! > not to be null at value.intField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Variable < $param > got invalid value < {'booleanField': None, 'enumField': None, 'floatField': None, 'intField': None, 'stringField': None, 'listBooleanField': [None], 'listEnumField': [None], 'listFloatField': [None], 'listIntField': [None], 'listStringField': [None]} >; Expected non-nullable type < String! > not to be null at value.stringField.",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                ],
            },
        ),
        (
            """query ($param: WrapperNonNullMyInput!) { wrapperNonNullInputObjectWithDefaultField(param: $param) }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": True,
                    "listEnumField": "ENUM_3",
                    "listFloatField": 3456.789e2,
                    "listIntField": 20,
                    "listStringField": "varValue",
                }
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True]-[listEnumField:enum_3_3-myenum]-[listFloatField:345681.9]-[listIntField:23]-[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: WrapperNonNullMyInput!) { wrapperNonNullInputObjectWithDefaultField(param: $param) }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True],
                    "listEnumField": ["ENUM_3"],
                    "listFloatField": [3456.789e2],
                    "listIntField": [20],
                    "listStringField": ["varValue"],
                }
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True]-[listEnumField:enum_3_3-myenum]-[listFloatField:345681.9]-[listIntField:23]-[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query ($param: WrapperNonNullMyInput!) { wrapperNonNullInputObjectWithDefaultField(param: $param) }""",
            {
                "param": {
                    "booleanField": True,
                    "enumField": "ENUM_3",
                    "floatField": 3456.789e2,
                    "intField": 20,
                    "stringField": "varValue",
                    "listBooleanField": [True, None],
                    "listEnumField": ["ENUM_3", None],
                    "listFloatField": [3456.789e2, None],
                    "listIntField": [20, None],
                    "listStringField": ["varValue", None],
                }
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True-None]-[listEnumField:enum_3_3-myenum-None]-[listFloatField:345681.9-None]-[listIntField:23-None]-[listStringField:varvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean
              $enumField: MyEnum
              $floatField: Float
              $intField: Int
              $stringField: String
              $listBooleanField: [Boolean]
              $listEnumField: [MyEnum]
              $listFloatField: [Float]
              $listIntField: [Int]
              $listStringField: [String]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 14, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $enumField > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 15},
                            {"line": 15, "column": 28},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $floatField > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 15},
                            {"line": 16, "column": 29},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $intField > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 15},
                            {"line": 17, "column": 27},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $stringField > of type < String > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 15},
                            {"line": 18, "column": 30},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listBooleanField > of type < [Boolean] > used in position expecting type < [Boolean]! >.",
                        "path": None,
                        "locations": [
                            {"line": 7, "column": 15},
                            {"line": 19, "column": 35},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listEnumField > of type < [MyEnum] > used in position expecting type < [MyEnum]! >.",
                        "path": None,
                        "locations": [
                            {"line": 8, "column": 15},
                            {"line": 20, "column": 32},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listFloatField > of type < [Float] > used in position expecting type < [Float]! >.",
                        "path": None,
                        "locations": [
                            {"line": 9, "column": 15},
                            {"line": 21, "column": 33},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listIntField > of type < [Int] > used in position expecting type < [Int]! >.",
                        "path": None,
                        "locations": [
                            {"line": 10, "column": 15},
                            {"line": 22, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listStringField > of type < [String] > used in position expecting type < [String]! >.",
                        "path": None,
                        "locations": [
                            {"line": 11, "column": 15},
                            {"line": 23, "column": 34},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean
              $enumField: MyEnum
              $floatField: Float
              $intField: Int
              $stringField: String
              $listBooleanField: [Boolean]
              $listEnumField: [MyEnum]
              $listFloatField: [Float]
              $listIntField: [Int]
              $listStringField: [String]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
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
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 14, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $enumField > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 15},
                            {"line": 15, "column": 28},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $floatField > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 15},
                            {"line": 16, "column": 29},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $intField > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 15},
                            {"line": 17, "column": 27},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $stringField > of type < String > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 15},
                            {"line": 18, "column": 30},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listBooleanField > of type < [Boolean] > used in position expecting type < [Boolean]! >.",
                        "path": None,
                        "locations": [
                            {"line": 7, "column": 15},
                            {"line": 19, "column": 35},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listEnumField > of type < [MyEnum] > used in position expecting type < [MyEnum]! >.",
                        "path": None,
                        "locations": [
                            {"line": 8, "column": 15},
                            {"line": 20, "column": 32},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listFloatField > of type < [Float] > used in position expecting type < [Float]! >.",
                        "path": None,
                        "locations": [
                            {"line": 9, "column": 15},
                            {"line": 21, "column": 33},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listIntField > of type < [Int] > used in position expecting type < [Int]! >.",
                        "path": None,
                        "locations": [
                            {"line": 10, "column": 15},
                            {"line": 22, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listStringField > of type < [String] > used in position expecting type < [String]! >.",
                        "path": None,
                        "locations": [
                            {"line": 11, "column": 15},
                            {"line": 23, "column": 34},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean
              $enumField: MyEnum
              $floatField: Float
              $intField: Int
              $stringField: String
              $listBooleanField: [Boolean]
              $listEnumField: [MyEnum]
              $listFloatField: [Float]
              $listIntField: [Int]
              $listStringField: [String]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": [None],
                "listEnumField": [None],
                "listFloatField": [None],
                "listIntField": [None],
                "listStringField": [None],
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 14, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $enumField > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 15},
                            {"line": 15, "column": 28},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $floatField > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 15},
                            {"line": 16, "column": 29},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $intField > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 15},
                            {"line": 17, "column": 27},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $stringField > of type < String > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 15},
                            {"line": 18, "column": 30},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listBooleanField > of type < [Boolean] > used in position expecting type < [Boolean]! >.",
                        "path": None,
                        "locations": [
                            {"line": 7, "column": 15},
                            {"line": 19, "column": 35},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listEnumField > of type < [MyEnum] > used in position expecting type < [MyEnum]! >.",
                        "path": None,
                        "locations": [
                            {"line": 8, "column": 15},
                            {"line": 20, "column": 32},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listFloatField > of type < [Float] > used in position expecting type < [Float]! >.",
                        "path": None,
                        "locations": [
                            {"line": 9, "column": 15},
                            {"line": 21, "column": 33},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listIntField > of type < [Int] > used in position expecting type < [Int]! >.",
                        "path": None,
                        "locations": [
                            {"line": 10, "column": 15},
                            {"line": 22, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listStringField > of type < [String] > used in position expecting type < [String]! >.",
                        "path": None,
                        "locations": [
                            {"line": 11, "column": 15},
                            {"line": 23, "column": 34},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean
              $enumField: MyEnum
              $floatField: Float
              $intField: Int
              $stringField: String
              $listBooleanField: [Boolean]
              $listEnumField: [MyEnum]
              $listFloatField: [Float]
              $listIntField: [Int]
              $listStringField: [String]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": True,
                "listEnumField": "ENUM_3",
                "listFloatField": 3456.789e2,
                "listIntField": 20,
                "listStringField": "varValue",
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 14, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $enumField > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 15},
                            {"line": 15, "column": 28},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $floatField > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 15},
                            {"line": 16, "column": 29},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $intField > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 15},
                            {"line": 17, "column": 27},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $stringField > of type < String > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 15},
                            {"line": 18, "column": 30},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listBooleanField > of type < [Boolean] > used in position expecting type < [Boolean]! >.",
                        "path": None,
                        "locations": [
                            {"line": 7, "column": 15},
                            {"line": 19, "column": 35},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listEnumField > of type < [MyEnum] > used in position expecting type < [MyEnum]! >.",
                        "path": None,
                        "locations": [
                            {"line": 8, "column": 15},
                            {"line": 20, "column": 32},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listFloatField > of type < [Float] > used in position expecting type < [Float]! >.",
                        "path": None,
                        "locations": [
                            {"line": 9, "column": 15},
                            {"line": 21, "column": 33},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listIntField > of type < [Int] > used in position expecting type < [Int]! >.",
                        "path": None,
                        "locations": [
                            {"line": 10, "column": 15},
                            {"line": 22, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listStringField > of type < [String] > used in position expecting type < [String]! >.",
                        "path": None,
                        "locations": [
                            {"line": 11, "column": 15},
                            {"line": 23, "column": 34},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean
              $enumField: MyEnum
              $floatField: Float
              $intField: Int
              $stringField: String
              $listBooleanField: [Boolean]
              $listEnumField: [MyEnum]
              $listFloatField: [Float]
              $listIntField: [Int]
              $listStringField: [String]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True],
                "listEnumField": ["ENUM_3"],
                "listFloatField": [3456.789e2],
                "listIntField": [20],
                "listStringField": ["varValue"],
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 14, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $enumField > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 15},
                            {"line": 15, "column": 28},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $floatField > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 15},
                            {"line": 16, "column": 29},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $intField > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 15},
                            {"line": 17, "column": 27},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $stringField > of type < String > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 15},
                            {"line": 18, "column": 30},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listBooleanField > of type < [Boolean] > used in position expecting type < [Boolean]! >.",
                        "path": None,
                        "locations": [
                            {"line": 7, "column": 15},
                            {"line": 19, "column": 35},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listEnumField > of type < [MyEnum] > used in position expecting type < [MyEnum]! >.",
                        "path": None,
                        "locations": [
                            {"line": 8, "column": 15},
                            {"line": 20, "column": 32},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listFloatField > of type < [Float] > used in position expecting type < [Float]! >.",
                        "path": None,
                        "locations": [
                            {"line": 9, "column": 15},
                            {"line": 21, "column": 33},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listIntField > of type < [Int] > used in position expecting type < [Int]! >.",
                        "path": None,
                        "locations": [
                            {"line": 10, "column": 15},
                            {"line": 22, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listStringField > of type < [String] > used in position expecting type < [String]! >.",
                        "path": None,
                        "locations": [
                            {"line": 11, "column": 15},
                            {"line": 23, "column": 34},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean
              $enumField: MyEnum
              $floatField: Float
              $intField: Int
              $stringField: String
              $listBooleanField: [Boolean]
              $listEnumField: [MyEnum]
              $listFloatField: [Float]
              $listIntField: [Int]
              $listStringField: [String]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True, None],
                "listEnumField": ["ENUM_3", None],
                "listFloatField": [3456.789e2, None],
                "listIntField": [20, None],
                "listStringField": ["varValue", None],
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 14, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $enumField > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 15},
                            {"line": 15, "column": 28},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $floatField > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 15},
                            {"line": 16, "column": 29},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $intField > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 15},
                            {"line": 17, "column": 27},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $stringField > of type < String > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 15},
                            {"line": 18, "column": 30},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listBooleanField > of type < [Boolean] > used in position expecting type < [Boolean]! >.",
                        "path": None,
                        "locations": [
                            {"line": 7, "column": 15},
                            {"line": 19, "column": 35},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listEnumField > of type < [MyEnum] > used in position expecting type < [MyEnum]! >.",
                        "path": None,
                        "locations": [
                            {"line": 8, "column": 15},
                            {"line": 20, "column": 32},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listFloatField > of type < [Float] > used in position expecting type < [Float]! >.",
                        "path": None,
                        "locations": [
                            {"line": 9, "column": 15},
                            {"line": 21, "column": 33},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listIntField > of type < [Int] > used in position expecting type < [Int]! >.",
                        "path": None,
                        "locations": [
                            {"line": 10, "column": 15},
                            {"line": 22, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listStringField > of type < [String] > used in position expecting type < [String]! >.",
                        "path": None,
                        "locations": [
                            {"line": 11, "column": 15},
                            {"line": 23, "column": 34},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $listBooleanField: [Boolean] = null
              $listEnumField: [MyEnum] = null
              $listFloatField: [Float] = null
              $listIntField: [Int] = null
              $listStringField: [String] = null
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 14, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $enumField > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 15},
                            {"line": 15, "column": 28},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $floatField > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 15},
                            {"line": 16, "column": 29},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $intField > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 15},
                            {"line": 17, "column": 27},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $stringField > of type < String > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 15},
                            {"line": 18, "column": 30},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listBooleanField > of type < [Boolean] > used in position expecting type < [Boolean]! >.",
                        "path": None,
                        "locations": [
                            {"line": 7, "column": 15},
                            {"line": 19, "column": 35},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listEnumField > of type < [MyEnum] > used in position expecting type < [MyEnum]! >.",
                        "path": None,
                        "locations": [
                            {"line": 8, "column": 15},
                            {"line": 20, "column": 32},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listFloatField > of type < [Float] > used in position expecting type < [Float]! >.",
                        "path": None,
                        "locations": [
                            {"line": 9, "column": 15},
                            {"line": 21, "column": 33},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listIntField > of type < [Int] > used in position expecting type < [Int]! >.",
                        "path": None,
                        "locations": [
                            {"line": 10, "column": 15},
                            {"line": 22, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listStringField > of type < [String] > used in position expecting type < [String]! >.",
                        "path": None,
                        "locations": [
                            {"line": 11, "column": 15},
                            {"line": 23, "column": 34},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $listBooleanField: [Boolean] = null
              $listEnumField: [MyEnum] = null
              $listFloatField: [Float] = null
              $listIntField: [Int] = null
              $listStringField: [String] = null
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
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
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 14, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $enumField > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 15},
                            {"line": 15, "column": 28},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $floatField > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 15},
                            {"line": 16, "column": 29},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $intField > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 15},
                            {"line": 17, "column": 27},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $stringField > of type < String > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 15},
                            {"line": 18, "column": 30},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listBooleanField > of type < [Boolean] > used in position expecting type < [Boolean]! >.",
                        "path": None,
                        "locations": [
                            {"line": 7, "column": 15},
                            {"line": 19, "column": 35},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listEnumField > of type < [MyEnum] > used in position expecting type < [MyEnum]! >.",
                        "path": None,
                        "locations": [
                            {"line": 8, "column": 15},
                            {"line": 20, "column": 32},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listFloatField > of type < [Float] > used in position expecting type < [Float]! >.",
                        "path": None,
                        "locations": [
                            {"line": 9, "column": 15},
                            {"line": 21, "column": 33},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listIntField > of type < [Int] > used in position expecting type < [Int]! >.",
                        "path": None,
                        "locations": [
                            {"line": 10, "column": 15},
                            {"line": 22, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listStringField > of type < [String] > used in position expecting type < [String]! >.",
                        "path": None,
                        "locations": [
                            {"line": 11, "column": 15},
                            {"line": 23, "column": 34},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $listBooleanField: [Boolean] = null
              $listEnumField: [MyEnum] = null
              $listFloatField: [Float] = null
              $listIntField: [Int] = null
              $listStringField: [String] = null
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": [None],
                "listEnumField": [None],
                "listFloatField": [None],
                "listIntField": [None],
                "listStringField": [None],
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 14, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $enumField > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 15},
                            {"line": 15, "column": 28},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $floatField > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 15},
                            {"line": 16, "column": 29},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $intField > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 15},
                            {"line": 17, "column": 27},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $stringField > of type < String > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 15},
                            {"line": 18, "column": 30},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listBooleanField > of type < [Boolean] > used in position expecting type < [Boolean]! >.",
                        "path": None,
                        "locations": [
                            {"line": 7, "column": 15},
                            {"line": 19, "column": 35},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listEnumField > of type < [MyEnum] > used in position expecting type < [MyEnum]! >.",
                        "path": None,
                        "locations": [
                            {"line": 8, "column": 15},
                            {"line": 20, "column": 32},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listFloatField > of type < [Float] > used in position expecting type < [Float]! >.",
                        "path": None,
                        "locations": [
                            {"line": 9, "column": 15},
                            {"line": 21, "column": 33},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listIntField > of type < [Int] > used in position expecting type < [Int]! >.",
                        "path": None,
                        "locations": [
                            {"line": 10, "column": 15},
                            {"line": 22, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listStringField > of type < [String] > used in position expecting type < [String]! >.",
                        "path": None,
                        "locations": [
                            {"line": 11, "column": 15},
                            {"line": 23, "column": 34},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $listBooleanField: [Boolean] = null
              $listEnumField: [MyEnum] = null
              $listFloatField: [Float] = null
              $listIntField: [Int] = null
              $listStringField: [String] = null
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": True,
                "listEnumField": "ENUM_3",
                "listFloatField": 3456.789e2,
                "listIntField": 20,
                "listStringField": "varValue",
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 14, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $enumField > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 15},
                            {"line": 15, "column": 28},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $floatField > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 15},
                            {"line": 16, "column": 29},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $intField > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 15},
                            {"line": 17, "column": 27},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $stringField > of type < String > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 15},
                            {"line": 18, "column": 30},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listBooleanField > of type < [Boolean] > used in position expecting type < [Boolean]! >.",
                        "path": None,
                        "locations": [
                            {"line": 7, "column": 15},
                            {"line": 19, "column": 35},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listEnumField > of type < [MyEnum] > used in position expecting type < [MyEnum]! >.",
                        "path": None,
                        "locations": [
                            {"line": 8, "column": 15},
                            {"line": 20, "column": 32},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listFloatField > of type < [Float] > used in position expecting type < [Float]! >.",
                        "path": None,
                        "locations": [
                            {"line": 9, "column": 15},
                            {"line": 21, "column": 33},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listIntField > of type < [Int] > used in position expecting type < [Int]! >.",
                        "path": None,
                        "locations": [
                            {"line": 10, "column": 15},
                            {"line": 22, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listStringField > of type < [String] > used in position expecting type < [String]! >.",
                        "path": None,
                        "locations": [
                            {"line": 11, "column": 15},
                            {"line": 23, "column": 34},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $listBooleanField: [Boolean] = null
              $listEnumField: [MyEnum] = null
              $listFloatField: [Float] = null
              $listIntField: [Int] = null
              $listStringField: [String] = null
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True],
                "listEnumField": ["ENUM_3"],
                "listFloatField": [3456.789e2],
                "listIntField": [20],
                "listStringField": ["varValue"],
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 14, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $enumField > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 15},
                            {"line": 15, "column": 28},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $floatField > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 15},
                            {"line": 16, "column": 29},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $intField > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 15},
                            {"line": 17, "column": 27},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $stringField > of type < String > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 15},
                            {"line": 18, "column": 30},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listBooleanField > of type < [Boolean] > used in position expecting type < [Boolean]! >.",
                        "path": None,
                        "locations": [
                            {"line": 7, "column": 15},
                            {"line": 19, "column": 35},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listEnumField > of type < [MyEnum] > used in position expecting type < [MyEnum]! >.",
                        "path": None,
                        "locations": [
                            {"line": 8, "column": 15},
                            {"line": 20, "column": 32},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listFloatField > of type < [Float] > used in position expecting type < [Float]! >.",
                        "path": None,
                        "locations": [
                            {"line": 9, "column": 15},
                            {"line": 21, "column": 33},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listIntField > of type < [Int] > used in position expecting type < [Int]! >.",
                        "path": None,
                        "locations": [
                            {"line": 10, "column": 15},
                            {"line": 22, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listStringField > of type < [String] > used in position expecting type < [String]! >.",
                        "path": None,
                        "locations": [
                            {"line": 11, "column": 15},
                            {"line": 23, "column": 34},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $listBooleanField: [Boolean] = null
              $listEnumField: [MyEnum] = null
              $listFloatField: [Float] = null
              $listIntField: [Int] = null
              $listStringField: [String] = null
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True, None],
                "listEnumField": ["ENUM_3", None],
                "listFloatField": [3456.789e2, None],
                "listIntField": [20, None],
                "listStringField": ["varValue", None],
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 14, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $enumField > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 15},
                            {"line": 15, "column": 28},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $floatField > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 15},
                            {"line": 16, "column": 29},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $intField > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 15},
                            {"line": 17, "column": 27},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $stringField > of type < String > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 15},
                            {"line": 18, "column": 30},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listBooleanField > of type < [Boolean] > used in position expecting type < [Boolean]! >.",
                        "path": None,
                        "locations": [
                            {"line": 7, "column": 15},
                            {"line": 19, "column": 35},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listEnumField > of type < [MyEnum] > used in position expecting type < [MyEnum]! >.",
                        "path": None,
                        "locations": [
                            {"line": 8, "column": 15},
                            {"line": 20, "column": 32},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listFloatField > of type < [Float] > used in position expecting type < [Float]! >.",
                        "path": None,
                        "locations": [
                            {"line": 9, "column": 15},
                            {"line": 21, "column": 33},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listIntField > of type < [Int] > used in position expecting type < [Int]! >.",
                        "path": None,
                        "locations": [
                            {"line": 10, "column": 15},
                            {"line": 22, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listStringField > of type < [String] > used in position expecting type < [String]! >.",
                        "path": None,
                        "locations": [
                            {"line": 11, "column": 15},
                            {"line": 23, "column": 34},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $listBooleanField: [Boolean] = [null]
              $listEnumField: [MyEnum] = [null]
              $listFloatField: [Float] = [null]
              $listIntField: [Int] = [null]
              $listStringField: [String] = [null]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 14, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $enumField > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 15},
                            {"line": 15, "column": 28},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $floatField > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 15},
                            {"line": 16, "column": 29},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $intField > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 15},
                            {"line": 17, "column": 27},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $stringField > of type < String > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 15},
                            {"line": 18, "column": 30},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $listBooleanField: [Boolean] = [null]
              $listEnumField: [MyEnum] = [null]
              $listFloatField: [Float] = [null]
              $listIntField: [Int] = [null]
              $listStringField: [String] = [null]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
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
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 14, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $enumField > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 15},
                            {"line": 15, "column": 28},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $floatField > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 15},
                            {"line": 16, "column": 29},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $intField > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 15},
                            {"line": 17, "column": 27},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $stringField > of type < String > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 15},
                            {"line": 18, "column": 30},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $listBooleanField: [Boolean] = [null]
              $listEnumField: [MyEnum] = [null]
              $listFloatField: [Float] = [null]
              $listIntField: [Int] = [null]
              $listStringField: [String] = [null]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": [None],
                "listEnumField": [None],
                "listFloatField": [None],
                "listIntField": [None],
                "listStringField": [None],
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 14, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $enumField > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 15},
                            {"line": 15, "column": 28},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $floatField > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 15},
                            {"line": 16, "column": 29},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $intField > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 15},
                            {"line": 17, "column": 27},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $stringField > of type < String > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 15},
                            {"line": 18, "column": 30},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $listBooleanField: [Boolean] = [null]
              $listEnumField: [MyEnum] = [null]
              $listFloatField: [Float] = [null]
              $listIntField: [Int] = [null]
              $listStringField: [String] = [null]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": True,
                "listEnumField": "ENUM_3",
                "listFloatField": 3456.789e2,
                "listIntField": 20,
                "listStringField": "varValue",
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 14, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $enumField > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 15},
                            {"line": 15, "column": 28},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $floatField > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 15},
                            {"line": 16, "column": 29},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $intField > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 15},
                            {"line": 17, "column": 27},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $stringField > of type < String > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 15},
                            {"line": 18, "column": 30},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $listBooleanField: [Boolean] = [null]
              $listEnumField: [MyEnum] = [null]
              $listFloatField: [Float] = [null]
              $listIntField: [Int] = [null]
              $listStringField: [String] = [null]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True],
                "listEnumField": ["ENUM_3"],
                "listFloatField": [3456.789e2],
                "listIntField": [20],
                "listStringField": ["varValue"],
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 14, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $enumField > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 15},
                            {"line": 15, "column": 28},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $floatField > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 15},
                            {"line": 16, "column": 29},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $intField > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 15},
                            {"line": 17, "column": 27},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $stringField > of type < String > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 15},
                            {"line": 18, "column": 30},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $listBooleanField: [Boolean] = [null]
              $listEnumField: [MyEnum] = [null]
              $listFloatField: [Float] = [null]
              $listIntField: [Int] = [null]
              $listStringField: [String] = [null]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True, None],
                "listEnumField": ["ENUM_3", None],
                "listFloatField": [3456.789e2, None],
                "listIntField": [20, None],
                "listStringField": ["varValue", None],
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 14, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $enumField > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 15},
                            {"line": 15, "column": 28},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $floatField > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 15},
                            {"line": 16, "column": 29},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $intField > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 15},
                            {"line": 17, "column": 27},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $stringField > of type < String > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 15},
                            {"line": 18, "column": 30},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = false
              $listEnumField: [MyEnum] = ENUM_4
              $listFloatField: [Float] = 456.789e2
              $listIntField: [Int] = 30
              $listStringField: [String] = "varDefault"
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            None,
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:False]-[enumField:ENUM_4_4-MyEnum-enumField]-[floatField:45681.9]-[intField:33]-[stringField:vardefault-scalar-stringField]-[listBooleanField:False]-[listEnumField:enum_4_4-myenum]-[listFloatField:45681.9]-[listIntField:33]-[listStringField:vardefault-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = false
              $listEnumField: [MyEnum] = ENUM_4
              $listFloatField: [Float] = 456.789e2
              $listIntField: [Int] = 30
              $listStringField: [String] = "varDefault"
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
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
            },
            {
                "data": {"wrapperNonNullInputObjectWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < {booleanField: $booleanField, enumField: $enumField, floatField: $floatField, intField: $intField, stringField: $stringField, listBooleanField: $listBooleanField, listEnumField: $listEnumField, listFloatField: $listFloatField, listIntField: $listIntField, listStringField: $listStringField} >.",
                        "path": ["wrapperNonNullInputObjectWithDefaultField"],
                        "locations": [{"line": 13, "column": 64}],
                    }
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = false
              $listEnumField: [MyEnum] = ENUM_4
              $listFloatField: [Float] = 456.789e2
              $listIntField: [Int] = 30
              $listStringField: [String] = "varDefault"
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": [None],
                "listEnumField": [None],
                "listFloatField": [None],
                "listIntField": [None],
                "listStringField": [None],
            },
            {
                "data": {"wrapperNonNullInputObjectWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < {booleanField: $booleanField, enumField: $enumField, floatField: $floatField, intField: $intField, stringField: $stringField, listBooleanField: $listBooleanField, listEnumField: $listEnumField, listFloatField: $listFloatField, listIntField: $listIntField, listStringField: $listStringField} >.",
                        "path": ["wrapperNonNullInputObjectWithDefaultField"],
                        "locations": [{"line": 13, "column": 64}],
                    }
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = false
              $listEnumField: [MyEnum] = ENUM_4
              $listFloatField: [Float] = 456.789e2
              $listIntField: [Int] = 30
              $listStringField: [String] = "varDefault"
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": True,
                "listEnumField": "ENUM_3",
                "listFloatField": 3456.789e2,
                "listIntField": 20,
                "listStringField": "varValue",
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True]-[listEnumField:enum_3_3-myenum]-[listFloatField:345681.9]-[listIntField:23]-[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = false
              $listEnumField: [MyEnum] = ENUM_4
              $listFloatField: [Float] = 456.789e2
              $listIntField: [Int] = 30
              $listStringField: [String] = "varDefault"
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True],
                "listEnumField": ["ENUM_3"],
                "listFloatField": [3456.789e2],
                "listIntField": [20],
                "listStringField": ["varValue"],
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True]-[listEnumField:enum_3_3-myenum]-[listFloatField:345681.9]-[listIntField:23]-[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = false
              $listEnumField: [MyEnum] = ENUM_4
              $listFloatField: [Float] = 456.789e2
              $listIntField: [Int] = 30
              $listStringField: [String] = "varDefault"
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True, None],
                "listEnumField": ["ENUM_3", None],
                "listFloatField": [3456.789e2, None],
                "listIntField": [20, None],
                "listStringField": ["varValue", None],
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True-None]-[listEnumField:enum_3_3-myenum-None]-[listFloatField:345681.9-None]-[listIntField:23-None]-[listStringField:varvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = [false]
              $listEnumField: [MyEnum] = [ENUM_4]
              $listFloatField: [Float] = [456.789e2]
              $listIntField: [Int] = [30]
              $listStringField: [String] = ["varDefault"]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            None,
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:False]-[enumField:ENUM_4_4-MyEnum-enumField]-[floatField:45681.9]-[intField:33]-[stringField:vardefault-scalar-stringField]-[listBooleanField:False]-[listEnumField:enum_4_4-myenum]-[listFloatField:45681.9]-[listIntField:33]-[listStringField:vardefault-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = [false]
              $listEnumField: [MyEnum] = [ENUM_4]
              $listFloatField: [Float] = [456.789e2]
              $listIntField: [Int] = [30]
              $listStringField: [String] = ["varDefault"]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
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
            },
            {
                "data": {"wrapperNonNullInputObjectWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < {booleanField: $booleanField, enumField: $enumField, floatField: $floatField, intField: $intField, stringField: $stringField, listBooleanField: $listBooleanField, listEnumField: $listEnumField, listFloatField: $listFloatField, listIntField: $listIntField, listStringField: $listStringField} >.",
                        "path": ["wrapperNonNullInputObjectWithDefaultField"],
                        "locations": [{"line": 13, "column": 64}],
                    }
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = [false]
              $listEnumField: [MyEnum] = [ENUM_4]
              $listFloatField: [Float] = [456.789e2]
              $listIntField: [Int] = [30]
              $listStringField: [String] = ["varDefault"]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": [None],
                "listEnumField": [None],
                "listFloatField": [None],
                "listIntField": [None],
                "listStringField": [None],
            },
            {
                "data": {"wrapperNonNullInputObjectWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < {booleanField: $booleanField, enumField: $enumField, floatField: $floatField, intField: $intField, stringField: $stringField, listBooleanField: $listBooleanField, listEnumField: $listEnumField, listFloatField: $listFloatField, listIntField: $listIntField, listStringField: $listStringField} >.",
                        "path": ["wrapperNonNullInputObjectWithDefaultField"],
                        "locations": [{"line": 13, "column": 64}],
                    }
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = [false]
              $listEnumField: [MyEnum] = [ENUM_4]
              $listFloatField: [Float] = [456.789e2]
              $listIntField: [Int] = [30]
              $listStringField: [String] = ["varDefault"]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": True,
                "listEnumField": "ENUM_3",
                "listFloatField": 3456.789e2,
                "listIntField": 20,
                "listStringField": "varValue",
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True]-[listEnumField:enum_3_3-myenum]-[listFloatField:345681.9]-[listIntField:23]-[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = [false]
              $listEnumField: [MyEnum] = [ENUM_4]
              $listFloatField: [Float] = [456.789e2]
              $listIntField: [Int] = [30]
              $listStringField: [String] = ["varDefault"]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True],
                "listEnumField": ["ENUM_3"],
                "listFloatField": [3456.789e2],
                "listIntField": [20],
                "listStringField": ["varValue"],
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True]-[listEnumField:enum_3_3-myenum]-[listFloatField:345681.9]-[listIntField:23]-[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = [false]
              $listEnumField: [MyEnum] = [ENUM_4]
              $listFloatField: [Float] = [456.789e2]
              $listIntField: [Int] = [30]
              $listStringField: [String] = ["varDefault"]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True, None],
                "listEnumField": ["ENUM_3", None],
                "listFloatField": [3456.789e2, None],
                "listIntField": [20, None],
                "listStringField": ["varValue", None],
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True-None]-[listEnumField:enum_3_3-myenum-None]-[listFloatField:345681.9-None]-[listIntField:23-None]-[listStringField:varvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = [false, null]
              $listEnumField: [MyEnum] = [ENUM_4, null]
              $listFloatField: [Float] = [456.789e2, null]
              $listIntField: [Int] = [30, null]
              $listStringField: [String] = ["varDefault", null]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            None,
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:False]-[enumField:ENUM_4_4-MyEnum-enumField]-[floatField:45681.9]-[intField:33]-[stringField:vardefault-scalar-stringField]-[listBooleanField:False-None]-[listEnumField:enum_4_4-myenum-None]-[listFloatField:45681.9-None]-[listIntField:33-None]-[listStringField:vardefault-scalar-None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = [false, null]
              $listEnumField: [MyEnum] = [ENUM_4, null]
              $listFloatField: [Float] = [456.789e2, null]
              $listIntField: [Int] = [30, null]
              $listStringField: [String] = ["varDefault", null]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
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
            },
            {
                "data": {"wrapperNonNullInputObjectWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < {booleanField: $booleanField, enumField: $enumField, floatField: $floatField, intField: $intField, stringField: $stringField, listBooleanField: $listBooleanField, listEnumField: $listEnumField, listFloatField: $listFloatField, listIntField: $listIntField, listStringField: $listStringField} >.",
                        "path": ["wrapperNonNullInputObjectWithDefaultField"],
                        "locations": [{"line": 13, "column": 64}],
                    }
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = [false, null]
              $listEnumField: [MyEnum] = [ENUM_4, null]
              $listFloatField: [Float] = [456.789e2, null]
              $listIntField: [Int] = [30, null]
              $listStringField: [String] = ["varDefault", null]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": [None],
                "listEnumField": [None],
                "listFloatField": [None],
                "listIntField": [None],
                "listStringField": [None],
            },
            {
                "data": {"wrapperNonNullInputObjectWithDefaultField": None},
                "errors": [
                    {
                        "message": "Argument < param > has invalid value < {booleanField: $booleanField, enumField: $enumField, floatField: $floatField, intField: $intField, stringField: $stringField, listBooleanField: $listBooleanField, listEnumField: $listEnumField, listFloatField: $listFloatField, listIntField: $listIntField, listStringField: $listStringField} >.",
                        "path": ["wrapperNonNullInputObjectWithDefaultField"],
                        "locations": [{"line": 13, "column": 64}],
                    }
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = [false, null]
              $listEnumField: [MyEnum] = [ENUM_4, null]
              $listFloatField: [Float] = [456.789e2, null]
              $listIntField: [Int] = [30, null]
              $listStringField: [String] = ["varDefault", null]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": True,
                "listEnumField": "ENUM_3",
                "listFloatField": 3456.789e2,
                "listIntField": 20,
                "listStringField": "varValue",
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True]-[listEnumField:enum_3_3-myenum]-[listFloatField:345681.9]-[listIntField:23]-[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = [false, null]
              $listEnumField: [MyEnum] = [ENUM_4, null]
              $listFloatField: [Float] = [456.789e2, null]
              $listIntField: [Int] = [30, null]
              $listStringField: [String] = ["varDefault", null]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True],
                "listEnumField": ["ENUM_3"],
                "listFloatField": [3456.789e2],
                "listIntField": [20],
                "listStringField": ["varValue"],
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True]-[listEnumField:enum_3_3-myenum]-[listFloatField:345681.9]-[listIntField:23]-[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $listBooleanField: [Boolean] = [false, null]
              $listEnumField: [MyEnum] = [ENUM_4, null]
              $listFloatField: [Float] = [456.789e2, null]
              $listIntField: [Int] = [30, null]
              $listStringField: [String] = ["varDefault", null]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True, None],
                "listEnumField": ["ENUM_3", None],
                "listFloatField": [3456.789e2, None],
                "listIntField": [20, None],
                "listStringField": ["varValue", None],
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True-None]-[listEnumField:enum_3_3-myenum-None]-[listFloatField:345681.9-None]-[listIntField:23-None]-[listStringField:varvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean]!
              $listEnumField: [MyEnum]!
              $listFloatField: [Float]!
              $listIntField: [Int]!
              $listStringField: [String]!
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of required type < Boolean! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $enumField > of required type < MyEnum! > was not provided.",
                        "path": None,
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "Variable < $floatField > of required type < Float! > was not provided.",
                        "path": None,
                        "locations": [{"line": 4, "column": 15}],
                    },
                    {
                        "message": "Variable < $intField > of required type < Int! > was not provided.",
                        "path": None,
                        "locations": [{"line": 5, "column": 15}],
                    },
                    {
                        "message": "Variable < $stringField > of required type < String! > was not provided.",
                        "path": None,
                        "locations": [{"line": 6, "column": 15}],
                    },
                    {
                        "message": "Variable < $listBooleanField > of required type < [Boolean]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 7, "column": 15}],
                    },
                    {
                        "message": "Variable < $listEnumField > of required type < [MyEnum]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 8, "column": 15}],
                    },
                    {
                        "message": "Variable < $listFloatField > of required type < [Float]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 9, "column": 15}],
                    },
                    {
                        "message": "Variable < $listIntField > of required type < [Int]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 10, "column": 15}],
                    },
                    {
                        "message": "Variable < $listStringField > of required type < [String]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 11, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean]!
              $listEnumField: [MyEnum]!
              $listFloatField: [Float]!
              $listIntField: [Int]!
              $listStringField: [String]!
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
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
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of non-null type < Boolean! > must not be null.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $enumField > of non-null type < MyEnum! > must not be null.",
                        "path": None,
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "Variable < $floatField > of non-null type < Float! > must not be null.",
                        "path": None,
                        "locations": [{"line": 4, "column": 15}],
                    },
                    {
                        "message": "Variable < $intField > of non-null type < Int! > must not be null.",
                        "path": None,
                        "locations": [{"line": 5, "column": 15}],
                    },
                    {
                        "message": "Variable < $stringField > of non-null type < String! > must not be null.",
                        "path": None,
                        "locations": [{"line": 6, "column": 15}],
                    },
                    {
                        "message": "Variable < $listBooleanField > of non-null type < [Boolean]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 7, "column": 15}],
                    },
                    {
                        "message": "Variable < $listEnumField > of non-null type < [MyEnum]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 8, "column": 15}],
                    },
                    {
                        "message": "Variable < $listFloatField > of non-null type < [Float]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 9, "column": 15}],
                    },
                    {
                        "message": "Variable < $listIntField > of non-null type < [Int]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 10, "column": 15}],
                    },
                    {
                        "message": "Variable < $listStringField > of non-null type < [String]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 11, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean]!
              $listEnumField: [MyEnum]!
              $listFloatField: [Float]!
              $listIntField: [Int]!
              $listStringField: [String]!
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": [None],
                "listEnumField": [None],
                "listFloatField": [None],
                "listIntField": [None],
                "listStringField": [None],
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of non-null type < Boolean! > must not be null.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $enumField > of non-null type < MyEnum! > must not be null.",
                        "path": None,
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "Variable < $floatField > of non-null type < Float! > must not be null.",
                        "path": None,
                        "locations": [{"line": 4, "column": 15}],
                    },
                    {
                        "message": "Variable < $intField > of non-null type < Int! > must not be null.",
                        "path": None,
                        "locations": [{"line": 5, "column": 15}],
                    },
                    {
                        "message": "Variable < $stringField > of non-null type < String! > must not be null.",
                        "path": None,
                        "locations": [{"line": 6, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean]!
              $listEnumField: [MyEnum]!
              $listFloatField: [Float]!
              $listIntField: [Int]!
              $listStringField: [String]!
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": True,
                "listEnumField": "ENUM_3",
                "listFloatField": 3456.789e2,
                "listIntField": 20,
                "listStringField": "varValue",
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True]-[listEnumField:enum_3_3-myenum]-[listFloatField:345681.9]-[listIntField:23]-[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean]!
              $listEnumField: [MyEnum]!
              $listFloatField: [Float]!
              $listIntField: [Int]!
              $listStringField: [String]!
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True],
                "listEnumField": ["ENUM_3"],
                "listFloatField": [3456.789e2],
                "listIntField": [20],
                "listStringField": ["varValue"],
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True]-[listEnumField:enum_3_3-myenum]-[listFloatField:345681.9]-[listIntField:23]-[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean]!
              $listEnumField: [MyEnum]!
              $listFloatField: [Float]!
              $listIntField: [Int]!
              $listStringField: [String]!
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True, None],
                "listEnumField": ["ENUM_3", None],
                "listFloatField": [3456.789e2, None],
                "listIntField": [20, None],
                "listStringField": ["varValue", None],
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True-None]-[listEnumField:enum_3_3-myenum-None]-[listFloatField:345681.9-None]-[listIntField:23-None]-[listStringField:varvalue-scalar-None]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean!]
              $listEnumField: [MyEnum!]
              $listFloatField: [Float!]
              $listIntField: [Int!]
              $listStringField: [String!]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $listBooleanField > of type < [Boolean!] > used in position expecting type < [Boolean]! >.",
                        "path": None,
                        "locations": [
                            {"line": 7, "column": 15},
                            {"line": 19, "column": 35},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listEnumField > of type < [MyEnum!] > used in position expecting type < [MyEnum]! >.",
                        "path": None,
                        "locations": [
                            {"line": 8, "column": 15},
                            {"line": 20, "column": 32},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listFloatField > of type < [Float!] > used in position expecting type < [Float]! >.",
                        "path": None,
                        "locations": [
                            {"line": 9, "column": 15},
                            {"line": 21, "column": 33},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listIntField > of type < [Int!] > used in position expecting type < [Int]! >.",
                        "path": None,
                        "locations": [
                            {"line": 10, "column": 15},
                            {"line": 22, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listStringField > of type < [String!] > used in position expecting type < [String]! >.",
                        "path": None,
                        "locations": [
                            {"line": 11, "column": 15},
                            {"line": 23, "column": 34},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean!]
              $listEnumField: [MyEnum!]
              $listFloatField: [Float!]
              $listIntField: [Int!]
              $listStringField: [String!]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
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
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $listBooleanField > of type < [Boolean!] > used in position expecting type < [Boolean]! >.",
                        "path": None,
                        "locations": [
                            {"line": 7, "column": 15},
                            {"line": 19, "column": 35},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listEnumField > of type < [MyEnum!] > used in position expecting type < [MyEnum]! >.",
                        "path": None,
                        "locations": [
                            {"line": 8, "column": 15},
                            {"line": 20, "column": 32},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listFloatField > of type < [Float!] > used in position expecting type < [Float]! >.",
                        "path": None,
                        "locations": [
                            {"line": 9, "column": 15},
                            {"line": 21, "column": 33},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listIntField > of type < [Int!] > used in position expecting type < [Int]! >.",
                        "path": None,
                        "locations": [
                            {"line": 10, "column": 15},
                            {"line": 22, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listStringField > of type < [String!] > used in position expecting type < [String]! >.",
                        "path": None,
                        "locations": [
                            {"line": 11, "column": 15},
                            {"line": 23, "column": 34},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean!]
              $listEnumField: [MyEnum!]
              $listFloatField: [Float!]
              $listIntField: [Int!]
              $listStringField: [String!]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": [None],
                "listEnumField": [None],
                "listFloatField": [None],
                "listIntField": [None],
                "listStringField": [None],
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $listBooleanField > of type < [Boolean!] > used in position expecting type < [Boolean]! >.",
                        "path": None,
                        "locations": [
                            {"line": 7, "column": 15},
                            {"line": 19, "column": 35},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listEnumField > of type < [MyEnum!] > used in position expecting type < [MyEnum]! >.",
                        "path": None,
                        "locations": [
                            {"line": 8, "column": 15},
                            {"line": 20, "column": 32},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listFloatField > of type < [Float!] > used in position expecting type < [Float]! >.",
                        "path": None,
                        "locations": [
                            {"line": 9, "column": 15},
                            {"line": 21, "column": 33},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listIntField > of type < [Int!] > used in position expecting type < [Int]! >.",
                        "path": None,
                        "locations": [
                            {"line": 10, "column": 15},
                            {"line": 22, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listStringField > of type < [String!] > used in position expecting type < [String]! >.",
                        "path": None,
                        "locations": [
                            {"line": 11, "column": 15},
                            {"line": 23, "column": 34},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean!]
              $listEnumField: [MyEnum!]
              $listFloatField: [Float!]
              $listIntField: [Int!]
              $listStringField: [String!]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": True,
                "listEnumField": "ENUM_3",
                "listFloatField": 3456.789e2,
                "listIntField": 20,
                "listStringField": "varValue",
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $listBooleanField > of type < [Boolean!] > used in position expecting type < [Boolean]! >.",
                        "path": None,
                        "locations": [
                            {"line": 7, "column": 15},
                            {"line": 19, "column": 35},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listEnumField > of type < [MyEnum!] > used in position expecting type < [MyEnum]! >.",
                        "path": None,
                        "locations": [
                            {"line": 8, "column": 15},
                            {"line": 20, "column": 32},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listFloatField > of type < [Float!] > used in position expecting type < [Float]! >.",
                        "path": None,
                        "locations": [
                            {"line": 9, "column": 15},
                            {"line": 21, "column": 33},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listIntField > of type < [Int!] > used in position expecting type < [Int]! >.",
                        "path": None,
                        "locations": [
                            {"line": 10, "column": 15},
                            {"line": 22, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listStringField > of type < [String!] > used in position expecting type < [String]! >.",
                        "path": None,
                        "locations": [
                            {"line": 11, "column": 15},
                            {"line": 23, "column": 34},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean!]
              $listEnumField: [MyEnum!]
              $listFloatField: [Float!]
              $listIntField: [Int!]
              $listStringField: [String!]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True],
                "listEnumField": ["ENUM_3"],
                "listFloatField": [3456.789e2],
                "listIntField": [20],
                "listStringField": ["varValue"],
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $listBooleanField > of type < [Boolean!] > used in position expecting type < [Boolean]! >.",
                        "path": None,
                        "locations": [
                            {"line": 7, "column": 15},
                            {"line": 19, "column": 35},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listEnumField > of type < [MyEnum!] > used in position expecting type < [MyEnum]! >.",
                        "path": None,
                        "locations": [
                            {"line": 8, "column": 15},
                            {"line": 20, "column": 32},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listFloatField > of type < [Float!] > used in position expecting type < [Float]! >.",
                        "path": None,
                        "locations": [
                            {"line": 9, "column": 15},
                            {"line": 21, "column": 33},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listIntField > of type < [Int!] > used in position expecting type < [Int]! >.",
                        "path": None,
                        "locations": [
                            {"line": 10, "column": 15},
                            {"line": 22, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listStringField > of type < [String!] > used in position expecting type < [String]! >.",
                        "path": None,
                        "locations": [
                            {"line": 11, "column": 15},
                            {"line": 23, "column": 34},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean!]
              $listEnumField: [MyEnum!]
              $listFloatField: [Float!]
              $listIntField: [Int!]
              $listStringField: [String!]
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True, None],
                "listEnumField": ["ENUM_3", None],
                "listFloatField": [3456.789e2, None],
                "listIntField": [20, None],
                "listStringField": ["varValue", None],
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $listBooleanField > of type < [Boolean!] > used in position expecting type < [Boolean]! >.",
                        "path": None,
                        "locations": [
                            {"line": 7, "column": 15},
                            {"line": 19, "column": 35},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listEnumField > of type < [MyEnum!] > used in position expecting type < [MyEnum]! >.",
                        "path": None,
                        "locations": [
                            {"line": 8, "column": 15},
                            {"line": 20, "column": 32},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listFloatField > of type < [Float!] > used in position expecting type < [Float]! >.",
                        "path": None,
                        "locations": [
                            {"line": 9, "column": 15},
                            {"line": 21, "column": 33},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listIntField > of type < [Int!] > used in position expecting type < [Int]! >.",
                        "path": None,
                        "locations": [
                            {"line": 10, "column": 15},
                            {"line": 22, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $listStringField > of type < [String!] > used in position expecting type < [String]! >.",
                        "path": None,
                        "locations": [
                            {"line": 11, "column": 15},
                            {"line": 23, "column": 34},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean!]!
              $listEnumField: [MyEnum!]!
              $listFloatField: [Float!]!
              $listIntField: [Int!]!
              $listStringField: [String!]!
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of required type < Boolean! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $enumField > of required type < MyEnum! > was not provided.",
                        "path": None,
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "Variable < $floatField > of required type < Float! > was not provided.",
                        "path": None,
                        "locations": [{"line": 4, "column": 15}],
                    },
                    {
                        "message": "Variable < $intField > of required type < Int! > was not provided.",
                        "path": None,
                        "locations": [{"line": 5, "column": 15}],
                    },
                    {
                        "message": "Variable < $stringField > of required type < String! > was not provided.",
                        "path": None,
                        "locations": [{"line": 6, "column": 15}],
                    },
                    {
                        "message": "Variable < $listBooleanField > of required type < [Boolean!]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 7, "column": 15}],
                    },
                    {
                        "message": "Variable < $listEnumField > of required type < [MyEnum!]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 8, "column": 15}],
                    },
                    {
                        "message": "Variable < $listFloatField > of required type < [Float!]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 9, "column": 15}],
                    },
                    {
                        "message": "Variable < $listIntField > of required type < [Int!]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 10, "column": 15}],
                    },
                    {
                        "message": "Variable < $listStringField > of required type < [String!]! > was not provided.",
                        "path": None,
                        "locations": [{"line": 11, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean!]!
              $listEnumField: [MyEnum!]!
              $listFloatField: [Float!]!
              $listIntField: [Int!]!
              $listStringField: [String!]!
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
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
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of non-null type < Boolean! > must not be null.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $enumField > of non-null type < MyEnum! > must not be null.",
                        "path": None,
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "Variable < $floatField > of non-null type < Float! > must not be null.",
                        "path": None,
                        "locations": [{"line": 4, "column": 15}],
                    },
                    {
                        "message": "Variable < $intField > of non-null type < Int! > must not be null.",
                        "path": None,
                        "locations": [{"line": 5, "column": 15}],
                    },
                    {
                        "message": "Variable < $stringField > of non-null type < String! > must not be null.",
                        "path": None,
                        "locations": [{"line": 6, "column": 15}],
                    },
                    {
                        "message": "Variable < $listBooleanField > of non-null type < [Boolean!]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 7, "column": 15}],
                    },
                    {
                        "message": "Variable < $listEnumField > of non-null type < [MyEnum!]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 8, "column": 15}],
                    },
                    {
                        "message": "Variable < $listFloatField > of non-null type < [Float!]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 9, "column": 15}],
                    },
                    {
                        "message": "Variable < $listIntField > of non-null type < [Int!]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 10, "column": 15}],
                    },
                    {
                        "message": "Variable < $listStringField > of non-null type < [String!]! > must not be null.",
                        "path": None,
                        "locations": [{"line": 11, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean!]!
              $listEnumField: [MyEnum!]!
              $listFloatField: [Float!]!
              $listIntField: [Int!]!
              $listStringField: [String!]!
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "listBooleanField": [None],
                "listEnumField": [None],
                "listFloatField": [None],
                "listIntField": [None],
                "listStringField": [None],
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of non-null type < Boolean! > must not be null.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $enumField > of non-null type < MyEnum! > must not be null.",
                        "path": None,
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "Variable < $floatField > of non-null type < Float! > must not be null.",
                        "path": None,
                        "locations": [{"line": 4, "column": 15}],
                    },
                    {
                        "message": "Variable < $intField > of non-null type < Int! > must not be null.",
                        "path": None,
                        "locations": [{"line": 5, "column": 15}],
                    },
                    {
                        "message": "Variable < $stringField > of non-null type < String! > must not be null.",
                        "path": None,
                        "locations": [{"line": 6, "column": 15}],
                    },
                    {
                        "message": "Variable < $listBooleanField > got invalid value < [None] >; Expected non-nullable type < Boolean! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 7, "column": 15}],
                    },
                    {
                        "message": "Variable < $listEnumField > got invalid value < [None] >; Expected non-nullable type < MyEnum! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 8, "column": 15}],
                    },
                    {
                        "message": "Variable < $listFloatField > got invalid value < [None] >; Expected non-nullable type < Float! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 9, "column": 15}],
                    },
                    {
                        "message": "Variable < $listIntField > got invalid value < [None] >; Expected non-nullable type < Int! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 10, "column": 15}],
                    },
                    {
                        "message": "Variable < $listStringField > got invalid value < [None] >; Expected non-nullable type < String! > not to be null at value[0].",
                        "path": None,
                        "locations": [{"line": 11, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean!]!
              $listEnumField: [MyEnum!]!
              $listFloatField: [Float!]!
              $listIntField: [Int!]!
              $listStringField: [String!]!
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": True,
                "listEnumField": "ENUM_3",
                "listFloatField": 3456.789e2,
                "listIntField": 20,
                "listStringField": "varValue",
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True]-[listEnumField:enum_3_3-myenum]-[listFloatField:345681.9]-[listIntField:23]-[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean!]!
              $listEnumField: [MyEnum!]!
              $listFloatField: [Float!]!
              $listIntField: [Int!]!
              $listStringField: [String!]!
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True],
                "listEnumField": ["ENUM_3"],
                "listFloatField": [3456.789e2],
                "listIntField": [20],
                "listStringField": ["varValue"],
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:True]-[listEnumField:enum_3_3-myenum]-[listFloatField:345681.9]-[listIntField:23]-[listStringField:varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $listBooleanField: [Boolean!]!
              $listEnumField: [MyEnum!]!
              $listFloatField: [Float!]!
              $listIntField: [Int!]!
              $listStringField: [String!]!
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: $listBooleanField
                listEnumField: $listEnumField
                listFloatField: $listFloatField
                listIntField: $listIntField
                listStringField: $listStringField
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "listBooleanField": [True, None],
                "listEnumField": ["ENUM_3", None],
                "listFloatField": [3456.789e2, None],
                "listIntField": [20, None],
                "listStringField": ["varValue", None],
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $listBooleanField > got invalid value < [True, None] >; Expected non-nullable type < Boolean! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 7, "column": 15}],
                    },
                    {
                        "message": "Variable < $listEnumField > got invalid value < ['ENUM_3', None] >; Expected non-nullable type < MyEnum! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 8, "column": 15}],
                    },
                    {
                        "message": "Variable < $listFloatField > got invalid value < [345678.9, None] >; Expected non-nullable type < Float! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 9, "column": 15}],
                    },
                    {
                        "message": "Variable < $listIntField > got invalid value < [20, None] >; Expected non-nullable type < Int! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 10, "column": 15}],
                    },
                    {
                        "message": "Variable < $listStringField > got invalid value < ['varValue', None] >; Expected non-nullable type < String! > not to be null at value[1].",
                        "path": None,
                        "locations": [{"line": 11, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean
              $enumField: MyEnum
              $floatField: Float
              $intField: Int
              $stringField: String
              $itemBooleanField: Boolean
              $itemEnumField: MyEnum
              $itemFloatField: Float
              $itemIntField: Int
              $itemStringField: String
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: [false, $itemBooleanField]
                listEnumField: [ENUM_2, $itemEnumField]
                listFloatField: [23456.789e2, $itemFloatField]
                listIntField: [10, $itemIntField]
                listStringField: ["paramDefaultValue", $itemStringField]
              })
            }
            """,
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 14, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $enumField > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 15},
                            {"line": 15, "column": 28},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $floatField > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 15},
                            {"line": 16, "column": 29},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $intField > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 15},
                            {"line": 17, "column": 27},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $stringField > of type < String > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 15},
                            {"line": 18, "column": 30},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean
              $enumField: MyEnum
              $floatField: Float
              $intField: Int
              $stringField: String
              $itemBooleanField: Boolean
              $itemEnumField: MyEnum
              $itemFloatField: Float
              $itemIntField: Int
              $itemStringField: String
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: [false, $itemBooleanField]
                listEnumField: [ENUM_2, $itemEnumField]
                listFloatField: [23456.789e2, $itemFloatField]
                listIntField: [10, $itemIntField]
                listStringField: ["paramDefaultValue", $itemStringField]
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "itemBooleanField": None,
                "itemEnumField": None,
                "itemFloatField": None,
                "itemIntField": None,
                "itemStringField": None,
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 14, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $enumField > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 15},
                            {"line": 15, "column": 28},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $floatField > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 15},
                            {"line": 16, "column": 29},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $intField > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 15},
                            {"line": 17, "column": 27},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $stringField > of type < String > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 15},
                            {"line": 18, "column": 30},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean
              $enumField: MyEnum
              $floatField: Float
              $intField: Int
              $stringField: String
              $itemBooleanField: Boolean
              $itemEnumField: MyEnum
              $itemFloatField: Float
              $itemIntField: Int
              $itemStringField: String
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: [false, $itemBooleanField]
                listEnumField: [ENUM_2, $itemEnumField]
                listFloatField: [23456.789e2, $itemFloatField]
                listIntField: [10, $itemIntField]
                listStringField: ["paramDefaultValue", $itemStringField]
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "itemBooleanField": True,
                "itemEnumField": "ENUM_3",
                "itemFloatField": 3456.789e2,
                "itemIntField": 20,
                "itemStringField": "varValue",
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 14, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $enumField > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 15},
                            {"line": 15, "column": 28},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $floatField > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 15},
                            {"line": 16, "column": 29},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $intField > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 15},
                            {"line": 17, "column": 27},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $stringField > of type < String > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 15},
                            {"line": 18, "column": 30},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $itemBooleanField: Boolean = null
              $itemEnumField: MyEnum = null
              $itemFloatField: Float = null
              $itemIntField: Int = null
              $itemStringField: String = null
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: [false, $itemBooleanField]
                listEnumField: [ENUM_2, $itemEnumField]
                listFloatField: [23456.789e2, $itemFloatField]
                listIntField: [10, $itemIntField]
                listStringField: ["paramDefaultValue", $itemStringField]
              })
            }
            """,
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 14, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $enumField > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 15},
                            {"line": 15, "column": 28},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $floatField > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 15},
                            {"line": 16, "column": 29},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $intField > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 15},
                            {"line": 17, "column": 27},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $stringField > of type < String > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 15},
                            {"line": 18, "column": 30},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $itemBooleanField: Boolean = null
              $itemEnumField: MyEnum = null
              $itemFloatField: Float = null
              $itemIntField: Int = null
              $itemStringField: String = null
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: [false, $itemBooleanField]
                listEnumField: [ENUM_2, $itemEnumField]
                listFloatField: [23456.789e2, $itemFloatField]
                listIntField: [10, $itemIntField]
                listStringField: ["paramDefaultValue", $itemStringField]
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "itemBooleanField": None,
                "itemEnumField": None,
                "itemFloatField": None,
                "itemIntField": None,
                "itemStringField": None,
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 14, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $enumField > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 15},
                            {"line": 15, "column": 28},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $floatField > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 15},
                            {"line": 16, "column": 29},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $intField > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 15},
                            {"line": 17, "column": 27},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $stringField > of type < String > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 15},
                            {"line": 18, "column": 30},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean = null
              $enumField: MyEnum = null
              $floatField: Float = null
              $intField: Int = null
              $stringField: String = null
              $itemBooleanField: Boolean = null
              $itemEnumField: MyEnum = null
              $itemFloatField: Float = null
              $itemIntField: Int = null
              $itemStringField: String = null
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: [false, $itemBooleanField]
                listEnumField: [ENUM_2, $itemEnumField]
                listFloatField: [23456.789e2, $itemFloatField]
                listIntField: [10, $itemIntField]
                listStringField: ["paramDefaultValue", $itemStringField]
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "itemBooleanField": True,
                "itemEnumField": "ENUM_3",
                "itemFloatField": 3456.789e2,
                "itemIntField": 20,
                "itemStringField": "varValue",
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of type < Boolean > used in position expecting type < Boolean! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 15},
                            {"line": 14, "column": 31},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $enumField > of type < MyEnum > used in position expecting type < MyEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 15},
                            {"line": 15, "column": 28},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $floatField > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 15},
                            {"line": 16, "column": 29},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $intField > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 15},
                            {"line": 17, "column": 27},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $stringField > of type < String > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 15},
                            {"line": 18, "column": 30},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $itemBooleanField: Boolean = false
              $itemEnumField: MyEnum = ENUM_4
              $itemFloatField: Float = 456.789e2
              $itemIntField: Int = 30
              $itemStringField: String = "varDefault"
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: [false, $itemBooleanField]
                listEnumField: [ENUM_2, $itemEnumField]
                listFloatField: [23456.789e2, $itemFloatField]
                listIntField: [10, $itemIntField]
                listStringField: ["paramDefaultValue", $itemStringField]
              })
            }
            """,
            None,
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:False]-[enumField:ENUM_4_4-MyEnum-enumField]-[floatField:45681.9]-[intField:33]-[stringField:vardefault-scalar-stringField]-[listBooleanField:False-False]-[listEnumField:enum_2_2-myenum-enum_4_4-myenum]-[listFloatField:2345681.9-45681.9]-[listIntField:13-33]-[listStringField:paramdefaultvalue-scalar-vardefault-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $itemBooleanField: Boolean = false
              $itemEnumField: MyEnum = ENUM_4
              $itemFloatField: Float = 456.789e2
              $itemIntField: Int = 30
              $itemStringField: String = "varDefault"
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: [false, $itemBooleanField]
                listEnumField: [ENUM_2, $itemEnumField]
                listFloatField: [23456.789e2, $itemFloatField]
                listIntField: [10, $itemIntField]
                listStringField: ["paramDefaultValue", $itemStringField]
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "itemBooleanField": None,
                "itemEnumField": None,
                "itemFloatField": None,
                "itemIntField": None,
                "itemStringField": None,
            },
            {
                "data": {"wrapperNonNullInputObjectWithDefaultField": None},
                "errors": [
                    {
                        "message": 'Argument < param > has invalid value < {booleanField: $booleanField, enumField: $enumField, floatField: $floatField, intField: $intField, stringField: $stringField, listBooleanField: [false, $itemBooleanField], listEnumField: [ENUM_2, $itemEnumField], listFloatField: [23456.789e2, $itemFloatField], listIntField: [10, $itemIntField], listStringField: ["paramDefaultValue", $itemStringField]} >.',
                        "path": ["wrapperNonNullInputObjectWithDefaultField"],
                        "locations": [{"line": 13, "column": 64}],
                    }
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean = false
              $enumField: MyEnum = ENUM_4
              $floatField: Float = 456.789e2
              $intField: Int = 30
              $stringField: String = "varDefault"
              $itemBooleanField: Boolean = false
              $itemEnumField: MyEnum = ENUM_4
              $itemFloatField: Float = 456.789e2
              $itemIntField: Int = 30
              $itemStringField: String = "varDefault"
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: [false, $itemBooleanField]
                listEnumField: [ENUM_2, $itemEnumField]
                listFloatField: [23456.789e2, $itemFloatField]
                listIntField: [10, $itemIntField]
                listStringField: ["paramDefaultValue", $itemStringField]
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "itemBooleanField": True,
                "itemEnumField": "ENUM_3",
                "itemFloatField": 3456.789e2,
                "itemIntField": 20,
                "itemStringField": "varValue",
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:False-True]-[listEnumField:enum_2_2-myenum-enum_3_3-myenum]-[listFloatField:2345681.9-345681.9]-[listIntField:13-23]-[listStringField:paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $itemBooleanField: Boolean!
              $itemEnumField: MyEnum!
              $itemFloatField: Float!
              $itemIntField: Int!
              $itemStringField: String!
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: [false, $itemBooleanField]
                listEnumField: [ENUM_2, $itemEnumField]
                listFloatField: [23456.789e2, $itemFloatField]
                listIntField: [10, $itemIntField]
                listStringField: ["paramDefaultValue", $itemStringField]
              })
            }
            """,
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of required type < Boolean! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $enumField > of required type < MyEnum! > was not provided.",
                        "path": None,
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "Variable < $floatField > of required type < Float! > was not provided.",
                        "path": None,
                        "locations": [{"line": 4, "column": 15}],
                    },
                    {
                        "message": "Variable < $intField > of required type < Int! > was not provided.",
                        "path": None,
                        "locations": [{"line": 5, "column": 15}],
                    },
                    {
                        "message": "Variable < $stringField > of required type < String! > was not provided.",
                        "path": None,
                        "locations": [{"line": 6, "column": 15}],
                    },
                    {
                        "message": "Variable < $itemBooleanField > of required type < Boolean! > was not provided.",
                        "path": None,
                        "locations": [{"line": 7, "column": 15}],
                    },
                    {
                        "message": "Variable < $itemEnumField > of required type < MyEnum! > was not provided.",
                        "path": None,
                        "locations": [{"line": 8, "column": 15}],
                    },
                    {
                        "message": "Variable < $itemFloatField > of required type < Float! > was not provided.",
                        "path": None,
                        "locations": [{"line": 9, "column": 15}],
                    },
                    {
                        "message": "Variable < $itemIntField > of required type < Int! > was not provided.",
                        "path": None,
                        "locations": [{"line": 10, "column": 15}],
                    },
                    {
                        "message": "Variable < $itemStringField > of required type < String! > was not provided.",
                        "path": None,
                        "locations": [{"line": 11, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $itemBooleanField: Boolean!
              $itemEnumField: MyEnum!
              $itemFloatField: Float!
              $itemIntField: Int!
              $itemStringField: String!
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: [false, $itemBooleanField]
                listEnumField: [ENUM_2, $itemEnumField]
                listFloatField: [23456.789e2, $itemFloatField]
                listIntField: [10, $itemIntField]
                listStringField: ["paramDefaultValue", $itemStringField]
              })
            }
            """,
            {
                "booleanField": None,
                "enumField": None,
                "floatField": None,
                "intField": None,
                "stringField": None,
                "itemBooleanField": None,
                "itemEnumField": None,
                "itemFloatField": None,
                "itemIntField": None,
                "itemStringField": None,
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $booleanField > of non-null type < Boolean! > must not be null.",
                        "path": None,
                        "locations": [{"line": 2, "column": 15}],
                    },
                    {
                        "message": "Variable < $enumField > of non-null type < MyEnum! > must not be null.",
                        "path": None,
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "Variable < $floatField > of non-null type < Float! > must not be null.",
                        "path": None,
                        "locations": [{"line": 4, "column": 15}],
                    },
                    {
                        "message": "Variable < $intField > of non-null type < Int! > must not be null.",
                        "path": None,
                        "locations": [{"line": 5, "column": 15}],
                    },
                    {
                        "message": "Variable < $stringField > of non-null type < String! > must not be null.",
                        "path": None,
                        "locations": [{"line": 6, "column": 15}],
                    },
                    {
                        "message": "Variable < $itemBooleanField > of non-null type < Boolean! > must not be null.",
                        "path": None,
                        "locations": [{"line": 7, "column": 15}],
                    },
                    {
                        "message": "Variable < $itemEnumField > of non-null type < MyEnum! > must not be null.",
                        "path": None,
                        "locations": [{"line": 8, "column": 15}],
                    },
                    {
                        "message": "Variable < $itemFloatField > of non-null type < Float! > must not be null.",
                        "path": None,
                        "locations": [{"line": 9, "column": 15}],
                    },
                    {
                        "message": "Variable < $itemIntField > of non-null type < Int! > must not be null.",
                        "path": None,
                        "locations": [{"line": 10, "column": 15}],
                    },
                    {
                        "message": "Variable < $itemStringField > of non-null type < String! > must not be null.",
                        "path": None,
                        "locations": [{"line": 11, "column": 15}],
                    },
                ],
            },
        ),
        (
            """query (
              $booleanField: Boolean!
              $enumField: MyEnum!
              $floatField: Float!
              $intField: Int!
              $stringField: String!
              $itemBooleanField: Boolean!
              $itemEnumField: MyEnum!
              $itemFloatField: Float!
              $itemIntField: Int!
              $itemStringField: String!
            ) {
              wrapperNonNullInputObjectWithDefaultField(param: {
                booleanField: $booleanField
                enumField: $enumField
                floatField: $floatField
                intField: $intField
                stringField: $stringField
                listBooleanField: [false, $itemBooleanField]
                listEnumField: [ENUM_2, $itemEnumField]
                listFloatField: [23456.789e2, $itemFloatField]
                listIntField: [10, $itemIntField]
                listStringField: ["paramDefaultValue", $itemStringField]
              })
            }
            """,
            {
                "booleanField": True,
                "enumField": "ENUM_3",
                "floatField": 3456.789e2,
                "intField": 20,
                "stringField": "varValue",
                "itemBooleanField": True,
                "itemEnumField": "ENUM_3",
                "itemFloatField": 3456.789e2,
                "itemIntField": 20,
                "itemStringField": "varValue",
            },
            {
                "data": {
                    "wrapperNonNullInputObjectWithDefaultField": "SUCCESS-[booleanField:True]-[enumField:ENUM_3_3-MyEnum-enumField]-[floatField:345681.9]-[intField:23]-[stringField:varvalue-scalar-stringField]-[listBooleanField:False-True]-[listEnumField:enum_2_2-myenum-enum_3_3-myenum]-[listFloatField:2345681.9-345681.9]-[listIntField:13-23]-[listStringField:paramdefaultvalue-scalar-varvalue-scalar]"
                }
            },
        ),
    ],
)
async def test_coercer_wrapper_non_null_input_object_with_default_field(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected
