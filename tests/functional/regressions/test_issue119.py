import pytest

from tartiflette import Resolver


def bakery(schema_name):
    @Resolver("Query.human", schema_name=schema_name)
    async def resolve_query_human(parent, *_args, **__kwargs):
        if not parent:
            parent = {}
        return {"name": parent.get("name", "Hooman")}


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="animals", bakery=bakery)
@pytest.mark.parametrize(
    "query,initial_value,expected",
    [
        (
            """
            query {
              human(id: 1) {
                name
              }
            }
            """,
            None,
            {"data": {"human": {"name": "Hooman"}}},
        ),
        (
            """
            query {
              human(id: 1) {
                name
              }
            }
            """,
            {},
            {"data": {"human": {"name": "Hooman"}}},
        ),
        (
            """
            query {
              human(id: 1) {
                name
              }
            }
            """,
            {"name": "Boris"},
            {"data": {"human": {"name": "Boris"}}},
        ),
    ],
)
async def test_issue119(schema_stack, query, initial_value, expected):
    assert (
        await schema_stack.execute(query, initial_value=initial_value)
        == expected
    )
