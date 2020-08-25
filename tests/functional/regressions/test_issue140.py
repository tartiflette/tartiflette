import pytest

from tartiflette import Resolver, create_schema


def bakery(schema_name):
    @Resolver("Query.a", schema_name=schema_name)
    async def resolver_query_a(*args, **kwargs):
        return {"b": "mpm", "c": "ppp"}


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    type A {
        b: String
        c: String
    }

    type Query {
        a: A
    }
    """,
    modules=[
        "tests.functional.test_schema_modules",
        "tests.functional.test_schema_modules.non_init_resolver",
    ],
    bakery=bakery,
)
async def test_issue140(schema_stack):
    assert await schema_stack.execute("""query { a { b c } }""") == {
        "data": {"a": {"b": "A.b", "c": "A.c"}}
    }


@pytest.mark.asyncio
async def test_issue140_except():
    with pytest.raises(ImportError):
        await create_schema(
            """a""", name="test_issue140_except", modules=["unkn.nown.modules"]
        )
