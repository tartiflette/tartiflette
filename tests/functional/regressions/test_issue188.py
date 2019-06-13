import pytest

from tartiflette import Resolver, create_engine

_SDL = """
input ListInput {
  limit: Int! = 3
  maxValue: Int
}

type Query {
  aList(input: ListInput): [String]
}
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Resolver("Query.aList", schema_name="test_issue188")
    async def resolve_query_a_list(_parent, args, _ctx, _info):
        max_value = args["input"].get("maxValue")
        return [
            str(i if max_value is None or i <= max_value else max_value)
            for i in range(1, args["input"]["limit"] + 1)
        ]

    return await create_engine(sdl=_SDL, schema_name="test_issue188")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,data",
    [
        (
            """
            query {
              aList(input: {
                limit: 2
              })
            }
            """,
            {"data": {"aList": ["1", "2"]}},
        ),
        (
            """
            query {
              aList(input: {
                limit: 4,
                maxValue: null,
              })
            }
            """,
            {"data": {"aList": ["1", "2", "3", "4"]}},
        ),
        (
            """
            query {
              aList(input: {
                limit: 4,
                maxValue: 3,
              })
            }
            """,
            {"data": {"aList": ["1", "2", "3", "3"]}},
        ),
    ],
)
async def test_issue188(query, data, ttftt_engine):
    assert await ttftt_engine.execute(query) == data
