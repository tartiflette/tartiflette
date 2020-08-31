from typing import Any, Callable, Dict, Optional

import pytest

from tartiflette import Directive, Resolver, create_schema
from tartiflette.types.exceptions.tartiflette import GraphQLSchemaError
from tests.functional.utils import match_schema_errors


def bakery(schema_name):
    @Directive(name="addValue", schema_name=schema_name)
    class AddValue:
        @staticmethod
        async def on_pre_output_coercion(
            directive_args: Dict[str, Any],
            next_directive: Callable,
            output_definition_node,
            value: Any,
            ctx: Optional[Any],
            info: "ResolveInfo",
        ):
            return (
                await next_directive(output_definition_node, value, ctx, info)
                + directive_args["value"]
            )

    @Resolver("Query.test1", schema_name=schema_name)
    async def resolver_test_1(*_args, **_kwargs):
        return 7


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    type Query {
        test1: Int
    }

    directive @addValue(value: Int) on SCALAR

    extend scalar Int @addValue(value: 5)
    """,
    bakery=bakery,
)
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query {
                test1
            }
            """,
            {"data": {"test1": 12}},
        )
    ],
)
async def test_issue_278_scalar_extend(schema_stack, query, expected):
    assert await schema_stack.execute(query) == expected


@pytest.mark.asyncio
async def test_issue_278_scalar_extend_invalid_sdl():
    with pytest.raises(GraphQLSchemaError) as excinfo:
        await create_schema(
            """
                directive @C on OBJECT | SCALAR

                scalar bob @C

                extend scalar bob @C

                type Query {
                    a: bob
                }

                extend scalar dontexists @C

                extend scalar Query @C
            """,
            name="test_issue_278_scalar_extend_invalid_sdl",
        )

    match_schema_errors(
        excinfo.value,
        [
            "The directive < @C > can only be used once at this location.",
            "Cannot extend type < dontexists > because it is not defined.",
            "Cannot extend non-object type < Query >.",
        ],
    )
