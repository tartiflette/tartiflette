import pytest

from tartiflette import Resolver, create_schema
from tartiflette.types.exceptions.tartiflette import GraphQLSchemaError
from tests.functional.utils import match_schema_errors


def bakery(schema_name):
    @Resolver("aType.vala", schema_name=schema_name)
    async def resolver_enum_test_1(*args, **kwargs):
        return {"b": "LOL"}


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    type anotherType {
        b: String
    }

    type aType {
        vala: anotherType
    }

    schema {
        query: aType
    }

    extend schema {
        mutation: aType
    }
    """,
    bakery=bakery,
)
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query {
                __schema {
                    queryType { name }
                    mutationType { name }
                    subscriptionType { name }
                }
            }
            """,
            {
                "data": {
                    "__schema": {
                        "queryType": {"name": "aType"},
                        "mutationType": {"name": "aType"},
                        "subscriptionType": None,
                    }
                }
            },
        ),
        (
            """
        query {
            vala {
                b
            }
        }""",
            {"data": {"vala": {"b": "LOL"}}},
        ),
    ],
)
async def test_issue_278_schema_extend(schema_stack, query, expected):
    assert await schema_stack.execute(query) == expected


@pytest.mark.asyncio
async def test_issue_278_schema_extend_invalid_sdl():
    with pytest.raises(GraphQLSchemaError) as excinfo:
        await create_schema(
            """
                type aType {
                    b: String
                }

                extend schema {
                    query: aType
                }

                extend schema {
                    query: aType
                }

                type Mutation {
                    g: String
                }

                extend schema {
                    mutation: aType
                }
            """,
            name="test_issue_278_schema_extend_invalid_sdl",
        )

    match_schema_errors(
        excinfo.value, ["There can be only one < query > type in schema."]
    )
