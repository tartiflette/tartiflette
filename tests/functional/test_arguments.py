import pytest

from tartiflette import Resolver


def bakery(schema_name):
    @Resolver("Query.bob", schema_name=schema_name)
    async def func_bob_resolver(_pr, arguments, _ctx, _info):
        return arguments["id"] + 2


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    type Query {
      bob(id: Int = 45): Int
    }
    """,
    bakery=bakery,
)
@pytest.mark.parametrize(
    "query,expected,variables",
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
async def test_arguments_in_sdl(schema_stack, query, expected, variables):
    assert (
        await schema_stack.execute(
            query, variables=variables, operation_name="aQuery"
        )
        == expected
    )
