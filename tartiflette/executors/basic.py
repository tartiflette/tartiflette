import asyncio

from tartiflette.executors.helpers import visualize_gql_tree_and_data
from tartiflette.executors.types import ExecutionContext


async def _level_execute(resolvers, exec_ctx, request_ctx):
    coroutines = [
        resolver(exec_ctx, request_ctx)
        for resolver in resolvers
        if not resolver.type_condition
        or (
            resolver.type_condition
            and resolver.parent
            and resolver.type_condition
            == resolver.parent.results.__class__.__name__
        )
        # TODO base __class__.__name__ on sdl parsing result
    ]

    return await asyncio.gather(*coroutines, return_exceptions=True)


# def _level_coerce(gql_nodes):
#     for node in gql_nodes:
#         node.coerce_result()


async def execute(gql_nodes, request_ctx):
    results = {"data": {}, "errors": []}
    exec_ctx = ExecutionContext()
    # TODO: We do this in two steps, it could be merged into one for better
    # performance
    for level, nodes in enumerate(gql_nodes):
        await _level_execute(nodes, exec_ctx, request_ctx)
        visualize_gql_tree_and_data(gql_nodes, level)
        visualize_gql_tree_and_data(gql_nodes, level, value='as_jsonable')

    # Coerce results
    # for level, node in enumerate(gql_nodes[0]):
    #     node.as_jsonable = node.coerce_result()
    #     visualize_gql_tree_and_data(gql_nodes, level, value='coerced')
    #     visualize_gql_tree_and_data(gql_nodes, level, value='as_jsonable')

    results["errors"] += [err.coerce_value() for err in exec_ctx.errors if err]

    for node in gql_nodes[0]:
        results["data"][node.name] = node.as_jsonable

    if not results["errors"]:
        del results["errors"]

    return results
