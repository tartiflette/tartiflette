from typing import Any, Callable, Dict, Optional, Union

import pytest

from tartiflette import Directive, create_engine

_SDL = """
directive @error on FIELD_DEFINITION | ARGUMENT_DEFINITION | INPUT_FIELD_DEFINITION | ENUM | ENUM_VALUE

enum MyEnum {
  ENUM_1
  ENUM_2
  ENUM_3
  ENUM_4
}

input MyInnerInput {
  booleanField: Boolean @error
  enumField: MyEnum @error
  floatField: Float @error
  intField: Int @error
  stringField: String @error
  listBooleanField: [Boolean] @error
  listEnumField: [MyEnum] @error
  listFloatField: [Float] @error
  listIntField: [Int] @error
  listStringField: [String] @error
}

input MyInput {
  booleanField: Boolean @error
  enumField: MyEnum @error
  floatField: Float @error
  intField: Int @error
  stringField: String @error
  listBooleanField: [Boolean] @error
  listEnumField: [MyEnum] @error
  listFloatField: [Float] @error
  listIntField: [Int] @error
  listStringField: [String] @error
  innerInputField: MyInnerInput @error
}

type Query {
  inputObjectField(param: MyInput): String
}
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Directive("error", schema_name="test_coercer_input_object_field_error")
    class ErrorDirective:
        @staticmethod
        async def on_post_input_coercion(
            directive_args: Dict[str, Any],
            next_directive: Callable,
            parent_node,
            value: Any,
            ctx: Optional[Any],
        ):
            raise ValueError("[ERROR] on_post_input_coercion")

    async def resolve_query_input_object_field(parent, args, ctx, info):
        if "param" not in args:
            return "SUCCESS"

        if args["param"] is None:
            return "SUCCESS-None"

        if not args["param"] and isinstance(args["param"], dict):
            return "SUCCESS-{}"

        return f"SUCCESS-{args['param']}"

    return await create_engine(
        _SDL, schema_name="test_coercer_input_object_field_error"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """
            query {
              inputObjectField(param: {
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
                innerInputField: {
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
                }
              })
            }""",
            None,
            {
                "data": {"inputObjectField": None},
                "errors": [
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": ["inputObjectField"],
                        "locations": [{"line": 4, "column": 31}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": ["inputObjectField"],
                        "locations": [{"line": 5, "column": 28}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": ["inputObjectField"],
                        "locations": [{"line": 6, "column": 29}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": ["inputObjectField"],
                        "locations": [{"line": 7, "column": 27}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": ["inputObjectField"],
                        "locations": [{"line": 8, "column": 30}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": ["inputObjectField"],
                        "locations": [{"line": 9, "column": 35}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": ["inputObjectField"],
                        "locations": [{"line": 10, "column": 32}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": ["inputObjectField"],
                        "locations": [{"line": 11, "column": 33}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": ["inputObjectField"],
                        "locations": [{"line": 12, "column": 31}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": ["inputObjectField"],
                        "locations": [{"line": 13, "column": 34}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": ["inputObjectField"],
                        "locations": [{"line": 15, "column": 33}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": ["inputObjectField"],
                        "locations": [{"line": 16, "column": 30}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": ["inputObjectField"],
                        "locations": [{"line": 17, "column": 31}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": ["inputObjectField"],
                        "locations": [{"line": 18, "column": 29}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": ["inputObjectField"],
                        "locations": [{"line": 19, "column": 32}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": ["inputObjectField"],
                        "locations": [{"line": 20, "column": 37}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": ["inputObjectField"],
                        "locations": [{"line": 21, "column": 34}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": ["inputObjectField"],
                        "locations": [{"line": 22, "column": 35}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": ["inputObjectField"],
                        "locations": [{"line": 23, "column": 33}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": ["inputObjectField"],
                        "locations": [{"line": 24, "column": 36}],
                    },
                ],
            },
        ),
        (
            """query ($param: MyInput) { inputObjectField(param: $param) }""",
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
                    "innerInputField": {
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
                }
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "[ERROR] on_post_input_coercion",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                ],
            },
        ),
    ],
)
async def test_coercer_input_object_field_error(
    ttftt_engine, query, variables, expected
):
    assert await ttftt_engine.execute(query, variables=variables) == expected
