from typing import Any, Callable, Dict, Optional

import pytest

from tartiflette import Directive, Resolver, create_schema
from tartiflette.types.exceptions.tartiflette import GraphQLSchemaError
from tests.functional.utils import match_schema_errors


def bakery(schema_name):
    @Directive(name="switchValue", schema_name=schema_name)
    class SwitchValue:
        @staticmethod
        async def on_pre_output_coercion(
            directive_args: Dict[str, Any],
            next_directive: Callable,
            output_definition_node,
            value: Any,
            ctx: Optional[Any],
            info: "ResolveInfo",
        ):
            value = await next_directive(
                output_definition_node, value, ctx, info
            )
            value.update(directive_args["newValue"])
            return value

    @Resolver("Query.test1", schema_name=schema_name)
    async def resolver_object_test_1(*_args, **_kwargs):
        return {"a": "Hey", "b": 6, "c": 9, "t": True}


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
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
    """,
    bakery=bakery,
)
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
async def test_issue_278_object_extend(schema_stack, query, expected):
    assert await schema_stack.execute(query) == expected


@pytest.mark.asyncio
async def test_issue_278_extend_object_invalid_sdl():
    with pytest.raises(GraphQLSchemaError) as excinfo:
        await create_schema(
            """
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
            name="test_issue_278_extend_object_invalid_sdl",
        )

    match_schema_errors(
        excinfo.value,
        [
            "Field < bob.a > can only be defined once.",
            "Field < bob.b > can only be defined once.",
            "The directive < @C > can only be used once at this location.",
            "Cannot extend type < dontexists > because it is not defined.",
            "Cannot extend non-scalar type < aType >.",
            "Type < anotherType > can only implement < a > once.",
        ],
    )
