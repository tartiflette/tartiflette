import pytest

from tartiflette import Resolver

_CACHE = {}


def my_query_cache_decorator(func):
    def wrapper(query, schema):
        query_hash = hash(query)
        cached_query = _CACHE.get(query_hash)
        if cached_query:
            return cached_query

        result = func(query, schema)
        _CACHE[query_hash] = result
        return result

    return wrapper


def bakery(schema_name):
    @Resolver("Query.hello", schema_name=schema_name)
    async def resolve_query_world(parent, args, ctx, info):
        return f"Hello {args['name']}"


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    type Query {
      hello(name: String!): String
    }
    """,
    bakery=bakery,
    query_cache_decorator=my_query_cache_decorator,
)
async def test_issue363(schema_stack):
    query = """
    query {
      hello(name: "John")
    }
    """

    assert _CACHE == {}
    assert await schema_stack.execute(query) == {
        "data": {"hello": "Hello John"}
    }
    assert hash(query) in _CACHE
