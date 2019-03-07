import pytest

from tartiflette.engine import Engine
from tartiflette.resolver import Resolver

_SDL = """
type A {
    b: String
    c: String
}

type Query {
    a: A
}
"""


@Resolver("Query.a", schema_name="test_issue140")
async def resolver_query_a(*args, **kwargs):
    return {"b": "mpm", "c": "ppp"}


_ENGINE = Engine(
    _SDL,
    schema_name="test_issue140",
    modules=[
        "tests.functional.test_engine_modules",
        "tests.functional.test_engine_modules.non_init_resolver",
    ],
)


@pytest.mark.asyncio
async def test_issue140():
    assert await _ENGINE.execute("""query { a { b c } }""") == {
        "data": {"a": {"b": "A.b", "c": "A.c"}}
    }


@pytest.mark.asyncio
async def test_issue140_except():
    with pytest.raises(ImportError):
        Engine("""a""", modules=["unkn.nown.modules"])
