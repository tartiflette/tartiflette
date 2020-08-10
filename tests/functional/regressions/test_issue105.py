import pytest


async def _query_human_resolver(*_args, **__kwargs):
    return {"name": "Hooman"}


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
                        "message": "Cannot query field < unknownField > on type < Human >.",
                        "path": None,
                        "locations": [{"line": 5, "column": 17}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
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
                        "message": "Unknown argument < undefinedArgument > on field < Query.human >.",
                        "path": None,
                        "locations": [{"line": 3, "column": 21}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.4.1",
                            "tag": "argument-names",
                            "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
                        },
                    },
                    {
                        "message": "Cannot query field < unknownField > on type < Human >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 17}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
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
                        "message": "Unknown argument < undefinedArgument > on field < Query.human >.",
                        "path": None,
                        "locations": [{"line": 3, "column": 21}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.4.1",
                            "tag": "argument-names",
                            "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
                        },
                    },
                    {
                        "message": "Cannot query field < unknownField > on type < Human >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 17}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
                    },
                    {
                        "message": "Cannot query field < unknownField > on type < Query >.",
                        "path": None,
                        "locations": [{"line": 7, "column": 15}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
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
                        "message": "Cannot query field < unknownField1 > on type < Query >.",
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
                        "message": "Field < doesKnowCommand > must not have a selection since type < Boolean! > has no subfields.",
                        "path": None,
                        "locations": [{"line": 5, "column": 47}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.3",
                            "tag": "leaf-field-selections",
                            "details": "https://spec.graphql.org/June2018/#sec-Leaf-Field-Selections",
                        },
                    },
                    {
                        "message": "Unknown argument < command > on field < Dog.doesKnowCommand >. Did you mean dogCommand?",
                        "path": None,
                        "locations": [{"line": 5, "column": 33}],
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
                        "locations": [{"line": 5, "column": 17}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.4.2.1",
                            "tag": "required-arguments",
                            "details": "https://spec.graphql.org/June2018/#sec-Required-Arguments",
                        },
                    },
                    {
                        "message": "Cannot query field < unknownField3 > on type < Dog >.",
                        "path": None,
                        "locations": [{"line": 8, "column": 17}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
                    },
                    {
                        "message": "Cannot query field < unknownField4 > on type < Query >.",
                        "path": None,
                        "locations": [{"line": 10, "column": 15}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
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
                        "message": "Cannot query field < unknownField1 > on type < Query >.",
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
                        "message": "Field < doesKnowCommand > must not have a selection since type < Boolean! > has no subfields.",
                        "path": None,
                        "locations": [{"line": 8, "column": 47}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.3",
                            "tag": "leaf-field-selections",
                            "details": "https://spec.graphql.org/June2018/#sec-Leaf-Field-Selections",
                        },
                    },
                    {
                        "message": "Unknown argument < command > on field < Dog.doesKnowCommand >. Did you mean dogCommand?",
                        "path": None,
                        "locations": [{"line": 8, "column": 33}],
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
                        "locations": [{"line": 8, "column": 17}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.4.2.1",
                            "tag": "required-arguments",
                            "details": "https://spec.graphql.org/June2018/#sec-Required-Arguments",
                        },
                    },
                    {
                        "message": "Cannot query field < unknownField3 > on type < Dog >.",
                        "path": None,
                        "locations": [{"line": 16, "column": 15}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
                    },
                    {
                        "message": "Cannot query field < unknownField4 > on type < Dog >.",
                        "path": None,
                        "locations": [{"line": 23, "column": 17}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
                    },
                    {
                        "message": "Cannot query field < unknownField5 > on type < Query >.",
                        "path": None,
                        "locations": [{"line": 25, "column": 15}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
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
                        "message": "Cannot query field < unknownField1 > on type < Query >.",
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
                        "message": "Field < doesKnowCommand > must not have a selection since type < Boolean! > has no subfields.",
                        "path": None,
                        "locations": [{"line": 8, "column": 47}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.3",
                            "tag": "leaf-field-selections",
                            "details": "https://spec.graphql.org/June2018/#sec-Leaf-Field-Selections",
                        },
                    },
                    {
                        "message": "Unknown argument < command > on field < Dog.doesKnowCommand >. Did you mean dogCommand?",
                        "path": None,
                        "locations": [{"line": 8, "column": 33}],
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
                        "locations": [{"line": 8, "column": 17}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.4.2.1",
                            "tag": "required-arguments",
                            "details": "https://spec.graphql.org/June2018/#sec-Required-Arguments",
                        },
                    },
                    {
                        "message": "Cannot query field < unknownField3 > on type < Dog >.",
                        "path": None,
                        "locations": [{"line": 17, "column": 15}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
                    },
                    {
                        "message": "Cannot query field < unknownField4 > on type < Dog >.",
                        "path": None,
                        "locations": [{"line": 25, "column": 17}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
                    },
                    {
                        "message": "Cannot query field < unknownField5 > on type < Query >.",
                        "path": None,
                        "locations": [{"line": 27, "column": 15}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
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
                        "message": "Cannot query field < unknownField1 > on type < Query >.",
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
                        "message": "Field < doesKnowCommand > must not have a selection since type < Boolean! > has no subfields.",
                        "path": None,
                        "locations": [{"line": 9, "column": 72}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.3",
                            "tag": "leaf-field-selections",
                            "details": "https://spec.graphql.org/June2018/#sec-Leaf-Field-Selections",
                        },
                    },
                    {
                        "message": "Unknown argument < command > on field < Dog.doesKnowCommand >. Did you mean dogCommand?",
                        "path": None,
                        "locations": [{"line": 9, "column": 58}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.4.1",
                            "tag": "argument-names",
                            "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
                        },
                    },
                    {
                        "message": "Directive < @deprecated > may not be used on FIELD.",
                        "path": None,
                        "locations": [{"line": 10, "column": 33}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.7.2",
                            "tag": "directives-are-in-valid-locations",
                            "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                        },
                    },
                    {
                        "message": "Unknown argument < undefinedArgument > on directive < @deprecated >.",
                        "path": None,
                        "locations": [{"line": 10, "column": 45}],
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
                        "locations": [{"line": 9, "column": 17}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.4.2.1",
                            "tag": "required-arguments",
                            "details": "https://spec.graphql.org/June2018/#sec-Required-Arguments",
                        },
                    },
                    {
                        "message": "Directive < @deprecated > may not be used on FIELD.",
                        "path": None,
                        "locations": [{"line": 14, "column": 72}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.7.2",
                            "tag": "directives-are-in-valid-locations",
                            "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                        },
                    },
                    {
                        "message": "Unknown argument < undefinedArgument > on directive < @deprecated >.",
                        "path": None,
                        "locations": [{"line": 14, "column": 84}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.4.1",
                            "tag": "argument-names",
                            "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
                        },
                    },
                    {
                        "message": "Cannot query field < unknownField3 > on type < Dog >.",
                        "path": None,
                        "locations": [{"line": 20, "column": 15}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
                    },
                    {
                        "message": "Unknown argument < undefinedArgument > on field < Dog.doesKnowCommand >.",
                        "path": None,
                        "locations": [{"line": 27, "column": 67}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.4.1",
                            "tag": "argument-names",
                            "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
                        },
                    },
                    {
                        "message": "Cannot query field < unknownField4 > on type < Dog >.",
                        "path": None,
                        "locations": [{"line": 29, "column": 17}],
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
                        "locations": [{"line": 30, "column": 72}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.7.2",
                            "tag": "directives-are-in-valid-locations",
                            "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                        },
                    },
                    {
                        "message": "Unknown argument < undefinedArgument > on directive < @deprecated >.",
                        "path": None,
                        "locations": [{"line": 30, "column": 84}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.4.1",
                            "tag": "argument-names",
                            "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
                        },
                    },
                    {
                        "message": "Cannot query field < unknownField5 > on type < Query >.",
                        "path": None,
                        "locations": [{"line": 32, "column": 15}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
                    },
                ],
            },
        ),
    ],
)
async def test_issue105(engine, query, expected):
    assert await engine.execute(query) == expected
