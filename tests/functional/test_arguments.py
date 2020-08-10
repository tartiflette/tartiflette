import pytest

from tartiflette import Resolver, create_engine


@Resolver("Query.bob", schema_name="test_arguments")
async def func_bob_resolver(_pr, arguments, _ctx, _info):
    return arguments["id"] + 2


_SDL = """
type Query {
    bob(id: Int = 45): Int
}
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    return await create_engine(sdl=_SDL, schema_name="test_arguments")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,expected,varis",
    [
        ("query aQuery{ bob }", {"data": {"bob": 47}}, {}),
        ("query aQuery{ bob(id: 27) }", {"data": {"bob": 29}}, {}),
        (
            "query aQuery($lol: Int) { bob(id: $lol) }",
            {"data": {"bob": 58}},
            {"lol": 56},
        ),
        (
            "query aQuery($lol: Int = 98) { bob(id: $lol) }",
            {"data": {"bob": 100}},
            {},
        ),
    ],
)
async def test_arguments_in_sdl(query, expected, varis, ttftt_engine):
    result = await ttftt_engine.execute(
        query, variables=varis, operation_name="aQuery"
    )

    assert expected == result
