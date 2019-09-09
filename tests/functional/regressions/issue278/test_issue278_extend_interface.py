from typing import Any, Callable, Dict, Optional

import pytest

from tartiflette import Directive, Resolver, create_engine
from tartiflette.types.exceptions.tartiflette import GraphQLSchemaError


@pytest.fixture(scope="module")
async def ttftt_engine():
    schema_sdl = """
        type Query {
            test1: aType
        }

        type aType implements anInterface {
            a: String
            b: Int
            h: Int
            d: String
        }

        interface anInterface {
            h: Int
            d: String
        }

        extend interface anInterface {
            c: Int
            t: Boolean
        }

        extend type aType {
            c: Int
            t: Boolean
        }
    """

    @Resolver("Query.test1", schema_name="test_issue_278_interface_extend")
    async def resolver_interface_test_1(*_args, **_kwargs):
        return {"a": "Hey", "b": 6, "c": 9, "t": True, "h": 6, "d": "GG"}

    return await create_engine(
        schema_sdl, schema_name="test_issue_278_interface_extend"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
        query {
            __type(name: "anInterface") {
            name
            kind
            fields {
                name
            }
        } }
        """,
            {
                "data": {
                    "__type": {
                        "name": "anInterface",
                        "kind": "INTERFACE",
                        "fields": [
                            {"name": "h"},
                            {"name": "d"},
                            {"name": "c"},
                            {"name": "t"},
                        ],
                    }
                }
            },
        ),
        (
            """
            query {
                test1 {
                    a
                    b
                    c
                    t
                    h
                    d
                }
            }
            """,
            {
                "data": {
                    "test1": {
                        "a": "Hey",
                        "b": 6,
                        "c": 9,
                        "t": True,
                        "h": 6,
                        "d": "GG",
                    }
                }
            },
        ),
    ],
)
async def test_issue_278_interface_extend(query, expected, ttftt_engine):
    assert await ttftt_engine.execute(query) == expected


@pytest.mark.asyncio
async def test_issue_278_extend_interface_invalid_sdl():
    with pytest.raises(
        GraphQLSchemaError,
        match="""

0: Can't add Field < a > to INTERFACE < bob > cause field already exists.
1: Can't add Field < b > to INTERFACE < bob > cause field already exists.
2: Can't add < C > Directive to < bob > INTERFACE, cause it's already there.
3: Can't extend a non existing type < dontexists >.
4: Can't extend INTERFACE < aType > cause it's not an INTERFACE.""",
    ):
        await create_engine(
            sdl="""
                directive @C on INTERFACE

                interface bob @C {
                    a: String
                    b: Int
                }

                extend interface bob @C {
                    a: String
                    b: Int
                }

                scalar aType

                type Query {
                    a: bob
                }

                extend interface dontexists @C

                extend interface aType {
                    d: Float
                }

                interface a {
                    c: Int
                }

                extend interface a @c
            """,
            schema_name="test_issue_278_extend_interface_invalid_sdl",
        )
