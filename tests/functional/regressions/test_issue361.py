import pytest

from tartiflette import Resolver
from tartiflette.resolver.default import (
    gather_arguments_coercer,
    sync_arguments_coercer,
)


async def default_arguments_coercer(*coroutines):
    [await x for x in coroutines]
    return [i for i in range(len(coroutines))]


def bakery(schema_name):
    async def custom_arguments_coercer(*coroutines):
        [await x for x in coroutines]
        return [i + 2 for i in range(len(coroutines))]

    @Resolver("Query.helloDefault", schema_name=schema_name)
    @Resolver(
        "Query.helloGather",
        schema_name=schema_name,
        arguments_coercer=gather_arguments_coercer,
    )
    @Resolver(
        "Query.helloSync",
        schema_name=schema_name,
        arguments_coercer=sync_arguments_coercer,
    )
    @Resolver(
        "Query.helloCustom",
        schema_name=schema_name,
        arguments_coercer=custom_arguments_coercer,
    )
    async def resolver_query_hello_default(parent, args, ctx, info):
        return f"Hello {args['firstName']} {args['lastName']}"


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    type Query {
      helloDefault(firstName: String!, lastName: String!): String!
      helloGather(firstName: String!, lastName: String!): String!
      helloSync(firstName: String!, lastName: String!): String!
      helloCustom(firstName: String!, lastName: String!): String!
    }
    """,
    default_arguments_coercer=default_arguments_coercer,
    bakery=bakery,
)
async def test_issue361(schema_stack):
    assert (
        await schema_stack.execute(
            """
            query ($firstName: String!, $lastName: String!) {
              helloDefault(firstName: $firstName, lastName: $lastName)
              helloGather(firstName: $firstName, lastName: $lastName)
              helloSync(firstName: $firstName, lastName: $lastName)
              helloCustom(firstName: $firstName, lastName: $lastName)
            }
            """,
            variables={"firstName": "John", "lastName": "Doe"},
        )
        == {
            "data": {
                "helloDefault": "Hello 0 1",
                "helloGather": "Hello John Doe",
                "helloSync": "Hello John Doe",
                "helloCustom": "Hello 2 3",
            }
        }
    )
