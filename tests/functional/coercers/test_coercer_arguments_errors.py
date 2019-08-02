import pytest

from tartiflette import Directive, Scalar, create_engine
from tartiflette.scalar.builtins.string import ScalarString
from tartiflette.types.exceptions.tartiflette import CoercionError
from tests.functional.coercers.common import (
    resolve_input_object_field,
    resolve_unwrapped_field,
)


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.nonNullBooleanField": resolve_unwrapped_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullBooleanField }""",
            None,
            {
                "data": {"nonNullBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < Boolean! > was not provided.",
                        "path": ["nonNullBooleanField"],
                        "locations": [{"line": 1, "column": 9}],
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean) { nonNullBooleanField(param: $param) }""",
            None,
            {
                "data": {"nonNullBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < Boolean! > was provided the variable < $param > which was not provided a runtime value.",
                        "path": ["nonNullBooleanField"],
                        "locations": [{"line": 1, "column": 54}],
                    }
                ],
            },
        ),
        (
            """query { nonNullBooleanField(param: null) }""",
            None,
            {
                "data": {"nonNullBooleanField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Boolean! > must not be null.",
                        "path": ["nonNullBooleanField"],
                        "locations": [{"line": 1, "column": 36}],
                    }
                ],
            },
        ),
    ],
)
async def test_coercion_boolean_field_arguments_errors(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.nonNullEnumField": resolve_unwrapped_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullEnumField }""",
            None,
            {
                "data": {"nonNullEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < MyEnum! > was not provided.",
                        "path": ["nonNullEnumField"],
                        "locations": [{"line": 1, "column": 9}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum) { nonNullEnumField(param: $param) }""",
            None,
            {
                "data": {"nonNullEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < MyEnum! > was provided the variable < $param > which was not provided a runtime value.",
                        "path": ["nonNullEnumField"],
                        "locations": [{"line": 1, "column": 50}],
                    }
                ],
            },
        ),
        (
            """query { nonNullEnumField(param: null) }""",
            None,
            {
                "data": {"nonNullEnumField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < MyEnum! > must not be null.",
                        "path": ["nonNullEnumField"],
                        "locations": [{"line": 1, "column": 33}],
                    }
                ],
            },
        ),
    ],
)
async def test_coercion_enum_field_arguments_errors(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.nonNullFloatField": resolve_unwrapped_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullFloatField }""",
            None,
            {
                "data": {"nonNullFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < Float! > was not provided.",
                        "path": ["nonNullFloatField"],
                        "locations": [{"line": 1, "column": 9}],
                    }
                ],
            },
        ),
        (
            """query ($param: Float) { nonNullFloatField(param: $param) }""",
            None,
            {
                "data": {"nonNullFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < Float! > was provided the variable < $param > which was not provided a runtime value.",
                        "path": ["nonNullFloatField"],
                        "locations": [{"line": 1, "column": 50}],
                    }
                ],
            },
        ),
        (
            """query { nonNullFloatField(param: null) }""",
            None,
            {
                "data": {"nonNullFloatField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Float! > must not be null.",
                        "path": ["nonNullFloatField"],
                        "locations": [{"line": 1, "column": 34}],
                    }
                ],
            },
        ),
    ],
)
async def test_coercion_float_field_arguments_errors(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.nonNullIntField": resolve_unwrapped_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullIntField }""",
            None,
            {
                "data": {"nonNullIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < Int! > was not provided.",
                        "path": ["nonNullIntField"],
                        "locations": [{"line": 1, "column": 9}],
                    }
                ],
            },
        ),
        (
            """query ($param: Int) { nonNullIntField(param: $param) }""",
            None,
            {
                "data": {"nonNullIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < Int! > was provided the variable < $param > which was not provided a runtime value.",
                        "path": ["nonNullIntField"],
                        "locations": [{"line": 1, "column": 46}],
                    }
                ],
            },
        ),
        (
            """query { nonNullIntField(param: null) }""",
            None,
            {
                "data": {"nonNullIntField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < Int! > must not be null.",
                        "path": ["nonNullIntField"],
                        "locations": [{"line": 1, "column": 32}],
                    }
                ],
            },
        ),
    ],
)
async def test_coercion_int_field_arguments_errors(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.nonNullStringField": resolve_unwrapped_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullStringField }""",
            None,
            {
                "data": {"nonNullStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < String! > was not provided.",
                        "path": ["nonNullStringField"],
                        "locations": [{"line": 1, "column": 9}],
                    }
                ],
            },
        ),
        (
            """query ($param: String) { nonNullStringField(param: $param) }""",
            None,
            {
                "data": {"nonNullStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < String! > was provided the variable < $param > which was not provided a runtime value.",
                        "path": ["nonNullStringField"],
                        "locations": [{"line": 1, "column": 52}],
                    }
                ],
            },
        ),
        (
            """query { nonNullStringField(param: null) }""",
            None,
            {
                "data": {"nonNullStringField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < String! > must not be null.",
                        "path": ["nonNullStringField"],
                        "locations": [{"line": 1, "column": 35}],
                    }
                ],
            },
        ),
    ],
)
async def test_coercion_string_field_arguments_errors(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="coercion",
    resolvers={"Query.nonNullInputObjectField": resolve_input_object_field},
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullInputObjectField }""",
            None,
            {
                "data": {"nonNullInputObjectField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < MyInput! > was not provided.",
                        "path": ["nonNullInputObjectField"],
                        "locations": [{"line": 1, "column": 9}],
                    }
                ],
            },
        ),
        (
            """query ($param: MyInput) { nonNullInputObjectField(param: $param) }""",
            None,
            {
                "data": {"nonNullInputObjectField": None},
                "errors": [
                    {
                        "message": "Argument < param > of required type < MyInput! > was provided the variable < $param > which was not provided a runtime value.",
                        "path": ["nonNullInputObjectField"],
                        "locations": [{"line": 1, "column": 58}],
                    }
                ],
            },
        ),
        (
            """query { nonNullInputObjectField(param: null) }""",
            None,
            {
                "data": {"nonNullInputObjectField": None},
                "errors": [
                    {
                        "message": "Argument < param > of non-null type < MyInput! > must not be null.",
                        "path": ["nonNullInputObjectField"],
                        "locations": [{"line": 1, "column": 40}],
                    }
                ],
            },
        ),
    ],
)
async def test_coercion_input_object_field_arguments_errors(
    engine, query, variables, expected
):
    assert await engine.execute(query, variables=variables) == expected


_SDL = """
directive @internalCoercionError on INPUT_FIELD_DEFINITION
directive @customCoercionError on INPUT_FIELD_DEFINITION

