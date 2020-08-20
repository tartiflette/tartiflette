import pytest

from tartiflette import Resolver


def bakery(schema_name):
    @Resolver("Query.hello", schema_name=schema_name)
    @Resolver("Query.world", schema_name=schema_name)
    async def resolve_query_world(*_):
        return "World"

    @Resolver("Mutation.world", schema_name=schema_name)
    async def resolve_mutation_world(*_):
        return "World"

    @Resolver("Subscription.world", schema_name=schema_name)
    async def resolve_subscription_world(*_):
        return "World"


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    type Query {
      hello: String
    }

    type Mutation {
      hello: String
    }

    type Subscription {
      hello: String
    }

    extend type Query {
      world: String
    }

    extend type Mutation {
      world: String
    }

    extend type Subscription {
      world: String
    }
    """,
    bakery=bakery,
)
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query {
              world
            }
            """,
            {"data": {"world": "World"}},
        ),
        (
            """
            mutation {
              world
            }
            """,
            {"data": {"world": "World"}},
        ),
    ],
)
async def test_issue292(schema_stack, query, expected):
    assert await schema_stack.execute(query) == expected
