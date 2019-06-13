import pytest

from tartiflette import Resolver, create_engine

_SDL = """
type FirstType {
  id: Int!
  firstField: String
}

type SecondType {
  id: Int!
  secondField: String
}

union BothTypes = FirstType | SecondType

type Query {
  bothTypesField: BothTypes
}
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Resolver("Query.bothTypesField", schema_name="test_issue_235")
    async def resolve_query_both_types_field(*_, **__):
        return {"_typename": "FirstType", "id": 1, "firstField": "firstField"}

    return await create_engine(_SDL, schema_name="test_issue_235")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            {
              bothTypesField {
                ... on FirstType {
                  __typename
                  id
                  firstField
                }
                ... on SecondType {
                  __typename
                  id
                  secondField
                }
              }
            }
            """,
            {
                "data": {
                    "bothTypesField": {
                        "__typename": "FirstType",
                        "id": 1,
                        "firstField": "firstField",
                    }
                }
            },
        ),
        (
            """
            fragment FirstTypeFields on FirstType {
              __typename
              id
              firstField
            }

            fragment SecondTypeFields on SecondType {
              __typename
              id
              secondField
            }

            {
              bothTypesField {
                ...FirstTypeFields
                ...SecondTypeFields
              }
            }
            """,
            {
                "data": {
                    "bothTypesField": {
                        "__typename": "FirstType",
                        "id": 1,
                        "firstField": "firstField",
                    }
                }
            },
        ),
        (
            """
            {
              bothTypesField {
                __typename
                ... on FirstType {
                  id
                  firstField
                }
                ... on SecondType {
                  id
                  secondField
                }
              }
            }
            """,
            {
                "data": {
                    "bothTypesField": {
                        "__typename": "FirstType",
                        "id": 1,
                        "firstField": "firstField",
                    }
                }
            },
        ),
        (
            """
            fragment FirstTypeFields on FirstType {
              id
              firstField
            }

            fragment SecondTypeFields on SecondType {
              id
              secondField
            }

            {
              bothTypesField {
                __typename
                ...FirstTypeFields
                ...SecondTypeFields
              }
            }
            """,
            {
                "data": {
                    "bothTypesField": {
                        "__typename": "FirstType",
                        "id": 1,
                        "firstField": "firstField",
                    }
                }
            },
        ),
    ],
)
async def test_issue_235(query, expected, ttftt_engine):
    assert await ttftt_engine.execute(query) == expected
