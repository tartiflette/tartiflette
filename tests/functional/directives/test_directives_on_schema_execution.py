import pytest

from tartiflette import Directive, Resolver

SDL = """
directive @a_directive(t: String) on SCHEMA

type Query {
    a: String
}

schema @a_directive(t: "Loll") {
    query: Query
}
"""

SDL_EXTEND = """
directive @b_directive(s: String) on SCHEMA

extend schema @b_directive(s: "extended")
"""


class ADirective:
    @staticmethod
    async def on_schema_execution(
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
        results = await next_directive(
            schema,
            document,
            parsing_errors,
            operation_name,
            context,
            variables,
            {"Modified by the directive": directive_args},
        )
        results.setdefault("extensions", {}).update(
            {"AddedByTheDirective": "OhYeah"}
        )
        return results


class BDirective:
    @staticmethod
    async def on_schema_execution(
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
        initial_value.update(directive_args)
        results = await next_directive(
            schema,
            document,
            parsing_errors,
            operation_name,
            context,
            variables,
            initial_value,
        )
        results.setdefault("extensions", {}).update(
            {"AddedByBBBBBBBTheDirective": "OhYeah"}
        )
        return results


async def resolve_a(parent_result, _args, _ctx, _info):
    return str(parent_result)


def directive_on_schema_execute_bakery(schema_name):
    Directive(name="a_directive", schema_name=schema_name)(ADirective)
    Resolver("Query.a", schema_name=schema_name)(resolve_a)


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl=SDL, bakery=directive_on_schema_execute_bakery,
)
async def test_directive_on_schema_execute(schema_stack):
    assert (
        await schema_stack.execute(
            """
            query {
              a
            }
            """,
            operation_name="",
        )
        == {
            "data": {"a": "{'Modified by the directive': {'t': 'Loll'}}"},
            "extensions": {"AddedByTheDirective": "OhYeah"},
        }
    )


def directive_on_schema_execute_extended_bakery(schema_name):
    Directive(name="a_directive", schema_name=schema_name)(ADirective)
    Directive(name="b_directive", schema_name=schema_name)(BDirective)
    Resolver("Query.a", schema_name=schema_name)(resolve_a)


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl=SDL + SDL_EXTEND, bakery=directive_on_schema_execute_extended_bakery,
)
async def test_directive_on_schema_execute_extended(schema_stack):
    assert (
        await schema_stack.execute(
            """
            query {
              a
            }
            """,
            operation_name="",
        )
        == {
            "data": {
                "a": "{'Modified by the directive': {'t': 'Loll'}, 's': 'extended'}"
            },
            "extensions": {
                "AddedByBBBBBBBTheDirective": "OhYeah",
                "AddedByTheDirective": "OhYeah",
            },
        }
    )
