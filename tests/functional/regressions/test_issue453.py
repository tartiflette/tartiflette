import pytest

from tartiflette import Directive, Resolver, create_engine

_SDL = """

directive @issue453Directive on SCHEMA

type Query {
    fieldA: Int
}

schema @issue453Directive {
    query: Query
}

"""


@pytest.mark.asyncio
async def test_issue453(random_schema_name):
    @Directive("issue453Directive", schema_name=random_schema_name)
    class AuthDirective:
        async def on_schema_execution(
            self,
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
            raise Exception("Error!")

    @Resolver("Query.fieldA", schema_name=random_schema_name)
    async def resolver_query_a(pr, args, ctx, info):
        return 1

    engine = await create_engine(_SDL, schema_name=random_schema_name)
    assert {
        "data": None,
        "errors": [{"locations": [], "message": "Error!", "path": ["Query"]}],
    } == await engine.execute("query { fieldA }")
