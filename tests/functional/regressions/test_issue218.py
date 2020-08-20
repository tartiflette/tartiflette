import pytest

from tartiflette import Resolver


def bakery(schema_name):
    @Resolver("Mutation.listFailure", schema_name=schema_name)
    @Resolver("Mutation.listScalar", schema_name=schema_name)
    async def list_failure(parent, args, ctx, info):
        return {"result": str(args)}


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    type Mutation {
      listFailure(input: [FailureInput!]!): FailureResult
      listScalar(input: [Int!]!): FailureResult
    }

    type FailureResult {
      result: String!
    }

    input FailureInput {
      a: Int!
      b: Int!
    }

    type Query {
        michel: FailureResult
    }
    """,
    bakery=bakery,
)
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
        mutation {
          listFailure(input: [
            {
              a: 3,
              b: 4
            },
            {
              a: 5,
              b: 6
            }
          ]) {
            result
          }
        }
        """,
            {
                "data": {
                    "listFailure": {
                        "result": "{'input': [{'a': 3, 'b': 4}, {'a': 5, 'b': 6}]}"
                    }
                }
            },
        ),
        (
            """
        mutation {
          listScalar(input: [
            1, 2, 3, 6
          ]) {
            result
          }
        }
        """,
            {"data": {"listScalar": {"result": "{'input': [1, 2, 3, 6]}"}}},
        ),
    ],
)
async def test_issue218(schema_stack, query, expected):
    assert await schema_stack.execute(query) == expected
