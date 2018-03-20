import asyncio


async def _level_execute(resolvers, request_ctx):
    corroutines = [
        resolver(request_ctx) for resolver in resolvers \
        if not resolver.type_condition or (resolver.type_condition and \
        resolver.parent and resolver.type_condition == \
        resolver.parent.results.__class__.__name__)
        # TODO base __class__.__name__ on idl parsing result
    ]

    return await asyncio.gather(*corroutines, return_exceptions=True)


async def execute(gql_nodes, request_ctx):
    results = {}
    for nodes in gql_nodes:
        await _level_execute(nodes, request_ctx)

    for node in gql_nodes[0]:
        results[node.name] = node.as_jsonable

    return results
