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

        type aType {
            a: String
            b: Int
        }

        input switchValueInput {
            c: Int
        }

        directive @switchValue(newValue: switchValueInput) on OBJECT

        extend type aType @switchValue(newValue: {c: 5}) {
            c: Int
            t: Boolean
        }
    """

    @Directive(name="switchValue", schema_name="test_issue_278_object_extend")
    class SwitchValue:
        @staticmethod
        async def on_pre_output_coercion(
            directive_args: Dict[str, Any],
            next_directive: Callable,
            value: Any,
            ctx: Optional[Any],
            info: "ResolveInfo",
        ):
            value = await next_directive(value, ctx, info)
            value.update(directive_args["newValue"])
            return value

    @Resolver("Query.test1", schema_name="test_issue_278_object_extend")
    async def resolver_object_test_1(*_args, **_kwargs):
        return {"a": "Hey", "b": 6, "c": 9, "t": True}

    return await create_engine(
        schema_sdl, schema_name="test_issue_278_object_extend"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
        query {
            __type(name: "aType") {
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
                        "name": "aType",
                        "kind": "OBJECT",
                        "fields": [
                            {"name": "a"},
                            {"name": "b"},
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
                }
            }
            """,
            {"data": {"test1": {"a": "Hey", "b": 6, "c": 5, "t": True}}},
        ),
    ],
)
async def test_issue_278_object_extend(query, expected, ttftt_engine):
    assert await ttftt_engine.execute(query) == expected


@pytest.mark.asyncio
async def test_issue_278_extend_object_invalid_sdl():
    with pytest.raises(
        GraphQLSchemaError,
        match="""

0: Can't add Field < a > to TYPE < bob > cause field already exists.
1: Can't add Field < b > to TYPE < bob > cause field already exists.
2: Can't add < C > Directive to < bob > TYPE, cause it's already there.
3: Can't extend a non existing type < dontexists >.
4: Can't extend TYPE < aType > cause it's not an TYPE.
5: Can't add Interface < a > to TYPE < anotherType > cause Interface already exists.""",
    ):
        await create_engine(
            sdl="""
                directive @C on OBJECT

                type bob @C {
                    a: String
                    b: Int
                }

                extend type bob @C {
                    a: String
                    b: Int
                }

                scalar aType

                type Query {
                    a: bob
                }

                extend type dontexists @C

                extend type aType {
                    d: Float
                }

                interface a {
                    c: Int
                }

                type anotherType implements a {
                    c: Int
                    r: String
                }

                extend type anotherType implements a

            """,
            schema_name="test_issue_278_extend_object_invalid_sdl",
        )
