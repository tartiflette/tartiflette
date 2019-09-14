import pytest

from tartiflette import Resolver, create_engine


@pytest.fixture(scope="module")
async def ttftt_engine():
    sdl = """
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
    """

    @Resolver("Query.hello", schema_name="test_issue292")
    @Resolver("Query.world", schema_name="test_issue292")
    async def resolve_query_world(*_):
        return "World"

    @Resolver("Mutation.world", schema_name="test_issue292")
    async def resolve_mutation_world(*_):
        return "World"

    @Resolver("Subscription.world", schema_name="test_issue292")
    async def resolve_subscription_world(*_):
        return "World"

    return await create_engine(sdl, schema_name="test_issue292")


@pytest.mark.asyncio
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
async def test_issue292(query, expected, ttftt_engine):
    assert await ttftt_engine.execute(query) == expected
