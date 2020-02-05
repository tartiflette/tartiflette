import pytest


async def resolve_dog(*_, **__):
    return {"name": "JeanMichel"}


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(resolvers={"Query.dog": resolve_dog})
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
                        "message": "Can't have multiple Input Field named < field4 >.",
                        "path": ["dog"],
                        "locations": [
                            {"line": 3, "column": 58},
                            {"line": 3, "column": 69},
                        ],
                        "extensions": {
                            "rule": "5.6.3",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Input-Object-Field-Uniqueness",
                            "tag": "input-object-field-uniqueness",
                        },
                    },
                    {
                        "message": "Can't have multiple Input Field named < field1 >.",
                        "path": ["dog"],
                        "locations": [
                            {"line": 3, "column": 27},
                            {"line": 3, "column": 38},
                        ],
                        "extensions": {
                            "rule": "5.6.3",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Input-Object-Field-Uniqueness",
                            "tag": "input-object-field-uniqueness",
                        },
                    },
                    {
                        "message": "Provided Argument < bob > doesn't exist on field < Query.dog >.",
                        "path": ["dog"],
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
        )
    ],
)
async def test_validators_input_object_field_uniqueness(
    query, expected, engine
):
    assert await engine.execute(query) == expected
