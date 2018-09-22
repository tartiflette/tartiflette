import pytest

from tartiflette import Resolver
from tartiflette.directive import Directive
from tartiflette.engine import Engine


@pytest.mark.asyncio
async def test_tartiflette_deprecated_directive():
    schema = """
    type Query {
        fieldNormal: Int
        fieldDeprecatedDefault: Int @deprecated
        fieldDeprecatedCustom: Int @deprecated(reason: "Unused anymore")
    }
    """
    ttftt = Engine(schema)

    @Resolver("Query.fieldNormal", schema=ttftt.schema)
    async def func_field_resolver4(parent, arguments, request_ctx, info):
        return 42

    @Resolver("Query.fieldDeprecatedDefault", schema=ttftt.schema)
    async def func_field_resolver5(parent, arguments, request_ctx, info):
        return 42

    @Resolver("Query.fieldDeprecatedCustom", schema=ttftt.schema)
    async def func_field_resolver6(parent, arguments, request_ctx, info):
        return 42

    assert ttftt.schema.directives["deprecated"] is not None
    assert ttftt.schema.directives["deprecated"].implementation is not None

    result = await ttftt.execute(
        """
    query Test{
        fieldNormal
        fieldDeprecatedDefault
        fieldDeprecatedCustom
    }
    """
    )

    assert {
        "data": {
            "fieldNormal": 42,
            "fieldDeprecatedDefault": 42,
            "fieldDeprecatedCustom": 42,
        }
    } == result


@pytest.mark.asyncio
async def test_tartiflette_directive_declaration():
    schema_sdl = """
    directive @lol on FIELD_DEFINITION
    directive @lol2 on FIELD_DEFINITION

    type Query {
        fieldLoled1: Int @lol
        fieldLoled2: Int @lol @deprecated
        fieldLoled3: Int @deprecated @lol @lol2
    }
    """
    # Execute directive

    ttftt = Engine(schema_sdl)

    @Directive("lol2", schema=ttftt.schema)
    class Loled:
        @staticmethod
        def on_build(schema):
            pass

        @staticmethod
        async def on_execution(func, pr, args, rctx, info):
            return (await func(pr, args, rctx, info)) + 1

        @staticmethod
        async def on_introspection(func, pr, args, rctx, info):
            pass

    @Resolver("Query.fieldLoled1", schema=ttftt.schema)
    async def func_field_resolver4(parent, arguments, request_ctx, info):
        return 42

    @Resolver("Query.fieldLoled2", schema=ttftt.schema)
    async def func_field_resolver5(parent, arguments, request_ctx, info):
        return 42

    @Resolver("Query.fieldLoled3", schema=ttftt.schema)
    async def func_field_resolver6(parent, arguments, request_ctx, info):
        return 42

    @Directive("lol", schema=ttftt.schema)
    class Loled:
        @staticmethod
        def on_build(schema):
            pass

        @staticmethod
        async def on_execution(func, pr, args, rctx, info):
            return (await func(pr, args, rctx, info)) + 1

        @staticmethod
        async def on_introspection(func, pr, args, rctx, info):
            pass

    assert ttftt.schema.directives["lol"] is not None
    assert ttftt.schema.directives["lol"].implementation is not None

    result = await ttftt.execute(
        """
    query Test{
        fieldLoled1
        fieldLoled2
        fieldLoled3
    }
    """
    )

    assert {
        "data": {"fieldLoled1": 43, "fieldLoled2": 43, "fieldLoled3": 44}
    } == result
