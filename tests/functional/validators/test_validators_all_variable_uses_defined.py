import pytest


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
                        "message": "Field name doesn't exist on CatOrDog",
                        "path": ["catOrDog", "name"],
                        "locations": [{"line": 3, "column": 36}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Undefined Varibable < a > in anonymous Operation.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 13},
                            {"line": 3, "column": 30},
                        ],
                        "extensions": {
                            "rule": "5.8.3",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Uses-Defined",
                            "tag": "all-variable-uses-defined",
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
                        "message": "Field name doesn't exist on CatOrDog",
                        "path": ["catOrDog", "name"],
                        "locations": [{"line": 5, "column": 25}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field knowCommands doesn't exist on CatOrDog",
                        "path": ["catOrDog", "knowCommands"],
                        "locations": [{"line": 6, "column": 25}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Undefined Varibable < a > in anonymous Operation.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 13},
                            {"line": 4, "column": 34},
                        ],
                        "extensions": {
                            "rule": "5.8.3",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Uses-Defined",
                            "tag": "all-variable-uses-defined",
                        },
                    },
                    {
                        "message": "Undefined Varibable < b > in anonymous Operation.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 13},
                            {"line": 5, "column": 40},
                            {"line": 6, "column": 51},
                        ],
                        "extensions": {
                            "rule": "5.8.3",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Uses-Defined",
                            "tag": "all-variable-uses-defined",
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
                        "message": "Field name doesn't exist on CatOrDog",
                        "path": ["catOrDog", "name"],
                        "locations": [{"line": 5, "column": 25}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field knowCommands doesn't exist on CatOrDog",
                        "path": ["catOrDog", "knowCommands"],
                        "locations": [{"line": 6, "column": 25}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field name doesn't exist on CatOrDog",
                        "path": ["catOrDog", "name"],
                        "locations": [{"line": 13, "column": 25}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field knowCommands doesn't exist on CatOrDog",
                        "path": ["catOrDog", "knowCommands"],
                        "locations": [{"line": 14, "column": 25}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Anonymous operation must be the only defined operation.",
                        "path": None,
                        "locations": [{"line": 2, "column": 13}],
                        "extensions": {
                            "rule": "5.2.2.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Lone-Anonymous-Operation",
                            "tag": "lone-anonymous-operation",
                        },
                    },
                    {
                        "message": "Undefined Varibable < a > in anonymous Operation.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 13},
                            {"line": 4, "column": 34},
                        ],
                        "extensions": {
                            "rule": "5.8.3",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Uses-Defined",
                            "tag": "all-variable-uses-defined",
                        },
                    },
                    {
                        "message": "Undefined Varibable < b > in anonymous Operation.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 13},
                            {"line": 5, "column": 40},
                            {"line": 6, "column": 51},
                        ],
                        "extensions": {
                            "rule": "5.8.3",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Uses-Defined",
                            "tag": "all-variable-uses-defined",
                        },
                    },
                    {
                        "message": "Undefined Varibable < b > in Operation < anotherQuery >.",
                        "path": None,
                        "locations": [
                            {"line": 10, "column": 13},
                            {"line": 13, "column": 40},
                            {"line": 14, "column": 51},
                        ],
                        "extensions": {
                            "rule": "5.8.3",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Uses-Defined",
                            "tag": "all-variable-uses-defined",
                        },
                    },
                    {
                        "message": "Can't use < $a / Int > for type < Int! >.",
                        "path": ["catOrDog"],
                        "locations": [
                            {"line": 10, "column": 32},
                            {"line": 12, "column": 34},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
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
                    {
                        "message": "Field tryThis doesn't exist on Dog",
                        "path": ["tryThis"],
                        "locations": [{"line": 6, "column": 21}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field aField doesn't exist on Dog",
                        "path": ["aField"],
                        "locations": [{"line": 12, "column": 17}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field name doesn't exist on CatOrDog",
                        "path": ["catOrDog", "name"],
                        "locations": [{"line": 18, "column": 25}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field knowCommands doesn't exist on CatOrDog",
                        "path": ["catOrDog", "knowCommands"],
                        "locations": [{"line": 19, "column": 25}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field name doesn't exist on CatOrDog",
                        "path": ["catOrDog", "name"],
                        "locations": [{"line": 26, "column": 25}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field knowCommands doesn't exist on CatOrDog",
                        "path": ["catOrDog", "knowCommands"],
                        "locations": [{"line": 27, "column": 25}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Anonymous operation must be the only defined operation.",
                        "path": None,
                        "locations": [{"line": 15, "column": 13}],
                        "extensions": {
                            "rule": "5.2.2.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Lone-Anonymous-Operation",
                            "tag": "lone-anonymous-operation",
                        },
                    },
                    {
                        "message": "Undefined Varibable < a > in anonymous Operation.",
                        "path": None,
                        "locations": [
                            {"line": 15, "column": 13},
                            {"line": 17, "column": 34},
                        ],
                        "extensions": {
                            "rule": "5.8.3",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Uses-Defined",
                            "tag": "all-variable-uses-defined",
                        },
                    },
                    {
                        "message": "Undefined Varibable < b > in anonymous Operation.",
                        "path": None,
                        "locations": [
                            {"line": 15, "column": 13},
                            {"line": 18, "column": 40},
                            {"line": 19, "column": 51},
                        ],
                        "extensions": {
                            "rule": "5.8.3",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Uses-Defined",
                            "tag": "all-variable-uses-defined",
                        },
                    },
                    {
                        "message": "Undefined Varibable < b > in Operation < anotherQuery >.",
                        "path": None,
                        "locations": [
                            {"line": 23, "column": 13},
                            {"line": 26, "column": 40},
                            {"line": 27, "column": 51},
                        ],
                        "extensions": {
                            "rule": "5.8.3",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Uses-Defined",
                            "tag": "all-variable-uses-defined",
                        },
                    },
                    {
                        "message": "Undefined Varibable < f > in Operation < anotherQuery >.",
                        "path": None,
                        "locations": [
                            {"line": 23, "column": 13},
                            {"line": 12, "column": 28},
                            {"line": 6, "column": 42},
                        ],
                        "extensions": {
                            "rule": "5.8.3",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Uses-Defined",
                            "tag": "all-variable-uses-defined",
                        },
                    },
                    {
                        "message": "Undefined Varibable < c > in Operation < anotherQuery >.",
                        "path": None,
                        "locations": [
                            {"line": 23, "column": 13},
                            {"line": 3, "column": 32},
                        ],
                        "extensions": {
                            "rule": "5.8.3",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Uses-Defined",
                            "tag": "all-variable-uses-defined",
                        },
                    },
                    {
                        "message": "Undefined Varibable < d > in Operation < anotherQuery >.",
                        "path": None,
                        "locations": [
                            {"line": 23, "column": 13},
                            {"line": 4, "column": 42},
                        ],
                        "extensions": {
                            "rule": "5.8.3",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Uses-Defined",
                            "tag": "all-variable-uses-defined",
                        },
                    },
                    {
                        "message": "Can't use < $a / Int > for type < Int! >.",
                        "path": ["catOrDog"],
                        "locations": [
                            {"line": 23, "column": 32},
                            {"line": 25, "column": 34},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                ],
            },
        ),
    ],
)
@pytest.mark.asyncio
@pytest.mark.ttftt_engine
async def test_validators_all_variable_uses_defined(query, expected, engine):
    assert await engine.execute(query) == expected
