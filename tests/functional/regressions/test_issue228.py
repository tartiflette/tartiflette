import pytest

from tartiflette import Engine, Resolver


@Resolver("Query.a", schema_name="issue228")
async def lol(*_args, **_kwargs):
    return {"ninja": "Ohio"}


_ENGINE = Engine(
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
    schema_name="issue228",
)


@pytest.mark.asyncio
async def test_issue228():
    assert await _ENGINE.execute("query aquery { a { ninja } }") == {
        "data": {"a": {"ninja": "Ohio Ninja Blah!!GO !"}}
    }
