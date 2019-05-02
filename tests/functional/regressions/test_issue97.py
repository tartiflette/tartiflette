import pytest


@pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.ttftt_engine
@pytest.mark.parametrize(
    "query,errors",
    [
        # Undefined argument on root node
        (
            """
            query {
              dog(notId: 1) {
                name
              }
            }
            """,
            [
                {
                    "message": "Undefined argument < notId > on field < dog > of type < Query >.",
                    "path": None,
                    "locations": [{"line": 3, "column": 19}],
                }
            ],
        ),
        (
            """
            query {
              ... on Query {
                dog(notId: 1) {
                  name
                }
              }
            }
            """,
            [
                {
                    "message": "Undefined argument < notId > on field < dog > of type < Query >.",
                    "path": None,
                    "locations": [{"line": 4, "column": 21}],
                }
            ],
        ),
        (
            """
            fragment QueryFields on Query {
              dog(notId: 1) {
                name
              }
            }

            query {
              ...QueryFields
            }
            """,
            [
                {
                    "message": "Undefined argument < notId > on field < dog > of type < Query >.",
                    "path": None,
                    "locations": [{"line": 3, "column": 19}],
                }
            ],
        ),
        (
            """
            fragment QueryFields on Query {
              ... on Query {
                dog(notId: 1) {
                  name
                }
              }
            }

            query {
              ...QueryFields
            }
            """,
            [
                {
                    "message": "Undefined argument < notId > on field < dog > of type < Query >.",
                    "path": None,
                    "locations": [{"line": 4, "column": 21}],
                }
            ],
        ),
        # Undefined argument on nested node
        (
            """
            query {
              dog {
                doesKnowCommand(command: SIT)
              }
            }
            """,
            [
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
        ),
        (
            """
            query {
              ... on Query {
                dog {
                  doesKnowCommand(command: SIT)
                }
              }
            }
            """,
            [
                {
                    "message": "Undefined argument < command > on field < doesKnowCommand > of type < Dog >.",
                    "path": None,
                    "locations": [{"line": 5, "column": 35}],
                },
                {
                    "message": "Missing required < dogCommand > argument on < doesKnowCommand > field.",
                    "path": None,
                    "locations": [{"line": 5, "column": 19}],
                },
            ],
        ),
        (
            """
            fragment QueryFields on Query {
              dog {
                doesKnowCommand(command: SIT)
              }
            }

            query {
              ...QueryFields
            }
            """,
            [
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
        ),
        (
            """
            fragment QueryFields on Query {
              ... on Query {
                dog {
                  doesKnowCommand(command: SIT)
                }
              }
            }

            query {
              ...QueryFields
            }
            """,
            [
                {
                    "message": "Undefined argument < command > on field < doesKnowCommand > of type < Dog >.",
                    "path": None,
                    "locations": [{"line": 5, "column": 35}],
                },
                {
                    "message": "Missing required < dogCommand > argument on < doesKnowCommand > field.",
                    "path": None,
                    "locations": [{"line": 5, "column": 19}],
                },
            ],
        ),
        (
            """
            fragment DogFields on Dog {
              ... on Dog {
                doesKnowCommand(command: SIT)
              }
            }

            fragment QueryFields on Query {
              ... on Query {
                dog {
                  ...DogFields
                }
              }
            }

            query {
              ...QueryFields
            }
            """,
            [
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
        ),
        # Undefined argument on directive on root node
        (
            """
            query {
              dog @deprecated(unless: false) {
                name
              }
            }
            """,
            [
                {
                    "message": "Undefined argument < unless > on directive < @deprecated >.",
                    "path": None,
                    "locations": [{"line": 3, "column": 31}],
                }
            ],
        ),
        (
            """
            query {
              ... on Query {
                dog @deprecated(unless: false) {
                  name
                }
              }
            }
            """,
            [
                {
                    "message": "Undefined argument < unless > on directive < @deprecated >.",
                    "path": None,
                    "locations": [{"line": 4, "column": 33}],
                }
            ],
        ),
        (
            """
            fragment QueryFields on Query {
              dog @deprecated(unless: false) {
                name
              }
            }

            query {
              ...QueryFields
            }
            """,
            [
                {
                    "message": "Undefined argument < unless > on directive < @deprecated >.",
                    "path": None,
                    "locations": [{"line": 3, "column": 31}],
                }
            ],
        ),
        (
            """
            fragment QueryFields on Query {
              ... on Query {
                dog @deprecated(unless: false) {
                  name
                }
              }
            }

            query {
              ...QueryFields
            }
            """,
            [
                {
                    "message": "Undefined argument < unless > on directive < @deprecated >.",
                    "path": None,
                    "locations": [{"line": 4, "column": 33}],
                }
            ],
        ),
        # Undefined argument on directive on nested node
        (
            """
            query {
              dog {
                isHousetrained(atOtherHomes: true) @deprecated(unless: false)
              }
            }
            """,
            [
                {
                    "message": "Undefined argument < unless > on directive < @deprecated >.",
                    "path": None,
                    "locations": [{"line": 4, "column": 64}],
                }
            ],
        ),
        (
            """
            query {
              ... on Query {
                dog {
                  isHousetrained(atOtherHomes: true) @deprecated(unless: false)
                }
              }
            }
            """,
            [
                {
                    "message": "Undefined argument < unless > on directive < @deprecated >.",
                    "path": None,
                    "locations": [{"line": 5, "column": 66}],
                }
            ],
        ),
        (
            """
            fragment QueryFields on Query {
              dog {
                isHousetrained(atOtherHomes: true) @deprecated(unless: false)
              }
            }

            query {
              ...QueryFields
            }
            """,
            [
                {
                    "message": "Undefined argument < unless > on directive < @deprecated >.",
                    "path": None,
                    "locations": [{"line": 4, "column": 64}],
                }
            ],
        ),
        (
            """
            fragment QueryFields on Query {
              ... on Query {
                dog {
                  isHousetrained(atOtherHomes: true) @deprecated(unless: false)
                }
              }
            }

            query {
              ...QueryFields
            }
            """,
            [
                {
                    "message": "Undefined argument < unless > on directive < @deprecated >.",
                    "path": None,
                    "locations": [{"line": 5, "column": 66}],
                }
            ],
        ),
        # Multiple undefined arguments
        (
            """
            query {
              dog(firstUndefinedArg: 1, secondUndefinedArg: 2) {
                name
              }
            }
            """,
            [
                {
                    "message": "Undefined argument < firstUndefinedArg > on field < dog > of type < Query >.",
                    "path": None,
                    "locations": [{"line": 3, "column": 19}],
                },
                {
                    "message": "Undefined argument < secondUndefinedArg > on field < dog > of type < Query >.",
                    "path": None,
                    "locations": [{"line": 3, "column": 41}],
                },
            ],
        ),
        (
            """
            query {
              dog {
                isHousetrained(atOtherHomes: true) @deprecated(firstUndefinedArg: 1, secondUndefinedArg: 2)
              }
            }
            """,
            [
                {
                    "message": "Undefined argument < firstUndefinedArg > on directive < @deprecated >.",
                    "path": None,
                    "locations": [{"line": 4, "column": 64}],
                },
                {
                    "message": "Undefined argument < secondUndefinedArg > on directive < @deprecated >.",
                    "path": None,
                    "locations": [{"line": 4, "column": 86}],
                },
            ],
        ),
        # Undefined arguments on undefined node or directive
        (
            """
            query {
              undefinedField(undefinedArg: 1)
            }
            """,
            [
                {
                    "message": "field `Query.undefinedField` was not found in "
                    "GraphQL schema.",
                    "path": ["undefinedField"],
                    "locations": [{"line": 3, "column": 15}],
                }
            ],
        ),
        (
            """
            query {
              undefinedField @deprecated(undefinedArg: 1)
            }
            """,
            [
                {
                    "message": "field `Query.undefinedField` was not found in GraphQL schema.",
                    "path": ["undefinedField"],
                    "locations": [{"line": 3, "column": 15}],
                }
            ],
        ),
    ],
)
async def test_issue97(engine, query, errors):
    assert await engine.execute(query) == {"data": None, "errors": errors}
