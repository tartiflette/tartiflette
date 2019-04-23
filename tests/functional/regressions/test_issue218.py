import pytest

from tartiflette import Engine, Resolver

_SDL = """
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
"""


@Resolver("Mutation.listFailure", schema_name="test_issue218")
@Resolver("Mutation.listScalar", schema_name="test_issue218")
async def list_failure(parent, args, ctx, info):
    return {"result": str(args)}


_ENGINE = Engine(sdl=_SDL, schema_name="test_issue218")


@pytest.mark.asyncio
async def test_issue218_input():
    assert (
        await _ENGINE.execute(
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
}"""
        )
        == {
            "data": {
                "listFailure": {
                    "result": "{'input': [{'a': 3, 'b': 4}, {'a': 5, 'b': 6}]}"
                }
            }
        }
    )


@pytest.mark.asyncio
async def test_issue218_scalar():
    assert (
        await _ENGINE.execute(
            """
mutation {
  listScalar(input: [
    1, 2, 3, 6
  ]) {
    result
  }
}"""
        )
        == {"data": {"listScalar": {"result": "{'input': [1, 2, 3, 6]}"}}}
    )
