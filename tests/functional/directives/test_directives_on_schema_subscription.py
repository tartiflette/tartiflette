import asyncio

import pytest

from tartiflette import Directive, Resolver, Subscription


def bakery(schema_name):
    @Directive(name="a_directive", schema_name=schema_name)
    class ADirective:
        @staticmethod
        async def on_schema_subscription(
            directive_args,
            next_directive,
            schema,
            document,
            parsing_errors,
            operation_name,
            context,
            variables,
            initial_value,
        ):
            async for payload in next_directive(
                schema,
                document,
                parsing_errors,
                operation_name,
                context,
                variables,
                int(directive_args["t"]),
            ):
                payload["extensions"] = {"AddedByTheDirective": "OhYeah"}
                yield payload

    @Resolver("Query.a", schema_name=schema_name)
    async def resolve_query_a(parent_result, _args, _ctx, _info):
        return str(parent_result)

    @Subscription("Subscription.timer", schema_name=schema_name)
    async def subscribe_timer(parent_result, *_, **__):
        for integer in range(0, 10):
            yield {"timer": integer + parent_result}
            await asyncio.sleep(0.01)


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    directive @a_directive(t: Int) on SCHEMA

    type Query {
        a: String
    }

    type Subscription {
        timer: Int!
    }

    schema @a_directive(t: 25) {
        query: Query
        subscription: Subscription
    }
    """,
    bakery=bakery,
)
async def test_directive_schema_on_subscription(schema_stack):
    i = 0
    async for result in schema_stack.subscribe(
        """
        subscription {
          timer
        }
        """
    ):
        assert result == {
            "data": {"timer": i + 25},
            "extensions": {"AddedByTheDirective": "OhYeah"},
        }
        i += 1

    assert i == 10
