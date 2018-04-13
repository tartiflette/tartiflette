import asyncio


async def _level_execute(resolvers, request_ctx):
    coroutines = [
        resolver(request_ctx) for resolver in resolvers \
        if not resolver.type_condition or (resolver.type_condition and \
        resolver.parent and resolver.type_condition == \
        resolver.parent.results.__class__.__name__)
        # TODO base __class__.__name__ on sdl parsing result
    ]

    return await asyncio.gather(*coroutines, return_exceptions=True)


async def execute(gql_nodes, request_ctx):
    results = {
        "data": {},
        "errors": [],
    }
    for nodes in gql_nodes:
        await _level_execute(nodes, request_ctx)
        # TODO: There is probably a better way than to iterate after each level
        # Flatten errors from each levels
        for node in nodes:
            if node.errors:
                results["errors"] += node.errors

    for node in gql_nodes[0]:
        results["data"][node.name] = node.as_jsonable

    if len(results["errors"]) == 0:
        del results["errors"]

    return results
