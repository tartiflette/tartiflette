import pytest

from tartiflette import Resolver


def bakery(schema_name):
    @Resolver("Query.aField", schema_name=schema_name)
    async def resolve_query_a_field(parent, args, ctx, info):
        nb_items = args["nbItems"]
        return [f"{nb_items}.{i}" for i in range(nb_items)]


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    type Query {
      aField(nbItems: Int = 2): [String!]
    }
    """,
    bakery=bakery,
)
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
async def test_issue207(schema_stack, query, variables, expected):
    assert await schema_stack.execute(query, variables=variables) == expected
