import pytest


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
                    "message": "Provided Argument < notId > doesn't exists on field < Query.dog >.",
                    "path": ["dog"],
                    "locations": [{"line": 3, "column": 19}],
                    "extensions": {
                        "rule": "5.4.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                        "tag": "argument-names",
                    },
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
                    "message": "Provided Argument < notId > doesn't exists on field < Query.dog >.",
                    "path": ["dog"],
                    "locations": [{"line": 4, "column": 21}],
                    "extensions": {
                        "rule": "5.4.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                        "tag": "argument-names",
                    },
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
                    "message": "Provided Argument < notId > doesn't exists on field < Query.dog >.",
                    "path": ["dog"],
                    "locations": [{"line": 3, "column": 19}],
                    "extensions": {
                        "rule": "5.4.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                        "tag": "argument-names",
                    },
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
                    "message": "Provided Argument < notId > doesn't exists on field < Query.dog >.",
                    "path": ["dog"],
                    "locations": [{"line": 4, "column": 21}],
                    "extensions": {
                        "rule": "5.4.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                        "tag": "argument-names",
                    },
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
                    "message": "Provided Argument < command > doesn't exists on field < Dog.doesKnowCommand >.",
                    "path": ["dog", "doesKnowCommand"],
                    "locations": [{"line": 4, "column": 33}],
                    "extensions": {
                        "rule": "5.4.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                        "tag": "argument-names",
                    },
                },
                {
                    "message": "Missing mandatory argument < dogCommand > in field < Dog.doesKnowCommand >.",
                    "path": ["dog", "doesKnowCommand"],
                    "locations": [{"line": 4, "column": 17}],
                    "extensions": {
                        "rule": "5.4.2.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Required-Arguments",
                        "tag": "required-arguments",
                    },
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
                    "message": "Provided Argument < command > doesn't exists on field < Dog.doesKnowCommand >.",
                    "path": ["dog", "doesKnowCommand"],
                    "locations": [{"line": 5, "column": 35}],
                    "extensions": {
                        "rule": "5.4.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                        "tag": "argument-names",
                    },
                },
                {
                    "message": "Missing mandatory argument < dogCommand > in field < Dog.doesKnowCommand >.",
                    "path": ["dog", "doesKnowCommand"],
                    "locations": [{"line": 5, "column": 19}],
                    "extensions": {
                        "rule": "5.4.2.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Required-Arguments",
                        "tag": "required-arguments",
                    },
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
                    "message": "Provided Argument < command > doesn't exists on field < Dog.doesKnowCommand >.",
                    "path": ["dog", "doesKnowCommand"],
                    "locations": [{"line": 4, "column": 33}],
                    "extensions": {
                        "rule": "5.4.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                        "tag": "argument-names",
                    },
                },
                {
                    "message": "Missing mandatory argument < dogCommand > in field < Dog.doesKnowCommand >.",
                    "path": ["dog", "doesKnowCommand"],
                    "locations": [{"line": 4, "column": 17}],
                    "extensions": {
                        "rule": "5.4.2.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Required-Arguments",
                        "tag": "required-arguments",
                    },
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
                    "message": "Provided Argument < command > doesn't exists on field < Dog.doesKnowCommand >.",
                    "path": ["dog", "doesKnowCommand"],
                    "locations": [{"line": 5, "column": 35}],
                    "extensions": {
                        "rule": "5.4.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                        "tag": "argument-names",
                    },
                },
                {
                    "message": "Missing mandatory argument < dogCommand > in field < Dog.doesKnowCommand >.",
                    "path": ["dog", "doesKnowCommand"],
                    "locations": [{"line": 5, "column": 19}],
                    "extensions": {
                        "rule": "5.4.2.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Required-Arguments",
                        "tag": "required-arguments",
                    },
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
                    "message": "Provided Argument < command > doesn't exists on field < Dog.doesKnowCommand >.",
                    "path": ["doesKnowCommand"],
                    "locations": [{"line": 4, "column": 33}],
                    "extensions": {
                        "rule": "5.4.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                        "tag": "argument-names",
                    },
                },
                {
                    "message": "Missing mandatory argument < dogCommand > in field < Dog.doesKnowCommand >.",
                    "path": ["doesKnowCommand"],
                    "locations": [{"line": 4, "column": 17}],
                    "extensions": {
                        "rule": "5.4.2.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Required-Arguments",
                        "tag": "required-arguments",
                    },
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
                    "message": "Provided Argument < unless > doesn't exists on directive < @deprecated >.",
                    "path": ["dog"],
                    "locations": [{"line": 3, "column": 31}],
                    "extensions": {
                        "rule": "5.4.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                        "tag": "argument-names",
                    },
                },
                {
                    "message": "Directive < @deprecated > is not used in a valid location.",
                    "path": ["dog"],
                    "locations": [
                        {"line": 3, "column": 15},
                        {"line": 3, "column": 19},
                    ],
                    "extensions": {
                        "rule": "5.7.2",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                        "tag": "directives-are-in-valid-locations",
                    },
                },
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
                    "message": "Provided Argument < unless > doesn't exists on directive < @deprecated >.",
                    "path": ["dog"],
                    "locations": [{"line": 4, "column": 33}],
                    "extensions": {
                        "rule": "5.4.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                        "tag": "argument-names",
                    },
                },
                {
                    "message": "Directive < @deprecated > is not used in a valid location.",
                    "path": ["dog"],
                    "locations": [
                        {"line": 4, "column": 17},
                        {"line": 4, "column": 21},
                    ],
                    "extensions": {
                        "rule": "5.7.2",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                        "tag": "directives-are-in-valid-locations",
                    },
                },
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
                    "message": "Provided Argument < unless > doesn't exists on directive < @deprecated >.",
                    "path": ["dog"],
                    "locations": [{"line": 3, "column": 31}],
                    "extensions": {
                        "rule": "5.4.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                        "tag": "argument-names",
                    },
                },
                {
                    "message": "Directive < @deprecated > is not used in a valid location.",
                    "path": ["dog"],
                    "locations": [
                        {"line": 3, "column": 15},
                        {"line": 3, "column": 19},
                    ],
                    "extensions": {
                        "rule": "5.7.2",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                        "tag": "directives-are-in-valid-locations",
                    },
                },
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
                    "message": "Provided Argument < unless > doesn't exists on directive < @deprecated >.",
                    "path": ["dog"],
                    "locations": [{"line": 4, "column": 33}],
                    "extensions": {
                        "rule": "5.4.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                        "tag": "argument-names",
                    },
                },
                {
                    "message": "Directive < @deprecated > is not used in a valid location.",
                    "path": ["dog"],
                    "locations": [
                        {"line": 4, "column": 17},
                        {"line": 4, "column": 21},
                    ],
                    "extensions": {
                        "rule": "5.7.2",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                        "tag": "directives-are-in-valid-locations",
                    },
                },
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
                    "message": "Provided Argument < unless > doesn't exists on directive < @deprecated >.",
                    "path": ["dog", "isHousetrained"],
                    "locations": [{"line": 4, "column": 64}],
                    "extensions": {
                        "rule": "5.4.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                        "tag": "argument-names",
                    },
                },
                {
                    "message": "Directive < @deprecated > is not used in a valid location.",
                    "path": ["dog", "isHousetrained"],
                    "locations": [
                        {"line": 4, "column": 17},
                        {"line": 4, "column": 52},
                    ],
                    "extensions": {
                        "rule": "5.7.2",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                        "tag": "directives-are-in-valid-locations",
                    },
                },
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
                    "message": "Provided Argument < unless > doesn't exists on directive < @deprecated >.",
                    "path": ["dog", "isHousetrained"],
                    "locations": [{"line": 5, "column": 66}],
                    "extensions": {
                        "rule": "5.4.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                        "tag": "argument-names",
                    },
                },
                {
                    "message": "Directive < @deprecated > is not used in a valid location.",
                    "path": ["dog", "isHousetrained"],
                    "locations": [
                        {"line": 5, "column": 19},
                        {"line": 5, "column": 54},
                    ],
                    "extensions": {
                        "rule": "5.7.2",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                        "tag": "directives-are-in-valid-locations",
                    },
                },
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
                    "message": "Provided Argument < unless > doesn't exists on directive < @deprecated >.",
                    "path": ["dog", "isHousetrained"],
                    "locations": [{"line": 4, "column": 64}],
                    "extensions": {
                        "rule": "5.4.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                        "tag": "argument-names",
                    },
                },
                {
                    "message": "Directive < @deprecated > is not used in a valid location.",
                    "path": ["dog", "isHousetrained"],
                    "locations": [
                        {"line": 4, "column": 17},
                        {"line": 4, "column": 52},
                    ],
                    "extensions": {
                        "rule": "5.7.2",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                        "tag": "directives-are-in-valid-locations",
                    },
                },
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
                    "message": "Provided Argument < unless > doesn't exists on directive < @deprecated >.",
                    "path": ["dog", "isHousetrained"],
                    "locations": [{"line": 5, "column": 66}],
                    "extensions": {
                        "rule": "5.4.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                        "tag": "argument-names",
                    },
                },
                {
                    "message": "Directive < @deprecated > is not used in a valid location.",
                    "path": ["dog", "isHousetrained"],
                    "locations": [
                        {"line": 5, "column": 19},
                        {"line": 5, "column": 54},
                    ],
                    "extensions": {
                        "rule": "5.7.2",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                        "tag": "directives-are-in-valid-locations",
                    },
                },
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
                    "message": "Provided Argument < firstUndefinedArg > doesn't exists on field < Query.dog >.",
                    "path": ["dog"],
                    "locations": [{"line": 3, "column": 19}],
                    "extensions": {
                        "rule": "5.4.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                        "tag": "argument-names",
                    },
                },
                {
                    "message": "Provided Argument < secondUndefinedArg > doesn't exists on field < Query.dog >.",
                    "path": ["dog"],
                    "locations": [{"line": 3, "column": 41}],
                    "extensions": {
                        "rule": "5.4.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                        "tag": "argument-names",
                    },
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
                    "message": "Provided Argument < firstUndefinedArg > doesn't exists on directive < @deprecated >.",
                    "path": ["dog", "isHousetrained"],
                    "locations": [{"line": 4, "column": 64}],
                    "extensions": {
                        "rule": "5.4.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                        "tag": "argument-names",
                    },
                },
                {
                    "message": "Provided Argument < secondUndefinedArg > doesn't exists on directive < @deprecated >.",
                    "path": ["dog", "isHousetrained"],
                    "locations": [{"line": 4, "column": 86}],
                    "extensions": {
                        "rule": "5.4.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                        "tag": "argument-names",
                    },
                },
                {
                    "message": "Directive < @deprecated > is not used in a valid location.",
                    "path": ["dog", "isHousetrained"],
                    "locations": [
                        {"line": 4, "column": 17},
                        {"line": 4, "column": 52},
                    ],
                    "extensions": {
                        "rule": "5.7.2",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                        "tag": "directives-are-in-valid-locations",
                    },
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
                    "message": "Field undefinedField doesn't exist on Query",
                    "path": ["undefinedField"],
                    "locations": [{"line": 3, "column": 15}],
                    "extensions": {
                        "rule": "5.3.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                    },
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
                    "message": "Provided Argument < undefinedArg > doesn't exists on directive < @deprecated >.",
                    "path": ["undefinedField"],
                    "locations": [{"line": 3, "column": 42}],
                    "extensions": {
                        "rule": "5.4.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                        "tag": "argument-names",
                    },
                },
                {
                    "message": "Directive < @deprecated > is not used in a valid location.",
                    "path": ["undefinedField"],
                    "locations": [
                        {"line": 3, "column": 15},
                        {"line": 3, "column": 30},
                    ],
                    "extensions": {
                        "rule": "5.7.2",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                        "tag": "directives-are-in-valid-locations",
                    },
                },
                {
                    "message": "Field undefinedField doesn't exist on Query",
                    "path": ["undefinedField"],
                    "locations": [{"line": 3, "column": 15}],
                    "extensions": {
                        "rule": "5.3.1",
                        "spec": "June 2018",
                        "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                    },
                },
            ],
        ),
    ],
)
async def test_issue97(engine, query, errors):
    assert await engine.execute(query) == {"data": None, "errors": errors}
