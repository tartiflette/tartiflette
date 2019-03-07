from tartiflette import Resolver


@Resolver("A.b", schema_name="test_issue140")
async def resolver_a_b(*args, **kwargs):
    return "A.b"
