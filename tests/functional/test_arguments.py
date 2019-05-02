import pytest

from tartiflette import Engine, Resolver


@pytest.mark.parametrize(
    "sdl,query,expected,varis",
    [
        (
            "type Query { bob(id: Int = 45): Int }",
            "query aQuery { bob }",
            {"data": {"bob": 47}},
            None,
        ),
        (
            "type Query { bob(id: Int = 45): Int }",
            "query aQuery { bob(id: 27) }",
            {"data": {"bob": 29}},
            None,
        ),
        (
            "type Query { bob(id: Int = 45): Int }",
            "query aQuery($lol: Int) { bob(id: $lol) }",
            {"data": {"bob": 47}},
            None,
        ),
        (
            "type Query { bob(id: Int = 45): Int }",
            "query aQuery($lol: Int) { bob(id: $lol) }",
            {"data": {"bob": 58}},
            {"lol": 56},
        ),
        (
            "type Query { bob(id: Int = 45): Int }",
            "query aQuery($lol: Int = 98) { bob(id: $lol) }",
            {"data": {"bob": 100}},
            None,
        ),
        (
            "type Query { bob(id: Int = 45): Int }",
            "query aQuery($lol: Int = 10) { bob(id: $lol) }",
            {"data": {"bob": 26}},
            {"lol": 24},
        ),
    ],
)
@pytest.mark.asyncio
async def test_arguments_in_sdl(sdl, query, expected, varis, clean_registry):
    @Resolver("Query.bob")
    async def resolve_query_bob(_pr, arguments, _ctx, _info):
        return arguments["id"] + 2

    ttftt = Engine(sdl)

    result = await ttftt.execute(
        query, variables=varis, operation_name="aQuery"
    )

    assert expected == result
