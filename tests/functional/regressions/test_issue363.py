import logging

import pytest

from tartiflette import Resolver, create_engine

logger = logging.getLogger(__name__)

_CACHE = {}


@pytest.fixture(scope="module")
async def ttftt_engine():
    sdl = """
    type Query {
      hello(name: String!): String
    }
    """

    @Resolver("Query.hello", schema_name="test_issue363")
    async def resolve_query_world(parent, args, ctx, info):
        return f"Hello {args['name']}"

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

    return await create_engine(
        sdl,
        query_cache_decorator=my_query_cache_decorator,
        schema_name="test_issue363",
    )


@pytest.mark.asyncio
async def test_issue363(ttftt_engine):
    query = """
    query {
      hello(name: "John")
    }
    """
    expected = {"data": {"hello": "Hello John"}}

    assert _CACHE == {}
    assert await ttftt_engine.execute(query) == expected
    assert hash(query) in _CACHE
