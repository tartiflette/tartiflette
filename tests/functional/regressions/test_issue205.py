import pytest

from tartiflette import Engine, Resolver


@Resolver("Mutation.addEntry", schema_name="test_issue205")
async def resolver_mutation_add_entry(parent, args, ctx, info):
    return {"clientMutationId": args["input"].get("clientMutationId")}


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


_TTFTT_ENGINE = Engine(_SDL, schema_name="test_issue205")


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
async def test_issue205(query, variables, expected):
    assert await _TTFTT_ENGINE.execute(query, variables=variables) == expected
