import asyncio

from typing import Any, Callable, Dict, List, Optional

from tartiflette.executors.types import ExecutionContext
from tartiflette.types.exceptions.tartiflette import (
    UnknownAnonymousdOperation,
    UnknownNamedOperation,
)


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
    root_nodes: Dict[str, List["NodeField"]],
    operation_name: Optional[str],
    request_ctx: Optional[Dict[str, Any]],
    error_coercer: Callable[[Exception], dict],
) -> dict:
    execution_ctx = ExecutionContext()

    try:
        root_resolvers = root_nodes[operation_name]
    except KeyError:
        if operation_name or len(root_nodes) != 1:
            error = (
                UnknownNamedOperation(
                    "Unknown operation named < %s >." % operation_name
                )
                if operation_name is not None
                else UnknownAnonymousdOperation(
                    "Must provide operation name if query contains multiple operations."
                )
            )
            return {"data": None, "errors": [error_coercer(error)]}

        root_resolvers = root_nodes[list(root_nodes.keys())[0]]

    await _execute(root_resolvers, execution_ctx, request_ctx)

    results = {
        "data": _get_datas(root_resolvers),
        "errors": [error_coercer(err) for err in execution_ctx.errors if err],
    }

    if not results["errors"]:
        del results["errors"]

    return results
