import asyncio

from typing import Any, Callable, Dict, List, Optional

from tartiflette.executors.types import ExecutionContext


async def _execute(
    root_resolvers: List["NodeField"],
    execution_ctx: ExecutionContext,
    request_ctx: Optional[Dict[str, Any]],
) -> None:
    await asyncio.gather(
        *[resolver(execution_ctx, request_ctx) for resolver in root_resolvers],
        return_exceptions=False,
    )


def _get_datas(root_nodes: List["NodeField"]) -> Optional[dict]:
    # TODO: understand what is it for
    data = {}
    for node in root_nodes:
        if node.cant_be_null and node.marshalled is None:
            return None
        data[node.alias] = node.marshalled
    return data


async def execute(
    root_nodes: List["NodeField"],
    request_ctx: Optional[Dict[str, Any]],
    error_coercer: Callable[[Exception], dict],
) -> dict:
    execution_ctx = ExecutionContext()

    await _execute(root_nodes, execution_ctx, request_ctx)

    results = {
        "data": _get_datas(root_nodes),
        "errors": [error_coercer(err) for err in execution_ctx.errors if err],
    }

    if not results["errors"]:
        del results["errors"]

    return results
