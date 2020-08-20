import pytest

from tartiflette import Resolver


def bakery(schema_name):
    @Resolver("Query.simpleParameterField", schema_name=schema_name)
    async def resolver(_pr, args, _ctx, _info):
        return str(args)


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    type Query {
        simpleParameterField(s: String): String
    }
    """,
    bakery=bakery,
)
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query {
                simpleParameterField(s:\"\"\"a\"\"\")
            }
            """,
            {"data": {"simpleParameterField": "{'s': 'a'}"}},
        ),
        (
            """
            query {
                simpleParameterField(s:\"\"\"a


                b\"\"\")
            }
            """,
            {"data": {"simpleParameterField": "{'s': 'a\\n\\n\\nb'}"}},
        ),
    ],
)
async def test_validators_all_variable_usages_are_allowed(
    schema_stack, query, expected
):
    assert await schema_stack.execute(query) == expected
