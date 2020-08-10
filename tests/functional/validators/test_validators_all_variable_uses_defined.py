import pytest


@pytest.mark.asyncio
@pytest.mark.ttftt_engine
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query {
                catOrDog(id: $a) { name }
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot query field < name > on type < CatOrDog >.",
                        "path": None,
                        "locations": [{"line": 3, "column": 36}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
                    },
                    {
                        "message": "Variable < $a > is not defined.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 30},
                            {"line": 2, "column": 13},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.3",
                            "tag": "all-variable-uses-defined",
                            "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                        },
                    },
                ],
            },
        ),
        (
            """
            query {
                ... {
                    catOrDog(id: $a) {
                        name @skip(if: $b)
                        knowCommands @include(if: $b)
                    }
                }
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot query field < name > on type < CatOrDog >.",
                        "path": None,
                        "locations": [{"line": 5, "column": 25}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
                    },
                    {
                        "message": "Cannot query field < knowCommands > on type < CatOrDog >.",
                        "path": None,
                        "locations": [{"line": 6, "column": 25}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
                    },
                    {
                        "message": "Variable < $a > is not defined.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 34},
                            {"line": 2, "column": 13},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.3",
                            "tag": "all-variable-uses-defined",
                            "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                        },
                    },
                    {
                        "message": "Variable < $b > is not defined.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 40},
                            {"line": 2, "column": 13},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.3",
                            "tag": "all-variable-uses-defined",
                            "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                        },
                    },
                    {
                        "message": "Variable < $b > is not defined.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 51},
                            {"line": 2, "column": 13},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.3",
                            "tag": "all-variable-uses-defined",
                            "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                        },
                    },
                ],
            },
        ),
        (
            """
            query {
                ... {
                    catOrDog(id: $a) {
                        name @skip(if: $b)
                        knowCommands @include(if: $b)
                    }
                }
            }
            query anotherQuery($a: Int) {
                ... {
                    catOrDog(id: $a) {
                        name @skip(if: $b)
                        knowCommands @include(if: $b)
                    }
                }
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "This anonymous operation must be the only defined operation.",
                        "path": None,
                        "locations": [{"line": 2, "column": 13}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.2.2.1",
                            "tag": "lone-anonymous-operation",
                            "details": "https://spec.graphql.org/June2018/#sec-Lone-Anonymous-Operation",
                        },
                    },
                    {
                        "message": "Cannot query field < name > on type < CatOrDog >.",
                        "path": None,
                        "locations": [{"line": 5, "column": 25}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
                    },
                    {
                        "message": "Cannot query field < knowCommands > on type < CatOrDog >.",
                        "path": None,
                        "locations": [{"line": 6, "column": 25}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
                    },
                    {
                        "message": "Variable < $a > is not defined.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 34},
                            {"line": 2, "column": 13},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.3",
                            "tag": "all-variable-uses-defined",
                            "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                        },
                    },
                    {
                        "message": "Variable < $b > is not defined.",
                        "path": None,
                        "locations": [
                            {"line": 5, "column": 40},
                            {"line": 2, "column": 13},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.3",
                            "tag": "all-variable-uses-defined",
                            "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                        },
                    },
                    {
                        "message": "Variable < $b > is not defined.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 51},
                            {"line": 2, "column": 13},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.3",
                            "tag": "all-variable-uses-defined",
                            "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                        },
                    },
                    {
                        "message": "Cannot query field < name > on type < CatOrDog >.",
                        "path": None,
                        "locations": [{"line": 13, "column": 25}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
                    },
                    {
                        "message": "Cannot query field < knowCommands > on type < CatOrDog >.",
                        "path": None,
                        "locations": [{"line": 14, "column": 25}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
                    },
                    {
                        "message": "Variable < $b > is not defined by operation < anotherQuery >.",
                        "path": None,
                        "locations": [
                            {"line": 13, "column": 40},
                            {"line": 10, "column": 13},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.3",
                            "tag": "all-variable-uses-defined",
                            "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                        },
                    },
                    {
                        "message": "Variable < $b > is not defined by operation < anotherQuery >.",
                        "path": None,
                        "locations": [
                            {"line": 14, "column": 51},
                            {"line": 10, "column": 13},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.3",
                            "tag": "all-variable-uses-defined",
                            "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                        },
                    },
                    {
                        "message": "Variable < $a > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 10, "column": 32},
                            {"line": 12, "column": 34},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
        (
            """
            fragment DogFragment on Dog {
                name @skip(if: $c)
                doesKnowCommand(command: $d)
                ... {
                    tryThis @include(if: $f)
                }
                ...anotherDogFragment
            }

            fragment anotherDogFragment on Dog {
                aField(id: $f)
            }

            query {
                ... {
                    catOrDog(id: $a) {
                        name @skip(if: $b)
                        knowCommands @include(if: $b)
                    }
                }
            }
            query anotherQuery($a: Int) {
                ... {
                    catOrDog(id: $a) {
                        name @skip(if: $b)
                        knowCommands @include(if: $b)
                        ...DogFragment
                    }
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
                    {
                        "message": "Cannot query field < tryThis > on type < Dog >.",
                        "path": None,
                        "locations": [{"line": 6, "column": 21}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
                    },
                    {
                        "message": "Cannot query field < aField > on type < Dog >.",
                        "path": None,
                        "locations": [{"line": 12, "column": 17}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
                    },
                    {
                        "message": "This anonymous operation must be the only defined operation.",
                        "path": None,
                        "locations": [{"line": 15, "column": 13}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.2.2.1",
                            "tag": "lone-anonymous-operation",
                            "details": "https://spec.graphql.org/June2018/#sec-Lone-Anonymous-Operation",
                        },
                    },
                    {
                        "message": "Cannot query field < name > on type < CatOrDog >.",
                        "path": None,
                        "locations": [{"line": 18, "column": 25}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
                    },
                    {
                        "message": "Cannot query field < knowCommands > on type < CatOrDog >.",
                        "path": None,
                        "locations": [{"line": 19, "column": 25}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
                    },
                    {
                        "message": "Variable < $a > is not defined.",
                        "path": None,
                        "locations": [
                            {"line": 17, "column": 34},
                            {"line": 15, "column": 13},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.3",
                            "tag": "all-variable-uses-defined",
                            "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                        },
                    },
                    {
                        "message": "Variable < $b > is not defined.",
                        "path": None,
                        "locations": [
                            {"line": 18, "column": 40},
                            {"line": 15, "column": 13},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.3",
                            "tag": "all-variable-uses-defined",
                            "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                        },
                    },
                    {
                        "message": "Variable < $b > is not defined.",
                        "path": None,
                        "locations": [
                            {"line": 19, "column": 51},
                            {"line": 15, "column": 13},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.3",
                            "tag": "all-variable-uses-defined",
                            "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                        },
                    },
                    {
                        "message": "Cannot query field < name > on type < CatOrDog >.",
                        "path": None,
                        "locations": [{"line": 26, "column": 25}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
                    },
                    {
                        "message": "Cannot query field < knowCommands > on type < CatOrDog >.",
                        "path": None,
                        "locations": [{"line": 27, "column": 25}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
                    },
                    {
                        "message": "Variable < $b > is not defined by operation < anotherQuery >.",
                        "path": None,
                        "locations": [
                            {"line": 26, "column": 40},
                            {"line": 23, "column": 13},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.3",
                            "tag": "all-variable-uses-defined",
                            "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                        },
                    },
                    {
                        "message": "Variable < $b > is not defined by operation < anotherQuery >.",
                        "path": None,
                        "locations": [
                            {"line": 27, "column": 51},
                            {"line": 23, "column": 13},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.3",
                            "tag": "all-variable-uses-defined",
                            "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                        },
                    },
                    {
                        "message": "Variable < $c > is not defined by operation < anotherQuery >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 32},
                            {"line": 23, "column": 13},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.3",
                            "tag": "all-variable-uses-defined",
                            "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                        },
                    },
                    {
                        "message": "Variable < $d > is not defined by operation < anotherQuery >.",
                        "path": None,
                        "locations": [
                            {"line": 4, "column": 42},
                            {"line": 23, "column": 13},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.3",
                            "tag": "all-variable-uses-defined",
                            "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                        },
                    },
                    {
                        "message": "Variable < $f > is not defined by operation < anotherQuery >.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 42},
                            {"line": 23, "column": 13},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.3",
                            "tag": "all-variable-uses-defined",
                            "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                        },
                    },
                    {
                        "message": "Variable < $f > is not defined by operation < anotherQuery >.",
                        "path": None,
                        "locations": [
                            {"line": 12, "column": 28},
                            {"line": 23, "column": 13},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.3",
                            "tag": "all-variable-uses-defined",
                            "details": "http://spec.graphql.org/June2018/#sec-All-Variable-Uses-Defined",
                        },
                    },
                    {
                        "message": "Variable < $a > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 23, "column": 32},
                            {"line": 25, "column": 34},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
    ],
)
async def test_validators_all_variable_uses_defined(query, expected, engine):
    assert await engine.execute(query) == expected
