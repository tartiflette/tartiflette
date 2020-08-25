import pytest

from tartiflette import Resolver


def bakery(schema_name):
    @Resolver("Query.bothTypesField", schema_name=schema_name)
    async def resolve_query_both_types_field(*_, **__):
        return {"_typename": "FirstType", "id": 1, "firstField": "firstField"}


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
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
    """,
    bakery=bakery,
)
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
async def test_issue_235(schema_stack, query, expected):
    assert await schema_stack.execute(query) == expected
