import pytest

from tartiflette import Resolver, create_engine

_SDL = """
type Query {
  aField(nbItems: Int = 2): [String!]
}
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Resolver("Query.aField", schema_name="test_issue207")
    async def resolve_query_a_field(parent, args, ctx, info):
        nb_items = args["nbItems"]
        return [f"{nb_items}.{i}" for i in range(nb_items)]

    return await create_engine(sdl=_SDL, schema_name="test_issue207")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """
            query AField {
              aField(nbItems: 3)
            }
            """,
            None,
            {"data": {"aField": ["3.0", "3.1", "3.2"]}},
        ),
        (
            """
            query AField {
              aField
            }
            """,
            None,
            {"data": {"aField": ["2.0", "2.1"]}},
        ),
        (
            """
            query AField($nbItems: Int) {
              aField(nbItems: $nbItems)
            }
            """,
            {"nbItems": 3},
            {"data": {"aField": ["3.0", "3.1", "3.2"]}},
        ),
        (
            """
            query AField($nbItems: Int) {
              aField(nbItems: $nbItems)
            }
            """,
            None,
            {"data": {"aField": ["2.0", "2.1"]}},
        ),
    ],
)
async def test_issue207(query, variables, expected, ttftt_engine):
    assert await ttftt_engine.execute(query, variables=variables) == expected
