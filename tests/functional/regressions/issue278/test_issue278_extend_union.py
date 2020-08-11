import pytest

from tartiflette import create_engine
from tartiflette.types.exceptions.tartiflette import GraphQLSchemaError
from tests.functional.utils import match_schema_errors


@pytest.fixture(scope="module")
async def ttftt_engine():
    schema_sdl = """
        type aType {
            a:String
            b:Int
        }

        type anotherType {
            c: String
            d: Float
        }

        type lol {
            g: String
            p: Boolean
        }

        union bobby = aType | anotherType

        type Query {
            a: bobby
        }

        extend union bobby = lol
    """

    return await create_engine(
        schema_sdl, schema_name="test_issue_278_union_extend"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
        query {
            __type(name: "bobby") {
            name
            kind
            possibleTypes {
                name
            }
        } }
        """,
            {
                "data": {
                    "__type": {
                        "name": "bobby",
                        "kind": "UNION",
                        "possibleTypes": [
                            {"name": "aType"},
                            {"name": "anotherType"},
                            {"name": "lol"},
                        ],
                    }
                }
            },
        )
    ],
)
async def test_issue_278_union_extend(query, expected, ttftt_engine):
    assert await ttftt_engine.execute(query) == expected


@pytest.mark.asyncio
async def test_issue_278_union_extend_invalid_sdl():
    with pytest.raises(GraphQLSchemaError) as excinfo:
        await create_engine(
            sdl="""
                union bob @deprecated = String | Int

                extend union bob @deprecated = String

                type aType {
                    b: bob
                }

                type Query {
                    a: bob
                }

                extend union dontexists @deprecated

                extend union aType = Float
            """,
            schema_name="test_issue_278_union_extend_invalid_sdl",
        )

    match_schema_errors(
        excinfo.value,
        [
            "Directive < @deprecated > may not be used on UNION.",
            "The directive < @deprecated > can only be used once at this location.",
            "Union type < bob > can only include type < String > once.",
            "Directive < @deprecated > may not be used on UNION.",
            "Cannot extend type < dontexists > because it is not defined.",
            "Directive < @deprecated > may not be used on UNION.",
            "Cannot extend non-object type < aType >.",
            "Union type < bob > can only include Object types, it cannot include < String >.",
            "Union type < bob > can only include Object types, it cannot include < Int >.",
            "Union type < aType > can only include Object types, it cannot include < Float >.",
        ],
    )
