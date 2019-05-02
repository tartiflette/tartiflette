import pytest


async def _query_human_resolver(*_args, **__kwargs):
    return {"name": "Hooman"}


@pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.ttftt_engine(resolvers={"Query.human": _query_human_resolver})
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query {
              human(id: 1) {
                name
              }
            }
            """,
            {"data": {"human": {"name": "Hooman"}}},
        ),
        (
            """
            query {
              human(id: 1) {
                name
                unknownField
              }
              dog {
                name
              }
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "field `Human.unknownField` was not found in GraphQL schema.",
                        "path": ["human", "unknownField"],
                        "locations": [{"line": 5, "column": 17}],
                    }
                ],
            },
        ),
        (
            """
            query {
              human(undefinedArgument: 1, id: 1) {
                unknownField
                name
              }
              dog {
                name
              }
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Undefined argument < undefinedArgument > on field < human > of type < Query >.",
                        "path": None,
                        "locations": [{"line": 3, "column": 21}],
                    },
                    {
                        "message": "field `Human.unknownField` was not found in GraphQL schema.",
                        "path": ["human", "unknownField"],
                        "locations": [{"line": 4, "column": 17}],
                    },
                ],
            },
        ),
        (
            """
            query {
              human(undefinedArgument: 1, id: 1) {
                unknownField
                name
              }
              unknownField {
                name
              }
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Undefined argument < undefinedArgument > on field < human > of type < Query >.",
                        "path": None,
                        "locations": [{"line": 3, "column": 21}],
                    },
                    {
                        "message": "field `Human.unknownField` was not found in GraphQL schema.",
                        "path": ["human", "unknownField"],
                        "locations": [{"line": 4, "column": 17}],
                    },
                    {
                        "message": "field `Query.unknownField` was not found in GraphQL schema.",
                        "path": ["unknownField"],
                        "locations": [{"line": 7, "column": 15}],
                    },
                ],
            },
        ),
        (
            """
            query {
              dog {
                doesKnowCommand(command: SIT)
              }
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Undefined argument < command > on field < doesKnowCommand > of type < Dog >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 33}],
                    },
                    {
                        "message": "Missing required < dogCommand > argument on < doesKnowCommand > field.",
                        "path": None,
                        "locations": [{"line": 4, "column": 17}],
                    },
                ],
            },
        ),
        (
            """
            fragment DogFields on Dog {
              ... on Dog {
                doesKnowCommand(command: SIT)
              }
            }
            query {
              dog {
                ...DogFields
              }
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Undefined argument < command > on field < doesKnowCommand > of type < Dog >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 33}],
                    },
                    {
                        "message": "Missing required < dogCommand > argument on < doesKnowCommand > field.",
                        "path": None,
                        "locations": [{"line": 4, "column": 17}],
                    },
                ],
            },
        ),
        (
            """
            query {
              unknownField1
              dog {
                doesKnowCommand(command: SIT) {
                  unknownField2
                }
                unknownField3
              }
              unknownField4
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "field `Query.unknownField1` was not found in GraphQL schema.",
                        "path": ["unknownField1"],
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "field < doesKnowCommand > is a leaf and thus can't have a selection set",
                        "path": ["dog", "doesKnowCommand"],
                        "locations": [{"line": 5, "column": 17}],
                    },
                    {
                        "message": "field `Dog.unknownField3` was not found in GraphQL schema.",
                        "path": ["dog", "unknownField3"],
                        "locations": [{"line": 8, "column": 17}],
                    },
                    {
                        "message": "field `Query.unknownField4` was not found in GraphQL schema.",
                        "path": ["unknownField4"],
                        "locations": [{"line": 10, "column": 15}],
                    },
                ],
            },
        ),
        (
            """
            fragment QueryFields on Query {
              unknownField1
            }

            fragment NestedDogFields on Dog {
              ... on Dog {
                doesKnowCommand(command: SIT) {
                  unknownField2
                }
              }
            }

            fragment DogFields on Dog {
              ...NestedDogFields
              unknownField3
            }

            query {
              ...QueryFields
              dog {
                ...DogFields
                unknownField4
              }
              unknownField5
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "field `Dog.unknownField4` was not found in GraphQL schema.",
                        "path": ["dog", "unknownField4"],
                        "locations": [{"line": 23, "column": 17}],
                    },
                    {
                        "message": "field `Query.unknownField5` was not found in GraphQL schema.",
                        "path": ["unknownField5"],
                        "locations": [{"line": 25, "column": 15}],
                    },
                    {
                        "message": "field `Query.unknownField1` was not found in GraphQL schema.",
                        "path": ["unknownField1"],
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "field `Dog.unknownField3` was not found in GraphQL schema.",
                        "path": ["dog", "unknownField3"],
                        "locations": [{"line": 16, "column": 15}],
                    },
                    {
                        "message": "field < doesKnowCommand > is a leaf and thus can't have a selection set",
                        "path": ["dog", "doesKnowCommand"],
                        "locations": [{"line": 8, "column": 17}],
                    },
                ],
            },
        ),
        (
            """
            fragment QueryFields on Query {
              unknownField1
            }

            fragment NestedDogFields on Dog {
              ... on Dog {
                doesKnowCommand(command: SIT) {
                  unknownField2 {
                    unknownField21
                  }
                }
              }
            }

            fragment DogFields on Dog {
              unknownField3
              ...NestedDogFields
            }

            query {
              ...QueryFields
              dog {
                ...DogFields
                unknownField4
              }
              unknownField5
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "field `Dog.unknownField4` was not found in GraphQL schema.",
                        "path": ["dog", "unknownField4"],
                        "locations": [{"line": 25, "column": 17}],
                    },
                    {
                        "message": "field `Query.unknownField5` was not found in GraphQL schema.",
                        "path": ["unknownField5"],
                        "locations": [{"line": 27, "column": 15}],
                    },
                    {
                        "message": "field `Query.unknownField1` was not found in GraphQL schema.",
                        "path": ["unknownField1"],
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "field `Dog.unknownField3` was not found in GraphQL schema.",
                        "path": ["dog", "unknownField3"],
                        "locations": [{"line": 17, "column": 15}],
                    },
                    {
                        "message": "field < doesKnowCommand > is a leaf and thus can't have a selection set",
                        "path": ["dog", "doesKnowCommand"],
                        "locations": [{"line": 8, "column": 17}],
                    },
                ],
            },
        ),
        (
            """
            fragment QueryFields on Query {
              unknownField1
            }

            fragment NestedDogFields on Dog {
              ... on Dog {
                doesKnowCommandDown: doesKnowCommand(dogCommand: DOWN)
                doesKnowCommandSitError: doesKnowCommand(command: SIT) {
                  unknownField2 @deprecated(undefinedArgument: "undefined") {
                    unknownField21
                  }
                }
                doesKnowCommandHeel: doesKnowCommand(dogCommand: HEEL) @deprecated(undefinedArgument: "undefined")
                doesKnowCommandSit: doesKnowCommand(dogCommand: SIT)
              }
            }

            fragment DogFields on Dog {
              unknownField3
              ...NestedDogFields
            }

            query {
              ...QueryFields
              dog {
                doesKnowCommandUndefinedArgument: doesKnowCommand(undefinedArgument: "undefined", dogCommand: SIT)
                ...DogFields
                unknownField4
                doesKnowCommandHeel: doesKnowCommand(dogCommand: HEEL) @deprecated(undefinedArgument: "undefined")
              }
              unknownField5
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Undefined argument < undefinedArgument > on field < doesKnowCommand > of type < Dog >.",
                        "path": None,
                        "locations": [{"line": 27, "column": 67}],
                    },
                    {
                        "message": "field `Dog.unknownField4` was not found in GraphQL schema.",
                        "path": ["dog", "unknownField4"],
                        "locations": [{"line": 29, "column": 17}],
                    },
                    {
                        "message": "Undefined argument < undefinedArgument > on directive < @deprecated >.",
                        "path": None,
                        "locations": [{"line": 30, "column": 84}],
                    },
                    {
                        "message": "field `Query.unknownField5` was not found in GraphQL schema.",
                        "path": ["unknownField5"],
                        "locations": [{"line": 32, "column": 15}],
                    },
                    {
                        "message": "field `Query.unknownField1` was not found in GraphQL schema.",
                        "path": ["unknownField1"],
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "field `Dog.unknownField3` was not found in GraphQL schema.",
                        "path": ["dog", "unknownField3"],
                        "locations": [{"line": 20, "column": 15}],
                    },
                    {
                        "message": "field < doesKnowCommand > is a leaf and thus can't have a selection set",
                        "path": ["dog", "doesKnowCommand"],
                        "locations": [{"line": 9, "column": 17}],
                    },
                    {
                        "message": "Undefined argument < undefinedArgument > on directive < @deprecated >.",
                        "path": None,
                        "locations": [{"line": 14, "column": 84}],
                    },
                ],
            },
        ),
    ],
)
async def test_issue105(engine, query, expected):
    assert await engine.execute(query) == expected
