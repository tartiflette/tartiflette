import pytest


async def _query_human_resolver(parent_result, *_args, **__kwargs):
    if not parent_result:
        parent_result = {}
    return {"name": parent_result.get("name", "Hooman")}


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(resolvers={"Query.human": _query_human_resolver})
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
async def test_issue119(engine, query, initial_value, expected):
    assert await engine.execute(query, initial_value=initial_value) == expected
