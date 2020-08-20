import pytest

from tartiflette import Resolver


def bakery(schema_name):
    @Resolver("Query.aList", schema_name=schema_name)
    async def resolve_query_a_list(_parent, args, _ctx, _info):
        max_value = args["input"].get("maxValue")
        return [
            str(i if max_value is None or i <= max_value else max_value)
            for i in range(1, args["input"]["limit"] + 1)
        ]


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    input ListInput {
      limit: Int! = 3
      maxValue: Int
    }

    type Query {
      aList(input: ListInput): [String]
    }
    """,
    bakery=bakery,
)
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
async def test_issue188(schema_stack, query, data):
    assert await schema_stack.execute(query) == data
