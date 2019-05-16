import pytest

from tartiflette import create_engine


@pytest.mark.ttftt_engine
@pytest.mark.asyncio
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
                        "message": "Field name doesn't exist on String",
                        "path": ["name"],
                        "locations": [{"line": 2, "column": 44}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Fragment aFragment cannot condition on non composite type String.",
                        "path": None,
                        "locations": [{"line": 2, "column": 13}],
                        "extensions": {
                            "rule": "5.5.1.3",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Fragments-On-Composite-Types",
                            "tag": "fragments-on-composite-types",
                        },
                    },
                    {
                        "message": "Field name doesn't exist on Root",
                        "path": ["devs", "name"],
                        "locations": [{"line": 4, "column": 28}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field preferredLanguage doesn't exist on Root",
                        "path": ["devs", "preferredLanguage"],
                        "locations": [{"line": 4, "column": 33}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Field devs doesn't exist on Query",
                        "path": ["devs"],
                        "locations": [{"line": 4, "column": 21}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Unknown Fragment for Spread < anotherFragment >.",
                        "path": None,
                        "locations": [{"line": 4, "column": 64}],
                        "extensions": {
                            "rule": "5.5.2.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-spread-target-defined",
                            "tag": "fragment-spread-target-defined",
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
                        "message": "Field nothing doesn't exist on String",
                        "path": ["dog", "name", "nothing"],
                        "locations": [{"line": 2, "column": 50}],
                        "extensions": {
                            "rule": "5.3.1",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                            "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        },
                    },
                    {
                        "message": "Inline Fragment cannot condition on non composite type String.",
                        "path": ["dog", "name"],
                        "locations": [{"line": 2, "column": 34}],
                        "extensions": {
                            "rule": "5.5.1.3",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Fragments-On-Composite-Types",
                            "tag": "fragments-on-composite-types",
                        },
                    },
                    {
                        "message": "Field name must not have a selection since type String has no subfields.",
                        "path": ["dog", "name"],
                        "locations": [{"line": 2, "column": 27}],
                        "extensions": {
                            "rule": "5.3.3",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Leaf-Field-Selections",
                            "tag": "leaf-field-selections",
                        },
                    },
                ],
            },
        ),
    ],
)
async def test_validators_fragment_on_composite_type(query, expected, engine):
    assert await engine.execute(query) == expected
