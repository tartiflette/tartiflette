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
                        "message": "Field unknownField doesn't exist on Human",
                        "path": ["human", "unknownField"],
                        "locations": [{"line": 5, "column": 17}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
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
                        "message": "Field unknownField doesn't exist on Human",
                        "path": ["human", "unknownField"],
                        "locations": [{"line": 4, "column": 17}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Provided Argument < undefinedArgument > doesn't exist on field < Query.human >.",
                        "path": ["human"],
                        "locations": [{"line": 3, "column": 21}],
                        "extensions": {
                            "rule": "5.4.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                            "tag": "argument-names",
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
                        "message": "Field unknownField doesn't exist on Human",
                        "path": ["human", "unknownField"],
                        "locations": [{"line": 4, "column": 17}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Provided Argument < undefinedArgument > doesn't exist on field < Query.human >.",
                        "path": ["human"],
                        "locations": [{"line": 3, "column": 21}],
                        "extensions": {
                            "rule": "5.4.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                            "tag": "argument-names",
                        },
                    },
                    {
                        "message": "Field name doesn't exist on Root",
                        "path": ["unknownField", "name"],
                        "locations": [{"line": 8, "column": 17}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field unknownField doesn't exist on Query",
                        "path": ["unknownField"],
                        "locations": [{"line": 7, "column": 15}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
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
                        "message": "Provided Argument < command > doesn't exist on field < Dog.doesKnowCommand >.",
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
                        "message": "Provided Argument < command > doesn't exist on field < Dog.doesKnowCommand >.",
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
                        "message": "Field unknownField1 doesn't exist on Query",
                        "path": ["unknownField1"],
                        "locations": [{"line": 3, "column": 15}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field unknownField2 doesn't exist on Boolean",
                        "path": ["dog", "doesKnowCommand", "unknownField2"],
                        "locations": [{"line": 6, "column": 19}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field doesKnowCommand must not have a selection since type Boolean has no subfields.",
                        "path": ["dog", "doesKnowCommand"],
                        "locations": [{"line": 5, "column": 17}],
                        "extensions": {
                            "rule": "5.3.3",
                            "tag": "leaf-field-selections",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Leaf-Field-Selections",
                            "spec": "June 2018",
                        },
                    },
                    {
                        "message": "Provided Argument < command > doesn't exist on field < Dog.doesKnowCommand >.",
                        "path": ["dog", "doesKnowCommand"],
                        "locations": [{"line": 5, "column": 33}],
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
                        "locations": [{"line": 5, "column": 17}],
                        "extensions": {
                            "rule": "5.4.2.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Required-Arguments",
                            "tag": "required-arguments",
                        },
                    },
                    {
                        "message": "Field unknownField3 doesn't exist on Dog",
                        "path": ["dog", "unknownField3"],
                        "locations": [{"line": 8, "column": 17}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field unknownField4 doesn't exist on Query",
                        "path": ["unknownField4"],
                        "locations": [{"line": 10, "column": 15}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
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
                        "message": "Field unknownField1 doesn't exist on Query",
                        "path": ["unknownField1"],
                        "locations": [{"line": 3, "column": 15}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field unknownField2 doesn't exist on Boolean",
                        "path": ["doesKnowCommand", "unknownField2"],
                        "locations": [{"line": 9, "column": 19}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field doesKnowCommand must not have a selection since type Boolean has no subfields.",
                        "path": ["doesKnowCommand"],
                        "locations": [{"line": 8, "column": 17}],
                        "extensions": {
                            "rule": "5.3.3",
                            "tag": "leaf-field-selections",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Leaf-Field-Selections",
                            "spec": "June 2018",
                        },
                    },
                    {
                        "message": "Provided Argument < command > doesn't exist on field < Dog.doesKnowCommand >.",
                        "path": ["doesKnowCommand"],
                        "locations": [{"line": 8, "column": 33}],
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
                        "locations": [{"line": 8, "column": 17}],
                        "extensions": {
                            "rule": "5.4.2.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Required-Arguments",
                            "tag": "required-arguments",
                        },
                    },
                    {
                        "message": "Field unknownField3 doesn't exist on Dog",
                        "path": ["unknownField3"],
                        "locations": [{"line": 16, "column": 15}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field unknownField4 doesn't exist on Dog",
                        "path": ["dog", "unknownField4"],
                        "locations": [{"line": 23, "column": 17}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field unknownField5 doesn't exist on Query",
                        "path": ["unknownField5"],
                        "locations": [{"line": 25, "column": 15}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
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
                        "message": "Field unknownField1 doesn't exist on Query",
                        "path": ["unknownField1"],
                        "locations": [{"line": 3, "column": 15}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field unknownField21 doesn't exist on Root",
                        "path": [
                            "doesKnowCommand",
                            "unknownField2",
                            "unknownField21",
                        ],
                        "locations": [{"line": 10, "column": 21}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field unknownField2 doesn't exist on Boolean",
                        "path": ["doesKnowCommand", "unknownField2"],
                        "locations": [{"line": 9, "column": 19}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field doesKnowCommand must not have a selection since type Boolean has no subfields.",
                        "path": ["doesKnowCommand"],
                        "locations": [{"line": 8, "column": 17}],
                        "extensions": {
                            "rule": "5.3.3",
                            "tag": "leaf-field-selections",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Leaf-Field-Selections",
                            "spec": "June 2018",
                        },
                    },
                    {
                        "message": "Provided Argument < command > doesn't exist on field < Dog.doesKnowCommand >.",
                        "path": ["doesKnowCommand"],
                        "locations": [{"line": 8, "column": 33}],
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
                        "locations": [{"line": 8, "column": 17}],
                        "extensions": {
                            "rule": "5.4.2.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Required-Arguments",
                            "tag": "required-arguments",
                        },
                    },
                    {
                        "message": "Field unknownField3 doesn't exist on Dog",
                        "path": ["unknownField3"],
                        "locations": [{"line": 17, "column": 15}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field unknownField4 doesn't exist on Dog",
                        "path": ["dog", "unknownField4"],
                        "locations": [{"line": 25, "column": 17}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field unknownField5 doesn't exist on Query",
                        "path": ["unknownField5"],
                        "locations": [{"line": 27, "column": 15}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
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
                        "message": "Field unknownField1 doesn't exist on Query",
                        "path": ["unknownField1"],
                        "locations": [{"line": 3, "column": 15}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Provided Argument < undefinedArgument > doesn't exist on directive < @deprecated >.",
                        "path": ["doesKnowCommand", "unknownField2"],
                        "locations": [{"line": 10, "column": 45}],
                        "extensions": {
                            "rule": "5.4.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                            "tag": "argument-names",
                        },
                    },
                    {
                        "message": "Field unknownField21 doesn't exist on Root",
                        "path": [
                            "doesKnowCommand",
                            "unknownField2",
                            "unknownField21",
                        ],
                        "locations": [{"line": 11, "column": 21}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Directive < @deprecated > is not used in a valid location.",
                        "path": ["doesKnowCommand", "unknownField2"],
                        "locations": [
                            {"line": 10, "column": 19},
                            {"line": 10, "column": 33},
                        ],
                        "extensions": {
                            "rule": "5.7.2",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                            "tag": "directives-are-in-valid-locations",
                        },
                    },
                    {
                        "message": "Field unknownField2 doesn't exist on Boolean",
                        "path": ["doesKnowCommand", "unknownField2"],
                        "locations": [{"line": 10, "column": 19}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field doesKnowCommand must not have a selection since type Boolean has no subfields.",
                        "path": ["doesKnowCommand"],
                        "locations": [{"line": 9, "column": 17}],
                        "extensions": {
                            "rule": "5.3.3",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Leaf-Field-Selections",
                            "tag": "leaf-field-selections",
                        },
                    },
                    {
                        "message": "Provided Argument < command > doesn't exist on field < Dog.doesKnowCommand >.",
                        "path": ["doesKnowCommand"],
                        "locations": [{"line": 9, "column": 58}],
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
                        "locations": [{"line": 9, "column": 17}],
                        "extensions": {
                            "rule": "5.4.2.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Required-Arguments",
                            "tag": "required-arguments",
                        },
                    },
                    {
                        "message": "Provided Argument < undefinedArgument > doesn't exist on directive < @deprecated >.",
                        "path": ["doesKnowCommand"],
                        "locations": [{"line": 14, "column": 84}],
                        "extensions": {
                            "rule": "5.4.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                            "tag": "argument-names",
                        },
                    },
                    {
                        "message": "Directive < @deprecated > is not used in a valid location.",
                        "path": ["doesKnowCommand"],
                        "locations": [
                            {"line": 14, "column": 17},
                            {"line": 14, "column": 72},
                        ],
                        "extensions": {
                            "rule": "5.7.2",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                            "tag": "directives-are-in-valid-locations",
                        },
                    },
                    {
                        "message": "Field unknownField3 doesn't exist on Dog",
                        "path": ["unknownField3"],
                        "locations": [{"line": 20, "column": 15}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Provided Argument < undefinedArgument > doesn't exist on field < Dog.doesKnowCommand >.",
                        "path": ["dog", "doesKnowCommand"],
                        "locations": [{"line": 27, "column": 67}],
                        "extensions": {
                            "rule": "5.4.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                            "tag": "argument-names",
                        },
                    },
                    {
                        "message": "Field unknownField4 doesn't exist on Dog",
                        "path": ["dog", "unknownField4"],
                        "locations": [{"line": 29, "column": 17}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Provided Argument < undefinedArgument > doesn't exist on directive < @deprecated >.",
                        "path": ["dog", "doesKnowCommand"],
                        "locations": [{"line": 30, "column": 84}],
                        "extensions": {
                            "rule": "5.4.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names",
                            "tag": "argument-names",
                        },
                    },
                    {
                        "message": "Directive < @deprecated > is not used in a valid location.",
                        "path": ["dog", "doesKnowCommand"],
                        "locations": [
                            {"line": 30, "column": 17},
                            {"line": 30, "column": 72},
                        ],
                        "extensions": {
                            "rule": "5.7.2",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                            "tag": "directives-are-in-valid-locations",
                        },
                    },
                    {
                        "message": "Field unknownField5 doesn't exist on Query",
                        "path": ["unknownField5"],
                        "locations": [{"line": 32, "column": 15}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                ],
            },
        ),
    ],
)
async def test_issue105(engine, query, expected):
    assert await engine.execute(query) == expected
