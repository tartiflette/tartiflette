import pytest

from tartiflette import Resolver, create_engine
from tartiflette.resolver.default import (
    gather_arguments_coercer,
    sync_arguments_coercer,
)


@pytest.fixture(scope="module")
async def ttftt_engine():
    sdl = """
    type Query {
      helloDefault(firstName: String!, lastName: String!): String!
      helloGather(firstName: String!, lastName: String!): String!
      helloSync(firstName: String!, lastName: String!): String!
      helloCustom(firstName: String!, lastName: String!): String!
    }
    """

    async def default_arguments_coercer(*coroutines):
        return [i for i in range(len(coroutines))]

    async def custom_arguments_coercer(*coroutines):
        return [i + 2 for i in range(len(coroutines))]

    @Resolver("Query.helloDefault", schema_name="test_issue361")
    @Resolver(
        "Query.helloGather",
        schema_name="test_issue361",
        arguments_coercer=gather_arguments_coercer,
    )
    @Resolver(
        "Query.helloSync",
        schema_name="test_issue361",
        arguments_coercer=sync_arguments_coercer,
    )
    @Resolver(
        "Query.helloCustom",
        schema_name="test_issue361",
        arguments_coercer=custom_arguments_coercer,
    )
    async def resolver_query_hello_default(parent, args, ctx, info):
        return f"Hello {args['firstName']} {args['lastName']}"

    return await create_engine(
        sdl,
        custom_default_arguments_coercer=default_arguments_coercer,
        schema_name="test_issue361",
    )


@pytest.mark.asyncio
async def test_issue361(ttftt_engine):
    assert (
        await ttftt_engine.execute(
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
