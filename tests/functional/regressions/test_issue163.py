import pytest


async def _resolver(*args, **kwargs):
    return {"name": "a", "nickname": "b"}


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(resolvers={"Query.dog": _resolver})
async def test_issue163(engine):
    assert await engine.execute("query { dog { ... { name nickname }} }") == {
        "data": {"dog": {"name": "a", "nickname": "b"}}
    }
