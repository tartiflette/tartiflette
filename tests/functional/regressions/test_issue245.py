import json
import os

import pytest

from tartiflette import Resolver, create_engine


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Resolver("Query.test", schema_name="issue245")
    async def resolver_test(*args, **kwargs):
        return True

    return await create_engine(
        sdl=f"{os.path.dirname(__file__)}/sdl/issue245.sdl",
        schema_name="issue245",
    )


@pytest.mark.asyncio
async def test_issue245(ttftt_engine):
    assert await ttftt_engine.execute("query { test }") == {
        "data": {"test": True}
    }

    assert await ttftt_engine.execute(
        'query { __type(name: "Query") { description name fields { name description } } }'
    ) == {
        "data": {
            "__type": {
                "description": None,
                "name": "Query",
                "fields": [{"name": "test", "description": "тест"}],
            }
        }
    }
