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
            """query { nonNullBooleanField }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Field < nonNullBooleanField > argument < param > of type < Boolean! > is required, but it was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 9}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.4.2.1",
                            "tag": "required-arguments",
                            "details": "https://spec.graphql.org/June2018/#sec-Required-Arguments",
                        },
                    }
                ],
            },
        ),
        (
            """query ($param: Boolean!) { nonNullBooleanField(param: $param) }""",
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
            """query { nonNullBooleanField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Boolean! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 36}],
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
    ],
)
async def test_coercion_boolean_field_arguments_errors(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullEnumField }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Field < nonNullEnumField > argument < param > of type < MyEnum! > is required, but it was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 9}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.4.2.1",
                            "tag": "required-arguments",
                            "details": "https://spec.graphql.org/June2018/#sec-Required-Arguments",
                        },
                    }
                ],
            },
        ),
        (
            """query ($param: MyEnum!) { nonNullEnumField(param: $param) }""",
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
            """query { nonNullEnumField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < MyEnum! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 33}],
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
    ],
)
async def test_coercion_enum_field_arguments_errors(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullFloatField }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Field < nonNullFloatField > argument < param > of type < Float! > is required, but it was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 9}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.4.2.1",
                            "tag": "required-arguments",
                            "details": "https://spec.graphql.org/June2018/#sec-Required-Arguments",
                        },
                    }
                ],
            },
        ),
        (
            """query ($param: Float!) { nonNullFloatField(param: $param) }""",
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
            """query { nonNullFloatField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Float! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 34}],
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
    ],
)
async def test_coercion_float_field_arguments_errors(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullIntField }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Field < nonNullIntField > argument < param > of type < Int! > is required, but it was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 9}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.4.2.1",
                            "tag": "required-arguments",
                            "details": "https://spec.graphql.org/June2018/#sec-Required-Arguments",
                        },
                    }
                ],
            },
        ),
        (
            """query ($param: Int!) { nonNullIntField(param: $param) }""",
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
            """query { nonNullIntField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < Int! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 32}],
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
    ],
)
async def test_coercion_int_field_arguments_errors(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullStringField }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Field < nonNullStringField > argument < param > of type < String! > is required, but it was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 9}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.4.2.1",
                            "tag": "required-arguments",
                            "details": "https://spec.graphql.org/June2018/#sec-Required-Arguments",
                        },
                    }
                ],
            },
        ),
        (
            """query ($param: String!) { nonNullStringField(param: $param) }""",
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
            """query { nonNullStringField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < String! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 35}],
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
    ],
)
async def test_coercion_string_field_arguments_errors(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="coercion")
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """query { nonNullInputObjectField }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Field < nonNullInputObjectField > argument < param > of type < MyInput! > is required, but it was not provided.",
                        "path": None,
                        "locations": [{"line": 1, "column": 9}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.4.2.1",
                            "tag": "required-arguments",
                            "details": "https://spec.graphql.org/June2018/#sec-Required-Arguments",
                        },
                    }
                ],
            },
        ),
        (
            """query ($param: MyInput!) { nonNullInputObjectField(param: $param) }""",
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
            """query { nonNullInputObjectField(param: null) }""",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type < MyInput! >, found < null >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 40}],
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
    ],
)
async def test_coercion_input_object_field_arguments_errors(
    schema_stack, query, variables, expected
):
    assert await schema_stack.execute(query, variables=variables) == expected


_SDL = """
directive @internalCoercionError on INPUT_FIELD_DEFINITION | SCALAR | ARGUMENT_DEFINITION
directive @customCoercionError on INPUT_FIELD_DEFINITION | SCALAR | ARGUMENT_DEFINITION

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


def bakery(schema_name):
    @Directive("internalCoercionError", schema_name=schema_name)
    class InternalCoercionError:
        async def on_post_argument_coercion(
            self,
            directive_args,
            next_directive,
            parent_node,
            argument_definition_node,
            value,
            ctx,
        ):
            raise CoercionError("Oopsie")

        async def on_post_input_coercion(
            self,
            directive_args,
            next_directive,
            parent_node,
            input_definition_node,
            value,
            ctx,
        ):
            raise CoercionError("Oopsie")

    @Directive("customCoercionError", schema_name=schema_name)
    class CustomCoercionError:
        async def on_post_argument_coercion(
            self,
            directive_args,
            next_directive,
            parent_node,
            argument_definition_node,
            value,
            ctx,
        ):
            raise ValueError("Oopsie")

        async def on_post_input_coercion(
            self,
            directive_args,
            next_directive,
            parent_node,
            input_definition_node,
            value,
            ctx,
        ):
            raise ValueError("Oopsie")

    @Scalar("FirstErrorScalar", schema_name=schema_name)
    @Scalar("SecondErrorScalar", schema_name=schema_name)
    class ErrorScalars(ScalarString):
        pass


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    directive @internalCoercionError on INPUT_FIELD_DEFINITION | SCALAR | ARGUMENT_DEFINITION
    directive @customCoercionError on INPUT_FIELD_DEFINITION | SCALAR | ARGUMENT_DEFINITION

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
    """,
    bakery=bakery,
)
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
async def test_coercion_arguments_errors(schema_stack, query, expected):
    assert await schema_stack.execute(query) == expected
