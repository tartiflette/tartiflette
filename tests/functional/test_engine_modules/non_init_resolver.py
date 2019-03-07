from tartiflette import Resolver


@Resolver("A.c", schema_name="test_issue140")
async def resolver_a_c(*args, **kwargs):
    return "A.c"
