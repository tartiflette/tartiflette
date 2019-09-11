from typing import Any, Callable, Dict, Optional

import pytest

from tartiflette import Directive, Resolver, create_engine
from tartiflette.types.exceptions.tartiflette import GraphQLSchemaError


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

        union bobby @deprecated = aType | anotherType

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
    with pytest.raises(
        GraphQLSchemaError,
        match="""

0: Can't add PossibleType < String > to UNION < bob > cause PossibleType already exists.
1: Can't add < deprecated > Directive to < bob > UNION, cause it's already there.
2: Can't extend a non existing type < dontexists >.
3: Can't extend UNION < aType > cause it's not an UNION.""",
    ):
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
