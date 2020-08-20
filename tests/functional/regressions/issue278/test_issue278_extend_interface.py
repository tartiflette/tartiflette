import pytest

from tartiflette import Resolver, create_schema
from tartiflette.types.exceptions.tartiflette import GraphQLSchemaError
from tests.functional.utils import match_schema_errors


def bakery(schema_name):
    @Resolver("Query.test1", schema_name=schema_name)
    async def resolver_interface_test_1(*_args, **_kwargs):
        return {"a": "Hey", "b": 6, "c": 9, "t": True, "h": 6, "d": "GG"}


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
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
    """,
    bakery=bakery,
)
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
async def test_issue_278_interface_extend(schema_stack, query, expected):
    assert await schema_stack.execute(query) == expected


@pytest.mark.asyncio
async def test_issue_278_extend_interface_invalid_sdl():
    with pytest.raises(GraphQLSchemaError) as excinfo:
        await create_schema(
            """
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
            name="test_issue_278_extend_interface_invalid_sdl",
        )

    match_schema_errors(
        excinfo.value,
        [
            "Field < bob.a > can only be defined once.",
            "Field < bob.b > can only be defined once.",
            "The directive < @C > can only be used once at this location.",
            "Cannot extend type < dontexists > because it is not defined.",
            "Cannot extend non-scalar type < aType >.",
            "Unknown directive < @c >.",
        ],
    )
