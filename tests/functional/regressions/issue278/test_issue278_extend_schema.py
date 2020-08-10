import pytest

from tartiflette import Resolver, create_engine
from tartiflette.types.exceptions.tartiflette import GraphQLSchemaError
from tests.functional.utils import match_schema_errors


@pytest.fixture(scope="module")
async def ttftt_engine():
    schema_sdl = """
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
    """

    @Resolver("aType.vala", schema_name="test_issue_278_schema_extend")
    async def resolver_enum_test_1(*args, **kwargs):
        return {"b": "LOL"}

    return await create_engine(
        schema_sdl, schema_name="test_issue_278_schema_extend"
    )


@pytest.mark.asyncio
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
async def test_issue_278_schema_extend(query, expected, ttftt_engine):
    assert await ttftt_engine.execute(query) == expected


@pytest.mark.asyncio
async def test_issue_278_schema_extend_invalid_sdl():
    with pytest.raises(GraphQLSchemaError) as excinfo:
        await create_engine(
            sdl="""
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
            schema_name="test_issue_278_schema_extend_invalid_sdl",
        )

    match_schema_errors(
        excinfo.value, ["There can be only one < query > type in schema."],
    )
