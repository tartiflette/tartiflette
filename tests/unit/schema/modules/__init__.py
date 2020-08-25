from tartiflette import Resolver, Scalar
from tartiflette.scalar.builtins.string import ScalarString


async def bake(schema_name, config):
    Scalar("String", schema_name=schema_name)(ScalarString)

    @Resolver("Query.hello", schema_name=schema_name)
    async def resolve_query_hello(parent, args, ctx, info):
        return f"Hello {args['name']}!"
