import os

import pytest

from tartiflette import Resolver
from tests.data.utils import get_path_to_sdl


def bakery(schema_name):
    @Resolver("Query.test", schema_name=schema_name)
    async def resolver_test(*args, **kwargs):
        return True


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl=get_path_to_sdl("issue245.sdl"), bakery=bakery
)
async def test_issue245(schema_stack):
    assert await schema_stack.execute("query { test }") == {
        "data": {"test": True}
    }

    assert await schema_stack.execute(
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
