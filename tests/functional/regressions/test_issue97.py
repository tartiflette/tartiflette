import pytest


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="animals")
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
                    "message": "Unknown argument < notId > on field < Query.dog >.",
                    "path": None,
                    "locations": [{"line": 3, "column": 19}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
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
                    "message": "Unknown argument < notId > on field < Query.dog >.",
                    "path": None,
                    "locations": [{"line": 4, "column": 21}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
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
                    "message": "Unknown argument < notId > on field < Query.dog >.",
                    "path": None,
                    "locations": [{"line": 3, "column": 19}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
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
                    "message": "Unknown argument < notId > on field < Query.dog >.",
                    "path": None,
                    "locations": [{"line": 4, "column": 21}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
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
                    "message": "Unknown argument < command > on field < Dog.doesKnowCommand >. Did you mean dogCommand?",
                    "path": None,
                    "locations": [{"line": 4, "column": 33}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
                    },
                },
                {
                    "message": "Field < doesKnowCommand > argument < dogCommand > of type < DogCommand! > is required, but it was not provided.",
                    "path": None,
                    "locations": [{"line": 4, "column": 17}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.2.1",
                        "tag": "required-arguments",
                        "details": "https://spec.graphql.org/June2018/#sec-Required-Arguments",
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
                    "message": "Unknown argument < command > on field < Dog.doesKnowCommand >. Did you mean dogCommand?",
                    "path": None,
                    "locations": [{"line": 5, "column": 35}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
                    },
                },
                {
                    "message": "Field < doesKnowCommand > argument < dogCommand > of type < DogCommand! > is required, but it was not provided.",
                    "path": None,
                    "locations": [{"line": 5, "column": 19}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.2.1",
                        "tag": "required-arguments",
                        "details": "https://spec.graphql.org/June2018/#sec-Required-Arguments",
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
                    "message": "Unknown argument < command > on field < Dog.doesKnowCommand >. Did you mean dogCommand?",
                    "path": None,
                    "locations": [{"line": 4, "column": 33}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
                    },
                },
                {
                    "message": "Field < doesKnowCommand > argument < dogCommand > of type < DogCommand! > is required, but it was not provided.",
                    "path": None,
                    "locations": [{"line": 4, "column": 17}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.2.1",
                        "tag": "required-arguments",
                        "details": "https://spec.graphql.org/June2018/#sec-Required-Arguments",
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
                    "message": "Unknown argument < command > on field < Dog.doesKnowCommand >. Did you mean dogCommand?",
                    "path": None,
                    "locations": [{"line": 5, "column": 35}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
                    },
                },
                {
                    "message": "Field < doesKnowCommand > argument < dogCommand > of type < DogCommand! > is required, but it was not provided.",
                    "path": None,
                    "locations": [{"line": 5, "column": 19}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.2.1",
                        "tag": "required-arguments",
                        "details": "https://spec.graphql.org/June2018/#sec-Required-Arguments",
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
                    "message": "Unknown argument < command > on field < Dog.doesKnowCommand >. Did you mean dogCommand?",
                    "path": None,
                    "locations": [{"line": 4, "column": 33}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
                    },
                },
                {
                    "message": "Field < doesKnowCommand > argument < dogCommand > of type < DogCommand! > is required, but it was not provided.",
                    "path": None,
                    "locations": [{"line": 4, "column": 17}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.2.1",
                        "tag": "required-arguments",
                        "details": "https://spec.graphql.org/June2018/#sec-Required-Arguments",
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
                    "message": "Directive < @deprecated > may not be used on FIELD.",
                    "path": None,
                    "locations": [{"line": 3, "column": 19}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                },
                {
                    "message": "Unknown argument < unless > on directive < @deprecated >.",
                    "path": None,
                    "locations": [{"line": 3, "column": 31}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
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
                    "message": "Directive < @deprecated > may not be used on FIELD.",
                    "path": None,
                    "locations": [{"line": 4, "column": 21}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                },
                {
                    "message": "Unknown argument < unless > on directive < @deprecated >.",
                    "path": None,
                    "locations": [{"line": 4, "column": 33}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
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
                    "message": "Directive < @deprecated > may not be used on FIELD.",
                    "path": None,
                    "locations": [{"line": 3, "column": 19}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                },
                {
                    "message": "Unknown argument < unless > on directive < @deprecated >.",
                    "path": None,
                    "locations": [{"line": 3, "column": 31}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
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
                    "message": "Directive < @deprecated > may not be used on FIELD.",
                    "path": None,
                    "locations": [{"line": 4, "column": 21}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                },
                {
                    "message": "Unknown argument < unless > on directive < @deprecated >.",
                    "path": None,
                    "locations": [{"line": 4, "column": 33}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
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
                    "message": "Directive < @deprecated > may not be used on FIELD.",
                    "path": None,
                    "locations": [{"line": 4, "column": 52}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                },
                {
                    "message": "Unknown argument < unless > on directive < @deprecated >.",
                    "path": None,
                    "locations": [{"line": 4, "column": 64}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
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
                    "message": "Directive < @deprecated > may not be used on FIELD.",
                    "path": None,
                    "locations": [{"line": 5, "column": 54}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                },
                {
                    "message": "Unknown argument < unless > on directive < @deprecated >.",
                    "path": None,
                    "locations": [{"line": 5, "column": 66}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
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
                    "message": "Directive < @deprecated > may not be used on FIELD.",
                    "path": None,
                    "locations": [{"line": 4, "column": 52}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                },
                {
                    "message": "Unknown argument < unless > on directive < @deprecated >.",
                    "path": None,
                    "locations": [{"line": 4, "column": 64}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
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
                    "message": "Directive < @deprecated > may not be used on FIELD.",
                    "path": None,
                    "locations": [{"line": 5, "column": 54}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                },
                {
                    "message": "Unknown argument < unless > on directive < @deprecated >.",
                    "path": None,
                    "locations": [{"line": 5, "column": 66}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
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
                    "message": "Unknown argument < firstUndefinedArg > on field < Query.dog >.",
                    "path": None,
                    "locations": [{"line": 3, "column": 19}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
                    },
                },
                {
                    "message": "Unknown argument < secondUndefinedArg > on field < Query.dog >.",
                    "path": None,
                    "locations": [{"line": 3, "column": 41}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
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
                    "message": "Directive < @deprecated > may not be used on FIELD.",
                    "path": None,
                    "locations": [{"line": 4, "column": 52}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                },
                {
                    "message": "Unknown argument < firstUndefinedArg > on directive < @deprecated >.",
                    "path": None,
                    "locations": [{"line": 4, "column": 64}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
                    },
                },
                {
                    "message": "Unknown argument < secondUndefinedArg > on directive < @deprecated >.",
                    "path": None,
                    "locations": [{"line": 4, "column": 86}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
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
                    "message": "Cannot query field < undefinedField > on type < Query >.",
                    "path": None,
                    "locations": [{"line": 3, "column": 15}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
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
                    "message": "Cannot query field < undefinedField > on type < Query >.",
                    "path": None,
                    "locations": [{"line": 3, "column": 15}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    },
                },
                {
                    "message": "Directive < @deprecated > may not be used on FIELD.",
                    "path": None,
                    "locations": [{"line": 3, "column": 30}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                },
                {
                    "message": "Unknown argument < undefinedArg > on directive < @deprecated >.",
                    "path": None,
                    "locations": [{"line": 3, "column": 42}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.4.1",
                        "tag": "argument-names",
                        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
                    },
                },
            ],
        ),
    ],
)
async def test_issue97(schema_stack, query, errors):
    assert await schema_stack.execute(query) == {
        "data": None,
        "errors": errors,
    }
