from typing import Any, Callable, Dict, Optional

import pytest

from tartiflette import Directive, Resolver, create_engine


@pytest.mark.asyncio
async def test_tartiflette_deprecated_execution_directive(clean_registry):
    schema = """
    type Query {
        fieldNormal: Int
        fieldDeprecatedDefault: Int @deprecated
        fieldDeprecatedCustom: Int @deprecated(reason: "Unused anymore")
    }
    """

    @Resolver("Query.fieldNormal")
    async def func_field_resolver4(parent, arguments, request_ctx, info):
        return 42

    @Resolver("Query.fieldDeprecatedDefault")
    async def func_field_resolver5(parent, arguments, request_ctx, info):
        return 42

    @Resolver("Query.fieldDeprecatedCustom")
    async def func_field_resolver6(parent, arguments, request_ctx, info):
        return 42

    ttftt = await create_engine(schema)

    assert (
        clean_registry.find_schema().find_directive("deprecated") is not None
    )
    assert (
        clean_registry.find_schema()
        .find_directive("deprecated")
        .implementation
        is not None
    )

    result = await ttftt.execute(
        """
    query Test{
        fieldNormal
        fieldDeprecatedDefault
        fieldDeprecatedCustom
    }
    """,
        operation_name="Test",
    )

    assert {
        "data": {
            "fieldNormal": 42,
            "fieldDeprecatedDefault": 42,
            "fieldDeprecatedCustom": 42,
        }
    } == result


@pytest.mark.asyncio
async def test_tartiflette_deprecated_introspection_directive(clean_registry):
    schema = """
    type Query {
        fieldNormal: Int
        fieldDeprecatedDefault: Int @deprecated
        fieldDeprecatedCustom: Int @deprecated(reason: "Unused anymore")
    }
    """

    @Resolver("Query.fieldNormal")
    async def func_field_resolver4(parent, arguments, request_ctx, info):
        return 42

    @Resolver("Query.fieldDeprecatedDefault")
    async def func_field_resolver5(parent, arguments, request_ctx, info):
        return 42

    @Resolver("Query.fieldDeprecatedCustom")
    async def func_field_resolver6(parent, arguments, request_ctx, info):
        return 42

    ttftt = await create_engine(schema)

    assert (
        clean_registry.find_schema().find_directive("deprecated") is not None
    )
    assert (
        clean_registry.find_schema()
        .find_directive("deprecated")
        .implementation
        is not None
    )

    result = await ttftt.execute(
        """
    query Test{
        __type(name: "Query") {
            fields(includeDeprecated: true) {
                name
                isDeprecated
                deprecationReason
            }
        }
    }
    """,
        operation_name="Test",
    )

    assert {
        "data": {
            "__type": {
                "fields": [
                    {
                        "name": "fieldNormal",
                        "isDeprecated": False,
                        "deprecationReason": None,
                    },
                    {
                        "name": "fieldDeprecatedDefault",
                        "isDeprecated": True,
                        "deprecationReason": "No longer supported",
                    },
                    {
                        "name": "fieldDeprecatedCustom",
                        "isDeprecated": True,
                        "deprecationReason": "Unused anymore",
                    },
                ]
            }
        }
    } == result


@pytest.mark.asyncio
async def test_tartiflette_directive_declaration(clean_registry):
    schema_sdl = """
    directive @lol on FIELD_DEFINITION
    directive @lol2( value: Int ) on FIELD_DEFINITION

    type Query {
        fieldLoled1: Int @lol
        fieldLoled2: Int @lol @deprecated @lol2(value:2)
        fieldLoled3: Int @deprecated @lol @lol2(value:6)
    }
    """
    # Execute directive

    @Directive("lol2")
    class Loled2:
        @staticmethod
        async def on_field_execution(
            directive_args: Dict[str, Any],
            next_resolver: Callable,
            parent: Optional[Any],
            args: Dict[str, Any],
            ctx: Optional[Any],
            info: "ResolveInfo",
        ):
            return (await next_resolver(parent, args, ctx, info)) + int(
                directive_args["value"]
            )

    @Resolver("Query.fieldLoled1")
    async def func_field_resolver4(_parent, _arguments, _request_ctx, _info):
        return 42

    @Resolver("Query.fieldLoled2")
    async def func_field_resolver5(_parent, _arguments, _request_ctx, _info):
        return 42

    @Resolver("Query.fieldLoled3")
    async def func_field_resolver6(_parent, _arguments, _request_ctx, _info):
        return 42

    @Directive("lol")
    class Loled:
        @staticmethod
        async def on_field_execution(
            directive_args: Dict[str, Any],
            next_resolver: Callable,
            parent: Optional[Any],
            args: Dict[str, Any],
            ctx: Optional[Any],
            info: "ResolveInfo",
        ):
            return (await next_resolver(parent, args, ctx, info)) + 1

    ttftt = await create_engine(schema_sdl)

    assert clean_registry.find_schema().find_directive("lol") is not None
    assert (
        clean_registry.find_schema().find_directive("lol").implementation
        is not None
    )

    result = await ttftt.execute(
        """
    query Test{
        fieldLoled1
        fieldLoled2
        fieldLoled3
    }
    """,
        operation_name="Test",
    )

    assert {
        "data": {"fieldLoled1": 43, "fieldLoled2": 45, "fieldLoled3": 49}
    } == result


@pytest.mark.asyncio
async def test_tartiflette_non_introspectable_execution_directive(
    clean_registry
):
    schema = """
    type Query {
        fieldNormal: Int
        fieldHiddendToIntrospactable: Int @nonIntrospectable
    }
    """

    @Resolver("Query.fieldNormal")
    async def func_field_resolver4(parent, arguments, request_ctx, info):
        return 42

    @Resolver("Query.fieldHiddendToIntrospactable")
    async def func_field_resolver5(parent, arguments, request_ctx, info):
        return 42

    ttftt = await create_engine(schema)

    assert (
        clean_registry.find_schema().find_directive("nonIntrospectable")
        is not None
    )
    assert (
        clean_registry.find_schema()
        .find_directive("nonIntrospectable")
        .implementation
        is not None
    )

    result = await ttftt.execute(
        """
    query Test{
        __type(name: "Query") {
            fields {
                name
                isDeprecated
                deprecationReason
            }
        }
    }
    """,
        operation_name="Test",
    )

    assert {
        "data": {
            "__type": {
                "fields": [
                    {
                        "name": "fieldNormal",
                        "isDeprecated": False,
                        "deprecationReason": None,
                    }
                ]
            }
        }
    } == result
