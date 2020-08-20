from typing import Any, Callable, Dict, Optional

import pytest

from tartiflette import Directive, Resolver, create_schema
from tartiflette.types.exceptions.tartiflette import GraphQLSchemaError
from tests.functional.utils import match_schema_errors


def bakery(schema_name):
    @Directive(name="switchValue", schema_name=schema_name)
    class SwitchValue:
        async def on_post_input_coercion(
            self,
            directive_args: Dict[str, Any],
            next_directive: Callable,
            parent_node,
            value: Any,
            ctx: Optional[Any],
        ):
            value = await next_directive(parent_node, value, ctx)
            value.update(directive_args["newValue"])
            return value

    @Resolver("Query.test1", schema_name=schema_name)
    async def resolver_input_object_test_1(_pr, arguments, *_args, **_kwargs):
        return str(arguments)


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    input anInput {
        a: String
        b: Float
    }

    type Query {
        test1(aParameter: anInput): String
    }

    input switchValuInput {
        c: Int
    }

    input anotherInput {
        g: Int
    }

    directive @switchValue(newValue: switchValuInput) on INPUT_OBJECT

    extend input anInput @switchValue(newValue: {c: 5}) {
        c: Int
    }

    extend input anotherInput @switchValue(newValue: switchValuInput)
    """,
    bakery=bakery,
)
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
        query {
            __type(name: "anInput") {
            name
            kind
            inputFields {
                name
            }
        } }
        """,
            {
                "data": {
                    "__type": {
                        "name": "anInput",
                        "kind": "INPUT_OBJECT",
                        "inputFields": [
                            {"name": "a"},
                            {"name": "b"},
                            {"name": "c"},
                        ],
                    }
                }
            },
        ),
        (
            """
            query {
                test1(aParameter: {a:"R", b:6.25, c:9})
            }
            """,
            {
                "data": {
                    "test1": "{'aParameter': {'a': 'R', 'b': 6.25, 'c': 5}}"
                }
            },
        ),
    ],
)
async def test_issue_278_input_object_extend(schema_stack, query, expected):
    assert await schema_stack.execute(query) == expected


@pytest.mark.asyncio
async def test_issue_278_extend_input_object_invalid_sdl():
    with pytest.raises(GraphQLSchemaError) as excinfo:
        await create_schema(
            """
                directive @C on INPUT_OBJECT

                input bob @C {
                    a: String
                    b: Int
                }

                extend input bob @C {
                    a: String
                    b: Int
                }

                type aType {
                    b: bob
                }

                type Query {
                    a: bob
                }

                extend input dontexists @C

                extend input aType {
                    d: Float
                }
            """,
            name="test_issue_278_extend_input_object_invalid_sdl",
        )

    match_schema_errors(
        excinfo.value,
        [
            "Field < bob.a > can only be defined once.",
            "Field < bob.b > can only be defined once.",
            "The directive < @C > can only be used once at this location.",
            "The type of < aType.b > must be Output type but got: bob.",
            "The type of < Query.a > must be Output type but got: bob.",
            "Cannot extend type < dontexists > because it is not defined.",
            "Cannot extend non-object type < aType >.",
        ],
    )
