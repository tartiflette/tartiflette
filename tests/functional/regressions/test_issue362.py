import json as json_module
import logging

import pytest

from tartiflette import Resolver, create_engine

logger = logging.getLogger(__name__)

_CALLED = False


@pytest.fixture(scope="module")
async def ttftt_engine():
    sdl = """
    type Query {
      hello(name: String!): String
    }
    """

    @Resolver("Query.hello", schema_name="test_issue362")
    async def resolve_query_world(parent, args, ctx, info):
        return f"Hello {args['name']}"

    def my_loader(a_str, *_args, **_kwargs):
        global _CALLED
        _CALLED = True
        return json_module.loads(a_str)

    return await create_engine(
        sdl, schema_name="test_issue362", json_loader=my_loader
    )


@pytest.mark.asyncio
async def test_issue362(ttftt_engine):
    query = """
    query {
      hello(name: "John")
    }
    """
    expected = {"data": {"hello": "Hello John"}}

    assert not _CALLED
    assert await ttftt_engine.execute(query) == expected
    assert _CALLED
