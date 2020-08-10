import pytest


@pytest.mark.asyncio
@pytest.mark.ttftt_engine
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            fragment aFragment on String { name }

            query { devs { name preferredLanguage ...aFragment ...anotherFragment } }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Fragment < aFragment > cannot condition on non composite type < String >.",
                        "path": None,
                        "locations": [{"line": 2, "column": 35}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.5.1.3",
                            "tag": "fragments-on-composite-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Fragments-On-Composite-Types",
                        },
                    },
                    {
                        "message": "Cannot query field < devs > on type < Query >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 21}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.1",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                        },
                    },
                    {
                        "message": "Unknown fragment < anotherFragment >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 67}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.5.2.1",
                            "tag": "fragment-spread-target-defined",
                            "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-target-defined",
                        },
                    },
                ],
            },
        ),
        (
            """
            query { dog { name { ... on String { nothing } } }}
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Field < name > must not have a selection since type < String! > has no subfields.",
                        "path": None,
                        "locations": [{"line": 2, "column": 32}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.3",
                            "tag": "leaf-field-selections",
                            "details": "https://spec.graphql.org/June2018/#sec-Leaf-Field-Selections",
                        },
                    },
                    {
                        "message": "Fragment cannot condition on non composite type < String >.",
                        "path": None,
                        "locations": [{"line": 2, "column": 41}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.5.1.3",
                            "tag": "fragments-on-composite-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Fragments-On-Composite-Types",
                        },
                    },
                ],
            },
        ),
    ],
)
async def test_validators_fragment_on_composite_type(query, expected, engine):
    assert await engine.execute(query) == expected
