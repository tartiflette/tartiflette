import pytest

from tartiflette import Resolver, create_engine


@pytest.fixture(scope="module", name="ttftt_engine")
async def ttftt_engine_fixture():
    sdl = """
type Query {
    simpleParameterField(s: String): String
}
"""

    @Resolver(
        "Query.simpleParameterField",
        schema_name="test_regressions_multiline_strings",
    )
    async def resolver(_pr, args, _ctx, _info):
        return str(args)

    return await create_engine(
        sdl, schema_name="test_regressions_multiline_strings"
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
@pytest.mark.asyncio
async def test_validators_all_variable_usages_are_allowed(
    query, expected, ttftt_engine
):
    assert await ttftt_engine.execute(query) == expected
