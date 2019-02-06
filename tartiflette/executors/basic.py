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
    initial_value: Optional[Any],
    allow_parallelization: bool,
) -> None:
    if not allow_parallelization:
        for resolver in root_resolvers:
            await resolver(
                execution_ctx, request_ctx, parent_result=initial_value
            )
    else:
        await asyncio.gather(
            *[
                resolver(
                    execution_ctx, request_ctx, parent_result=initial_value
                )
                for resolver in root_resolvers
            ],
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
    operations: Dict[Optional[str], List["NodeOperationDefinition"]],
    operation_name: Optional[str],
    request_ctx: Optional[Dict[str, Any]],
    initial_value: Optional[Any],
    error_coercer: Callable[[Exception], dict],
) -> dict:
    execution_ctx = ExecutionContext()

    try:
        operation = operations[operation_name]
    except KeyError:
        if operation_name or len(operations) != 1:
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

        operation = operations[list(operations.keys())[0]]

    root_nodes = operation.children

    await _execute(
        root_nodes,
        execution_ctx,
        request_ctx,
        initial_value=initial_value,
        allow_parallelization=operation.allow_parallelization,
    )

    results = {
        "data": _get_datas(root_nodes),
        "errors": [error_coercer(err) for err in execution_ctx.errors if err],
    }

    if not results["errors"]:
        del results["errors"]

    return results
