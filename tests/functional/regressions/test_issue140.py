import pytest

from tartiflette import Resolver, create_engine

_SDL = """
type A {
    b: String
    c: String
}

type Query {
    a: A
}
"""


@pytest.mark.asyncio
async def test_issue140():
    @Resolver("Query.a", schema_name="test_issue140")
    async def resolver_query_a(*args, **kwargs):
        return {"b": "mpm", "c": "ppp"}

    eng = await create_engine(
        _SDL,
        schema_name="test_issue140",
        modules=[
            "tests.functional.test_engine_modules",
            "tests.functional.test_engine_modules.non_init_resolver",
        ],
    )
    assert await eng.execute("""query { a { b c } }""") == {
        "data": {"a": {"b": "A.b", "c": "A.c"}}
    }


@pytest.mark.asyncio
async def test_issue140_except():
    with pytest.raises(ImportError):
        await create_engine("""a""", modules=["unkn.nown.modules"])
