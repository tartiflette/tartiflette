import asyncio

from tartiflette.executors.types import ExecutionContext


async def _execute(root_resolvers, exec_ctx, request_ctx):
    coroutines = [
        resolver(exec_ctx, request_ctx) for resolver in root_resolvers
    ]
    return await asyncio.gather(*coroutines, return_exceptions=False)


def _get_datas(root_nodes):
    data = {}
    for node in root_nodes:
        if node.cant_be_null and node.marshalled is None:
            return None
        data[node.alias] = node.marshalled

    return data


async def execute(root_nodes, request_ctx):
    results = {"data": {}, "errors": []}
    exec_ctx = ExecutionContext()

    await _execute(root_nodes, exec_ctx, request_ctx)

    results["errors"] += [err.coerce_value() for err in exec_ctx.errors if err]
    results["data"] = _get_datas(root_nodes)

    if not results["errors"]:
        del results["errors"]

    return results
