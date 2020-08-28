import pytest

from tartiflette import Directive, Resolver, Scalar
from tests.data.modules.pets.common import StringScalar
from tests.functional.utils import assert_unordered_lists


def bakery(schema_name):
    @Directive("wentThrough", schema_name=schema_name)
    class WentThroughDirective:
        @staticmethod
        async def on_schema_execution(
            directive_args,
            next_directive,
            schema,
            document,
            parsing_errors,
            operation_name,
            context,
            variables,
            initial_value,
        ):
            result = await next_directive(
                schema,
                document,
                parsing_errors,
                operation_name,
                context,
                variables,
                initial_value,
            )
            context["went_through"].append(
                f"wentThrough.on_schema_execution {directive_args['over']}"
            )
            return result

        @staticmethod
        async def on_post_argument_coercion(
            directive_args,
            next_directive,
            parent_node,
            argument_definition_node,
            value,
            ctx,
        ):
            result = await next_directive(
                parent_node, argument_definition_node, value, ctx,
            )
            ctx["went_through"].append(
                f"wentThrough.on_post_argument_coercion {directive_args['over']}"
            )
            return result

        @staticmethod
        async def on_post_input_object_coercion(
            directive_args,
            next_directive,
            parent_node,
            input_object_type_definition,
            value,
            ctx,
        ):
            result = await next_directive(parent_node, value, ctx)
            ctx["went_through"].append(
                f"wentThrough.on_post_input_object_coercion {directive_args['over']}"
            )
            return result

        @staticmethod
        async def on_post_input_field_coercion(
            directive_args,
            next_directive,
            parent_node,
            input_field_definition,
            value,
            ctx,
        ):
            result = await next_directive(parent_node, value, ctx)
            ctx["went_through"].append(
                f"wentThrough.on_post_input_field_coercion {directive_args['over']}"
            )
            return result

        @staticmethod
        async def on_post_scalar_input_coercion(
            directive_args,
            next_directive,
            parent_node,
            scalar_definition,
            value,
            ctx,
        ):
            result = await next_directive(parent_node, value, ctx)
            ctx["went_through"].append(
                f"wentThrough.on_post_scalar_input_coercion {directive_args['over']}"
            )
            return result

        @staticmethod
        async def on_post_enum_type_input_coercion(
            directive_args,
            next_directive,
            parent_node,
            enum_type_definition,
            value,
            ctx,
        ):
            result = await next_directive(parent_node, value, ctx)
            ctx["went_through"].append(
                f"wentThrough.on_post_enum_type_input_coercion {directive_args['over']}"
            )
            return result

        @staticmethod
        async def on_post_enum_value_input_coercion(
            directive_args,
            next_directive,
            parent_node,
            enum_value_definition,
            value,
            ctx,
        ):
            result = await next_directive(parent_node, value, ctx)
            ctx["went_through"].append(
                f"wentThrough.on_post_enum_value_input_coercion {directive_args['over']}"
            )
            return result

        @staticmethod
        async def on_post_input_coercion(
            directive_args,
            next_directive,
            parent_node,
            input_definition_node,
            value,
            ctx,
        ):
            result = await next_directive(
                parent_node, input_definition_node, value, ctx
            )
            ctx["went_through"].append(
                f"wentThrough.on_post_input_coercion {directive_args['over']}"
            )
            return result

        @staticmethod
        async def on_field_execution(
            directive_args, next_resolver, parent, args, ctx, info,
        ):
            result = await next_resolver(parent, args, ctx, info)
            ctx["went_through"].append(
                f"wentThrough.on_field_execution {directive_args['over']}"
            )
            return result

        @staticmethod
        async def on_pre_output_coercion(
            directive_args, next_directive, value, ctx, info,
        ):
            result = await next_directive(value, ctx, info)
            ctx["went_through"].append(
                f"wentThrough.on_pre_output_coercion {directive_args['over']}"
            )
            return result

    @Resolver("Query.human", schema_name=schema_name)
    async def resolver_query_human(parent, args, ctx, info):
        return {"id": "1", "name": "Human", "gender": "FEMALE"}

    Scalar("DefaultRawString", schema_name=schema_name)(StringScalar())


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    directive @wentThrough(over: DefaultRawString!) on
      | SCHEMA
      | SCALAR
      | OBJECT
      | FIELD_DEFINITION
      | ARGUMENT_DEFINITION
      | INTERFACE
      | UNION
      | ENUM_VALUE
      | ENUM
      | INPUT_OBJECT
      | INPUT_FIELD_DEFINITION

    scalar DefaultRawString
    extend scalar String @wentThrough(over: "String")
    extend scalar ID @wentThrough(over: "ID")

    interface Identifiable @wentThrough(over: "Interface") {
      id: ID! @wentThrough(over: "Interface.id")
    }

    interface Named @wentThrough(over: "Named") {
      name: String! @wentThrough(over: "Named.name")
    }

    enum Gender @wentThrough(over: "Gender") {
      MALE @wentThrough(over: "Gender.MALE")
      FEMALE @wentThrough(over: "Gender.FEMALE")
    }

    type Human implements Identifiable & Named @wentThrough(over: "Human") {
      id: ID! @wentThrough(over: "Human.id")
      name: String! @wentThrough(over: "Human.name")
      gender: Gender! @wentThrough(over: "Human.gender")
    }

    input TextFilter @wentThrough(over: "TextFilter") {
      startsWith: String @wentThrough(over: "TextFilter.startsWith")
      equals: String @wentThrough(over: "TextFilter.equals")
    }

    input HumanFilter @wentThrough(over: "HumanFilter") {
      id: ID! @wentThrough(over: "HumanFilter.id")
      name: TextFilter @wentThrough(over: "HumanFilter.name")
      gender: Gender @wentThrough(over: "HumanFilter.gender")
    }

    type Query @wentThrough(over: "Query") {
      human(
        filter: HumanFilter @wentThrough(over: "Query.human(filter:)")
      ): Human @wentThrough(over: "Query.human")
    }

    schema @wentThrough(over: "Schema") {
      query: Query
    }
    """,
    bakery=bakery,
)
@pytest.mark.parametrize(
    "query,variables,expected_response,expected_went_through",
    [
        (
            """
            {
              human(
                filter: {
                  id: "1",
                  name: {
                    equals: "Human"
                  },
                  gender: FEMALE,
                }
              ) {
                id
                name
                gender
              }
            }
            """,
            {},
            {
                "data": {
                    "human": {"id": "1", "name": "Human", "gender": "FEMALE"}
                }
            },
            [
                "wentThrough.on_post_scalar_input_coercion ID",
                "wentThrough.on_post_enum_value_input_coercion Gender.FEMALE",
                "wentThrough.on_post_scalar_input_coercion String",
                "wentThrough.on_post_input_field_coercion HumanFilter.id",
                "wentThrough.on_post_enum_type_input_coercion Gender",
                "wentThrough.on_post_input_field_coercion TextFilter.equals",
                "wentThrough.on_post_input_field_coercion HumanFilter.gender",
                "wentThrough.on_post_input_object_coercion TextFilter",
                "wentThrough.on_post_input_field_coercion HumanFilter.name",
                "wentThrough.on_post_input_object_coercion HumanFilter",
                "wentThrough.on_post_argument_coercion Query.human(filter:)",
                "wentThrough.on_field_execution Query.human",
                "wentThrough.on_pre_output_coercion Human",
                "wentThrough.on_field_execution Human.id",
                "wentThrough.on_field_execution Human.gender",
                "wentThrough.on_field_execution Human.name",
                "wentThrough.on_pre_output_coercion ID",
                "wentThrough.on_pre_output_coercion Gender",
                "wentThrough.on_pre_output_coercion String",
                "wentThrough.on_pre_output_coercion Gender.FEMALE",
                "wentThrough.on_schema_execution Schema",
            ],
        ),
        (
            """
            query ($filter: HumanFilter!) {
              human(filter: $filter) {
                id
                name
                gender
              }
            }
            """,
            {
                "filter": {
                    "id": "1",
                    "name": {"equals": "Human",},
                    "gender": "FEMALE",
                },
            },
            {
                "data": {
                    "human": {"id": "1", "name": "Human", "gender": "FEMALE"}
                }
            },
            [
                "wentThrough.on_post_scalar_input_coercion ID",
                "wentThrough.on_post_enum_value_input_coercion Gender.FEMALE",
                "wentThrough.on_post_scalar_input_coercion String",
                "wentThrough.on_post_input_field_coercion HumanFilter.id",
                "wentThrough.on_post_enum_type_input_coercion Gender",
                "wentThrough.on_post_input_field_coercion TextFilter.equals",
                "wentThrough.on_post_input_field_coercion HumanFilter.gender",
                "wentThrough.on_post_input_object_coercion TextFilter",
                "wentThrough.on_post_input_field_coercion HumanFilter.name",
                "wentThrough.on_post_input_object_coercion HumanFilter",
                "wentThrough.on_post_argument_coercion Query.human(filter:)",
                "wentThrough.on_field_execution Query.human",
                "wentThrough.on_pre_output_coercion Human",
                "wentThrough.on_field_execution Human.name",
                "wentThrough.on_field_execution Human.gender",
                "wentThrough.on_field_execution Human.id",
                "wentThrough.on_pre_output_coercion String",
                "wentThrough.on_pre_output_coercion Gender",
                "wentThrough.on_pre_output_coercion ID",
                "wentThrough.on_pre_output_coercion Gender.FEMALE",
                "wentThrough.on_schema_execution Schema",
            ],
        ),
    ],
)
async def test_directives_went_through(
    schema_stack, query, variables, expected_response, expected_went_through
):
    ctx = {"went_through": []}
    assert (
        await schema_stack.execute(query, context=ctx, variables=variables)
        == expected_response
    )
    assert_unordered_lists(ctx["went_through"], expected_went_through)
