import pytest

from tartiflette import Resolver


def bakery(schema_name):
    @Resolver("Query.dog", schema_name=schema_name)
    async def resolve_query_dog(*_, **__):
        return {"name": "JeanMichel"}


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="animals", bakery=bakery)
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query lol {
                dog(bob: {field1: 1, field1: 2, field3: {field4: 1, field4: 3, field1: 5}}) {
                    name
                }
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Unknown argument < bob > on field < Query.dog >.",
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
                        "message": "There can be only one input field named < field1 >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 27},
                            {"line": 3, "column": 38},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.3",
                            "tag": "input-object-field-uniqueness",
                            "details": "https://spec.graphql.org/June2018/#sec-Input-Object-Field-Uniqueness",
                        },
                    },
                    {
                        "message": "There can be only one input field named < field4 >.",
                        "path": None,
                        "locations": [
                            {"line": 3, "column": 58},
                            {"line": 3, "column": 69},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.6.3",
                            "tag": "input-object-field-uniqueness",
                            "details": "https://spec.graphql.org/June2018/#sec-Input-Object-Field-Uniqueness",
                        },
                    },
                ],
            },
        )
    ],
)
async def test_validators_input_object_field_uniqueness(
    schema_stack, query, expected
):
    assert await schema_stack.execute(query) == expected
