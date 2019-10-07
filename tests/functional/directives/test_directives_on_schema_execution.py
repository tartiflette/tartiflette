import pytest

from tartiflette import Directive, Resolver, create_engine

_SDL = """
directive @a_directive(t: String) on SCHEMA

type Query {
    a: String
}

schema @a_directive(t: "Loll") {
    query: Query
}
"""

_SDL_EXTEND = """
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
        initial_value = {"Modified by the directive": directive_args}

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
            {"AddedByTheDirective": "OhYeah"}
        )

        return results


async def resolve_a(parent_result, _args, _ctx, _info):
    return str(parent_result)


@pytest.fixture(scope="module", name="engine")
async def ttftt_engine():
    Directive(
        name="a_directive", schema_name="test_directive_on_schema_execute"
    )(ADirective)
    Resolver("Query.a", schema_name="test_directive_on_schema_execute")(
        resolve_a
    )
    return await create_engine(
        sdl=_SDL, schema_name="test_directive_on_schema_execute"
    )


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


@pytest.mark.asyncio
async def test_directive_on_schema_execute(engine):
    result = await engine.execute(
        """
        query {
            a
        }
        """,
        operation_name="",
    )

    assert {
        "data": {"a": "{'Modified by the directive': {'t': 'Loll'}}"},
        "extensions": {"AddedByTheDirective": "OhYeah"},
    } == result


@pytest.fixture(scope="module", name="engine_extended")
async def ttftt_engine_extended():
    Directive(
        name="a_directive",
        schema_name="test_directive_on_schema_execute_extended",
    )(ADirective)
    Directive(
        name="b_directive",
        schema_name="test_directive_on_schema_execute_extended",
    )(BDirective)
    Resolver(
        "Query.a", schema_name="test_directive_on_schema_execute_extended"
    )(resolve_a)
    return await create_engine(
        sdl=_SDL + _SDL_EXTEND,
        schema_name="test_directive_on_schema_execute_extended",
    )


@pytest.mark.asyncio
async def test_directive_on_schema_execute_extended(engine_extended):
    result = await engine_extended.execute(
        """
        query {
            a
        }
        """,
        operation_name="",
    )

    assert {
        "data": {
            "a": "{'Modified by the directive': {'t': 'Loll'}, 's': 'extended'}"
        },
        "extensions": {
            "AddedByBBBBBBBTheDirective": "OhYeah",
            "AddedByTheDirective": "OhYeah",
        },
    } == result
