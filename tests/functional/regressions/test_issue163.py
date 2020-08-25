import pytest

from tartiflette import Resolver


def bakery(schema_name):
    @Resolver("Query.dog", schema_name=schema_name)
    async def resolver_query_dog(*args, **kwargs):
        return {"name": "a", "nickname": "b"}


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="animals", bakery=bakery)
async def test_issue163(schema_stack):
    assert await schema_stack.execute(
        "query { dog { ... { name nickname }} }"
    ) == {"data": {"dog": {"name": "a", "nickname": "b"}}}
