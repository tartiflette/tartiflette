import pytest

from tartiflette import Resolver
from tartiflette.directive import Directive
from tartiflette.executors.types import Info
from tartiflette.schema import GraphQLSchema
from tartiflette.tartiflette import Tartiflette
from tartiflette.types.field import GraphQLField


@pytest.mark.asyncio
async def test_tartiflette_directive_declaration():
    schema_sdl = """
    directive @deprecated(
        reason: String = "No longer supported"
    ) on FIELD_DEFINITION | ENUM_VALUE
    
    type Query {
        fieldNormal: Int
        fieldDeprecatedDefault: Int @deprecated
        fieldDeprecatedCustom: Int @deprecated(reason: "Unused anymore")
    }
    """
    # Execute directive

    ttftt = Tartiflette(schema_sdl)

    @Resolver("Query.fieldNormal", schema=ttftt.schema)
    async def func_field_resolver(parent, arguments, request_ctx, info):
        return 42

    @Resolver("Query.fieldDeprecatedDefault", schema=ttftt.schema)
    async def func_field_resolver(parent, arguments, request_ctx, info):
        return 42

    @Resolver("Query.fieldDeprecatedCustom", schema=ttftt.schema)
    async def func_field_resolver(parent, arguments, request_ctx, info):
        return 42

    @Directive("deprecated", schema=ttftt.schema)
    class Deprecated:
        @staticmethod
        def on_build(schema: GraphQLSchema):
            for name, type in schema.types.items():
                try:
                    type.isDeprecated = False
                    type.deprecationReason = ""
                except AttributeError:
                    pass

            async def is_deprecated_resolver(parent, arguments, context, info: Info):
                try:
                    return info.schema_field.isDeprecated
                except AttributeError:
                    return None

            async def deprecation_reason_resolver(parent, arguments, context, info: Info):
                try:
                    return info.schema_field.deprecationReason
                except AttributeError:
                    return None

            schema.types["__Field"].fields["isDeprecated"] = GraphQLField(
                name="isDeprecated",
                gql_type=schema.types["Boolean"],
                arguments={},
                description="Description",
                resolver=is_deprecated_resolver,
            )
            schema.types["__Field"].fields["deprecationReason"] = GraphQLField(
                name="deprecationReason",
                gql_type=schema.types["String"],
                arguments={},
                description="Description",
                resolver=deprecation_reason_resolver,
            )

        @staticmethod
        async def on_execute(resolver, parent, arguments, request_ctx, info):
            # Directives should be able to:
            # - change result (post-process) = CHECK.
            # - change parent value (pre-process ? = CHECK.
            # - remove field from result (pre-execution filter ?) => None + no error ?
            # - add field to result (pre-execution filter ?) => Return value ?
            # - it can do all this on the default resolver too !
            # to modify the introspection, it should modify the introspection types & resolvers.
            return await resolver(parent, arguments, request_ctx, info)

    ttftt.schema.bake()
    assert len(ttftt.schema.directives) == 1
    assert ttftt.schema.directives["deprecated"] is not None
    assert ttftt.schema.directives["deprecated"].implementation is not None

    result = await ttftt.execute("""
    query Test{
        __type(name: "Query") {
            fields {
                name
                isDeprecated
                deprecationReason
            }
        }
    }
    """)

    assert {"data": {"__type": {
        "fields": [
            {"name": "fieldNormal",
             "isDeprecated": False,
             "deprecationReason": "No longer supported"},
            {"name": "fieldDeprecatedDefault",
             "isDeprecated": True,
             "deprecationReason": "No longer supported"},
            {"name": "fieldDeprecatedCustom",
             "isDeprecated": True,
             "deprecationReason": "Unused anymore"}
        ],
    }}} == result
