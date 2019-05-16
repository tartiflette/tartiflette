import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query {
                dog {
                    name {
                        a
                    }
                }
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Field a doesn't exist on String",
                        "path": ["dog", "name", "a"],
                        "locations": [{"line": 5, "column": 25}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field name must not have a selection since type String has no subfields.",
                        "path": ["dog", "name"],
                        "locations": [{"line": 4, "column": 21}],
                        "extensions": {
                            "rule": "5.3.3",
                            "tag": "leaf-field-selections",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Leaf-Field-Selections",
                            "spec": "June 2018",
                        },
                    },
                ],
            },
        ),
        (
            """
            query {
                dog
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Field dog of type Dog must have a selection of subfields.",
                        "path": ["dog"],
                        "locations": [{"line": 3, "column": 17}],
                        "extensions": {
                            "rule": "5.3.3",
                            "tag": "leaf-field-selections",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Leaf-Field-Selections",
                            "spec": "June 2018",
                        },
                    }
                ],
            },
        ),
        (
            """
            fragment doggy on Dog {
                name {
                    a
                }
            }
            query {
                dog {
                    ... doggy
                }
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Field a doesn't exist on String",
                        "path": ["name", "a"],
                        "locations": [{"line": 4, "column": 21}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field name must not have a selection since type String has no subfields.",
                        "path": ["name"],
                        "locations": [{"line": 3, "column": 17}],
                        "extensions": {
                            "rule": "5.3.3",
                            "tag": "leaf-field-selections",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Leaf-Field-Selections",
                            "spec": "June 2018",
                        },
                    },
                ],
            },
        ),
        (
            """
            query {
                dog {
                    ... on Dog {
                        name {
                            a
                        }
                    }
                }
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Field a doesn't exist on String",
                        "path": ["dog", "name", "a"],
                        "locations": [{"line": 6, "column": 29}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field name must not have a selection since type String has no subfields.",
                        "path": ["dog", "name"],
                        "locations": [{"line": 5, "column": 25}],
                        "extensions": {
                            "rule": "5.3.3",
                            "tag": "leaf-field-selections",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Leaf-Field-Selections",
                            "spec": "June 2018",
                        },
                    },
                ],
            },
        ),
    ],
)
@pytest.mark.ttftt_engine()
async def test_issue109(query, expected, engine):
    assert await engine.execute(query) == expected
