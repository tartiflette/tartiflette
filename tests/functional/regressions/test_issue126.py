import pytest


async def _query_human_resolver(parent, *_args, **__kwargs):
    return None


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
            {"data": {"human": None}},
        )
    ],
)
async def test_issue126(engine, query, initial_value, expected):
    assert await engine.execute(query, initial_value=initial_value) == expected
