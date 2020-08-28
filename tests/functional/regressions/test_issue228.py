import pytest

from tartiflette import (
    Directive,
    Resolver,
    create_schema,
    create_schema_with_operators,
)
from tartiflette.types.exceptions.tartiflette import GraphQLSchemaError
from tests.functional.utils import match_schema_errors


@pytest.mark.asyncio
async def test_issue228_1():
    @Resolver("Query.a", schema_name="issue228_1")
    async def lol(*_args, **_kwargs):
        return {"ninja": "Ohio"}

    _, execute, __ = await create_schema_with_operators(
        sdl="""
        type Query {
            a: Lol
        }
        """,
        modules=[
            {
                "name": "tests.functional.regressions.issue228.a_module",
                "config": {"val": "Blah!!"},
            }
        ],
        name="issue228_1",
    )

    assert await execute("query aquery { a { ninja } }") == {
        "data": {"a": {"ninja": "Ohio Ninja Blah!!GO !"}}
    }


@pytest.mark.asyncio
async def test_issue228_2():
    @Resolver("Query.a", schema_name="issue228_2")
    async def lol(*_args, **_kwargs):
        return {"ninja": "Ohio"}

    _, execute, __ = await create_schema_with_operators(
        sdl="""
        type Query {
            a: Lol
        }
        """,
        modules=[
            {
                "name": "tests.functional.regressions.issue228.b_module",
                "config": {"val": "Blah!!"},
            }
        ],
        name="issue228_2",
    )

    assert await execute("query aquery { a { ninja } }") == {
        "data": {"a": {"ninja": "Ohio NinjaB BBlah!!GO !B"}}
    }


@pytest.mark.asyncio
async def test_issue228_3():
    @Directive("tartifyMe", schema_name="issue228_3")
    class TartifyYourself:
        @staticmethod
        def on_pre_output_coercion(*_, **_kwargs):
            pass

        @staticmethod
        def on_post_input_coercion(*_, **_kwargs):
            pass

        @staticmethod
        def on_field_execution(*_, **_kwargs):
            pass

        @staticmethod
        def on_post_argument_coercion(*_, **_kwargs):
            pass

        @staticmethod
        def on_introspection(*_, **_kwargs):
            pass

        def on_schema_subscription(self, *_, **_kwargs):
            pass

        def on_schema_execution(self, *_, **_kwargs):
            pass

    with pytest.raises(GraphQLSchemaError) as excinfo:
        await create_schema(
            """
            directive @tartifyMe on FIELD_DEFINITION
            """,
            name="issue228_3",
        )

    match_schema_errors(excinfo.value, ["Query root type must be provided."])
