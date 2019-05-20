import pytest

from tartiflette import Engine, Resolver


@pytest.mark.asyncio
async def test_issue228_1():
    @Resolver("Query.a", schema_name="issue228_1")
    async def lol(*_args, **_kwargs):
        return {"ninja": "Ohio"}

    _engine = Engine(
        sdl="""

            type Query {
                a: Lol
            }""",
        modules=[
            {
                "name": "tests.functional.regressions.issue228.a_module",
                "config": {"val": "Blah!!"},
            }
        ],
        schema_name="issue228_1",
    )

    assert await _engine.execute("query aquery { a { ninja } }") == {
        "data": {"a": {"ninja": "Ohio Ninja Blah!!GO !"}}
    }


def test_issue228_2():
    import asyncio

    @Resolver("Query.a", schema_name="issue228_2")
    async def lol(*_args, **_kwargs):
        return {"ninja": "Ohio"}

    _engine = Engine(
        sdl="""

            type Query {
                a: Lol
            }""",
        modules=[
            {
                "name": "tests.functional.regressions.issue228.b_module",
                "config": {"val": "Blah!!"},
            }
        ],
        schema_name="issue228_2",
    )

    assert asyncio.get_event_loop().run_until_complete(
        _engine.execute("query aquery { a { ninja } }")
    ) == {"data": {"a": {"ninja": "Ohio NinjaB BBlah!!GO !B"}}}
