import asyncio

import pytest

from tartiflette import Directive, Resolver, Subscription, create_engine

_SDL = """
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
"""


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
        initial_value = int(directive_args["t"])

        async for payload in next_directive(
            schema,
            document,
            parsing_errors,
            operation_name,
            context,
            variables,
            initial_value,
        ):
            payload["extensions"] = {"AddedByTheDirective": "OhYeah"}
            yield payload


async def resolve_a(parent_result, _args, _ctx, _info):
    return str(parent_result)


async def subscription_timer(parent_result, *_, **__):
    for integer in range(0, 10):
        yield {"timer": integer + parent_result}
        await asyncio.sleep(0.01)


@pytest.fixture(scope="module", name="engine")
async def ttftt_engine():
    Directive(
        name="a_directive", schema_name="test_directive_schema_on_subscription"
    )(ADirective)
    Resolver("Query.a", schema_name="test_directive_schema_on_subscription")(
        resolve_a
    )
    Subscription(
        "Subscription.timer",
        schema_name="test_directive_schema_on_subscription",
    )(subscription_timer)

    return await create_engine(
        sdl=_SDL, schema_name="test_directive_schema_on_subscription"
    )


@pytest.mark.asyncio
async def test_directive_schema_on_subscription(engine):
    i = 0
    async for result in engine.subscribe(
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
