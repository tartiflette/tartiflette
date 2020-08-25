from tartiflette import Resolver


def bake(schema_name, config):
    @Resolver("A.c", schema_name=schema_name)
    async def resolver_a_c(*args, **kwargs):
        return "A.c"
