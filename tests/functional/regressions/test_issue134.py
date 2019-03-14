import pytest

from tartiflette import Engine, Resolver
from tartiflette.directive import CommonDirective, Directive

_SDL = """
directive @mySchemaDirective on SCHEMA

type Query {
  aField: String
}

schema @mySchemaDirective {
  query: Query
}
"""


@pytest.mark.asyncio
async def test_issue134():
    @Directive("mySchemaDirective", schema_name="test_issue134")
    class MySchemaDirective(CommonDirective):
        @staticmethod
        async def on_field_execution(
            directive_args, next_resolver, parent_result, args, ctx, info
        ):
            print("LOL")
            return await next_resolver(parent_result, args, ctx, info)

        @staticmethod
        def on_introspection(
            directive_args, next_directive, introspected_element, ctx, info
        ):
            print("LOL2")
            return next_directive(introspected_element, ctx, info)

    @Resolver("Query.aField", schema_name="test_issue134")
    async def myresolver(*_args, **_kwargs):
        return "Skiing is amazing"

    engine = Engine(_SDL, schema_name="test_issue134")

    print(await engine.execute("""query { aField }"""))
    print(await engine.execute("""query { __schema { types { name } } }"""))
