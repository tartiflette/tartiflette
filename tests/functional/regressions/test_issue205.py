import pytest

from tartiflette import Resolver, create_engine

_SDL = """
type Entry {
  id: Int!
  name: String!
}

input SubSubEntry {
  name: String!
}

input SubEntryInput {
  name: String!
  subSubEntry: SubSubEntry
}

input AddEntryInput {
  clientMutationId: String
  subEntry1: SubEntryInput!
  subEntry2: SubEntryInput!
}

type AddEntryPayload {
  clientMutationId: String
}

type Query {
  entry(id: Int!): Entry!
}

type Mutation {
  addEntry(input: AddEntryInput!): AddEntryPayload!
}
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Resolver("Mutation.addEntry", schema_name="test_issue205")
    async def resolver_mutation_add_entry(parent, args, ctx, info):
        return {"clientMutationId": args["input"].get("clientMutationId")}

    return await create_engine(sdl=_SDL, schema_name="test_issue205")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """
            mutation AddEntry($input: AddEntryInput!) {
              addEntry(input: $input) {
               clientMutationId
              }
            }
            """,
            {
                "input": {
                    "clientMutationId": "addEntryId",
                    "subEntry1": {"name": "Entry1", "subSubEntry": None},
                    "subEntry2": {"name": "Entry1", "subSubEntry": None},
                }
            },
            {"data": {"addEntry": {"clientMutationId": "addEntryId"}}},
        ),
        (
            """
            mutation AddEntry {
              addEntry(input: {
                clientMutationId: "addEntryId",
                subEntry1: {
                    name: "Entry1",
                    subSubEntry: null
                },
                subEntry2: {
                    name: "Entry1",
                    subSubEntry: null
                }
            }) {
               clientMutationId
              }
            }
            """,
            None,
            {"data": {"addEntry": {"clientMutationId": "addEntryId"}}},
        ),
    ],
)
async def test_issue205(query, variables, expected, ttftt_engine):
    assert await ttftt_engine.execute(query, variables=variables) == expected