scalar FirstErrorScalar @internalCoercionError
scalar SecondErrorScalar @customCoercionError

input FirstInputField {
  inputField: String
}

input SecondInputField {
  inputField: String
}

type Query {
  field(
    firstInput: FirstInputField @internalCoercionError
    secondInput: SecondInputField @customCoercionError
    firstErrorScalar: FirstErrorScalar
    secondErrorScalar: SecondErrorScalar
  ): String!
}
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Directive(
        "internalCoercionError", schema_name="test_coercion_arguments_errors"
    )
    class InternalCoercionError:
        async def on_argument_execution(
            self,
            directive_args,
            next_directive,
            parent_node,
            argument_node,
            value,
            ctx,
        ):
            raise CoercionError("Oopsie")

        async def on_post_input_coercion(
            self, directive_args, next_directive, parent_node, value, ctx
        ):
            raise CoercionError("Oopsie")

    @Directive(
        "customCoercionError", schema_name="test_coercion_arguments_errors"
    )
    class CustomCoercionError:
        async def on_argument_execution(
            self,
            directive_args,
            next_directive,
            parent_node,
            argument_node,
            value,
            ctx,
        ):
            raise ValueError("Oopsie")

        async def on_post_input_coercion(
            self, directive_args, next_directive, parent_node, value, ctx
        ):
            raise ValueError("Oopsie")

    @Scalar("FirstErrorScalar", schema_name="test_coercion_arguments_errors")
    @Scalar("SecondErrorScalar", schema_name="test_coercion_arguments_errors")
    class ErrorScalars(ScalarString):
        pass

    return await create_engine(
        sdl=_SDL, schema_name="test_coercion_arguments_errors"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            {
              field(firstInput: {inputField: "aValue"})
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Oopsie",
                        "path": ["field"],
                        "locations": [{"line": 3, "column": 21}],
                    }
                ],
            },
        ),
        (
            """
            {
              field(secondInput: {inputField: "aValue"})
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Oopsie",
                        "path": ["field"],
                        "locations": [{"line": 3, "column": 21}],
                    }
                ],
            },
        ),
        (
            """
            {
              field(firstErrorScalar: "aValue")
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Oopsie",
                        "path": ["field"],
                        "locations": [{"line": 3, "column": 39}],
                    }
                ],
            },
        ),
        (
            """
            {
              field(secondErrorScalar: "aValue")
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Oopsie",
                        "path": ["field"],
                        "locations": [{"line": 3, "column": 40}],
                    }
                ],
            },
        ),
    ],
)
async def test_coercion_arguments_errors(ttftt_engine, query, expected):
    assert await ttftt_engine.execute(query) == expected
