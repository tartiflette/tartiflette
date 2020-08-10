import pytest


@pytest.mark.asyncio
@pytest.mark.ttftt_engine
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
                        "message": "Field < name > must not have a selection since type < String! > has no subfields.",
                        "path": None,
                        "locations": [{"line": 4, "column": 26}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.3",
                            "tag": "leaf-field-selections",
                            "details": "https://spec.graphql.org/June2018/#sec-Leaf-Field-Selections",
                        },
                    }
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
                        "message": "Field < dog > of type < Dog > must have a selection of subfields. Did you mean < dog { ... } >?",
                        "path": None,
                        "locations": [{"line": 3, "column": 17}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.3",
                            "tag": "leaf-field-selections",
                            "details": "https://spec.graphql.org/June2018/#sec-Leaf-Field-Selections",
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
                        "message": "Field < name > must not have a selection since type < String! > has no subfields.",
                        "path": None,
                        "locations": [{"line": 3, "column": 22}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.3",
                            "tag": "leaf-field-selections",
                            "details": "https://spec.graphql.org/June2018/#sec-Leaf-Field-Selections",
                        },
                    }
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
                        "message": "Field < name > must not have a selection since type < String! > has no subfields.",
                        "path": None,
                        "locations": [{"line": 5, "column": 30}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.3",
                            "tag": "leaf-field-selections",
                            "details": "https://spec.graphql.org/June2018/#sec-Leaf-Field-Selections",
                        },
                    }
                ],
            },
        ),
    ],
)
async def test_issue109(query, expected, engine):
    assert await engine.execute(query) == expected
