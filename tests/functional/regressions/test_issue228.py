import pytest

from tartiflette import Directive, Resolver, create_engine


@pytest.mark.asyncio
async def test_issue228_1():
    @Resolver("Query.a", schema_name="issue228_1")
    async def lol(*_args, **_kwargs):
        return {"ninja": "Ohio"}

    _engine = await create_engine(
        sdl="""

            type Query {
                a: Lol
            }""",
        modules=[
            {
                "name": "tests.functional.regressions.issue228.a_module",
                "config": {"val": "Blah!!"},
            }
        ],
        schema_name="issue228_1",
    )

    assert await _engine.execute("query aquery { a { ninja } }") == {
        "data": {"a": {"ninja": "Ohio Ninja Blah!!GO !"}}
    }


@pytest.mark.asyncio
async def test_issue228_2():
    @Resolver("Query.a", schema_name="issue228_2")
    async def lol(*_args, **_kwargs):
        return {"ninja": "Ohio"}

    _engine = await create_engine(
        sdl="""

            type Query {
                a: Lol
            }""",
        modules=[
            {
                "name": "tests.functional.regressions.issue228.b_module",
                "config": {"val": "Blah!!"},
            }
        ],
        schema_name="issue228_2",
    )

    assert await _engine.execute("query aquery { a { ninja } }") == {
        "data": {"a": {"ninja": "Ohio NinjaB BBlah!!GO !B"}}
    }


@pytest.mark.asyncio
async def test_issue228_3():
    from tartiflette.types.exceptions.tartiflette import GraphQLSchemaError

    sdl = """

    directive @tartifyMe on FIELD_DEFINITION
    """

    @Directive("tartifyMe", schema_name="issue223_3")
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
        def on_argument_execution(*_, **_kwargs):
            pass

        @staticmethod
        def on_introspection(*_, **_kwargs):
            pass

    with pytest.raises(
        GraphQLSchemaError,
        match="""

0: Missing Query Type < Query >.
1: Directive tartifyMe Method on_pre_output_coercion is not awaitable
2: Directive tartifyMe Method on_introspection is not awaitable
3: Directive tartifyMe Method on_post_input_coercion is not awaitable
4: Directive tartifyMe Method on_argument_execution is not awaitable
5: Directive tartifyMe Method on_field_execution is not awaitable""",
    ):
        await create_engine(sdl=sdl, schema_name="issue223_3")
