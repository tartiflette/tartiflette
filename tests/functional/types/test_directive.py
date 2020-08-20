from typing import Any, Callable, Dict, Optional

import pytest

from tartiflette import Directive, Resolver
from tartiflette.schema.registry import SchemaRegistry


def tartiflette_deprecated_execution_directive_bakery(schema_name):
    @Resolver("Query.fieldNormal", schema_name=schema_name)
    async def func_field_resolver4(parent, arguments, request_ctx, info):
        return 42

    @Resolver("Query.fieldDeprecatedDefault", schema_name=schema_name)
    async def func_field_resolver5(parent, arguments, request_ctx, info):
        return 42

    @Resolver("Query.fieldDeprecatedCustom", schema_name=schema_name)
    async def func_field_resolver6(parent, arguments, request_ctx, info):
        return 42


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    type Query {
        fieldNormal: Int
        fieldDeprecatedDefault: Int @deprecated
        fieldDeprecatedCustom: Int @deprecated(reason: "Unused anymore")
    }
    """,
    bakery=tartiflette_deprecated_execution_directive_bakery,
)
async def test_tartiflette_deprecated_execution_directive(schema_stack):
    assert (
        SchemaRegistry.find_schema(schema_stack.hash).find_directive(
            "deprecated"
        )
        is not None
    )
    assert (
        SchemaRegistry.find_schema(schema_stack.hash)
        .find_directive("deprecated")
        .implementation
        is not None
    )

    assert (
        await schema_stack.execute(
            """
            query Test{
                fieldNormal
                fieldDeprecatedDefault
                fieldDeprecatedCustom
            }
            """,
            operation_name="Test",
        )
        == {
            "data": {
                "fieldNormal": 42,
                "fieldDeprecatedDefault": 42,
                "fieldDeprecatedCustom": 42,
            }
        }
    )


def tartiflette_deprecated_introspection_directive_bakery(schema_name):
    @Resolver("Query.fieldNormal", schema_name=schema_name)
    async def func_field_resolver4(parent, arguments, request_ctx, info):
        return 42

    @Resolver("Query.fieldDeprecatedDefault", schema_name=schema_name)
    async def func_field_resolver5(parent, arguments, request_ctx, info):
        return 42

    @Resolver("Query.fieldDeprecatedCustom", schema_name=schema_name)
    async def func_field_resolver6(parent, arguments, request_ctx, info):
        return 42


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    type Query {
        fieldNormal: Int
        fieldDeprecatedDefault: Int @deprecated
        fieldDeprecatedCustom: Int @deprecated(reason: "Unused anymore")
    }
    """,
    bakery=tartiflette_deprecated_introspection_directive_bakery,
)
async def test_tartiflette_deprecated_introspection_directive(schema_stack):
    assert (
        SchemaRegistry.find_schema(schema_stack.hash).find_directive(
            "deprecated"
        )
        is not None
    )
    assert (
        SchemaRegistry.find_schema(schema_stack.hash)
        .find_directive("deprecated")
        .implementation
        is not None
    )

    assert (
        await schema_stack.execute(
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
        == {
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
        }
    )


def tartiflette_directive_declaration_bakery(schema_name):
    @Directive("lol2", schema_name=schema_name)
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

    @Resolver("Query.fieldLoled1", schema_name=schema_name)
    async def func_field_resolver4(_parent, _arguments, _request_ctx, _info):
        return 42

    @Resolver("Query.fieldLoled2", schema_name=schema_name)
    async def func_field_resolver5(_parent, _arguments, _request_ctx, _info):
        return 42

    @Resolver("Query.fieldLoled3", schema_name=schema_name)
    async def func_field_resolver6(_parent, _arguments, _request_ctx, _info):
        return 42

    @Directive("lol", schema_name=schema_name)
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


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    directive @lol on FIELD_DEFINITION
    directive @lol2( value: Int ) on FIELD_DEFINITION

    type Query {
        fieldLoled1: Int @lol
        fieldLoled2: Int @lol @deprecated @lol2(value:2)
        fieldLoled3: Int @deprecated @lol @lol2(value:6)
    }
    """,
    bakery=tartiflette_directive_declaration_bakery,
)
async def test_tartiflette_directive_declaration(schema_stack):
    assert (
        SchemaRegistry.find_schema(schema_stack.hash).find_directive("lol")
        is not None
    )
    assert (
        SchemaRegistry.find_schema(schema_stack.hash)
        .find_directive("lol")
        .implementation
        is not None
    )

    assert (
        await schema_stack.execute(
            """
            query Test{
                fieldLoled1
                fieldLoled2
                fieldLoled3
            }
            """,
            operation_name="Test",
        )
        == {"data": {"fieldLoled1": 43, "fieldLoled2": 45, "fieldLoled3": 49}}
    )


def tartiflette_non_introspectable_execution_directive_bakery(schema_name):
    @Resolver("Query.fieldNormal", schema_name=schema_name)
    async def func_field_resolver4(parent, arguments, request_ctx, info):
        return 42

    @Resolver("Query.fieldHiddendToIntrospactable", schema_name=schema_name)
    async def func_field_resolver5(parent, arguments, request_ctx, info):
        return 42


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    type Query {
        fieldNormal: Int
        fieldHiddendToIntrospactable: Int @nonIntrospectable
    }
    """,
    bakery=tartiflette_non_introspectable_execution_directive_bakery,
)
async def test_tartiflette_non_introspectable_execution_directive(
    schema_stack,
):
    assert (
        SchemaRegistry.find_schema(schema_stack.hash).find_directive(
            "nonIntrospectable"
        )
        is not None
    )
    assert (
        SchemaRegistry.find_schema(schema_stack.hash)
        .find_directive("nonIntrospectable")
        .implementation
        is not None
    )

    assert (
        await schema_stack.execute(
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
        == {
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
        }
    )
