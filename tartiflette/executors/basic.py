import asyncio

from typing import Any, AsyncIterable, Callable, Dict, List, Optional

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
    data = {}
    for node in root_nodes:
        if node.cant_be_null and node.marshalled is None:
            return None
        if not node.is_execution_stopped:
            data[node.alias] = node.marshalled

    return data or None


def get_operation(operations, operation_name):
    try:
        return operations[operation_name], None
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
            return None, [error]
        return operations[list(operations.keys())[0]], None


async def execute(
    operations: Dict[Optional[str], List["NodeOperationDefinition"]],
    operation_name: Optional[str],
    request_ctx: Optional[Dict[str, Any]],
    initial_value: Optional[Any],
    error_coercer: Callable[[Exception], dict],
) -> dict:
    # pylint: disable=too-many-locals
    execution_ctx = ExecutionContext()

    operation, errors = get_operation(operations, operation_name)

    if errors:
        return {"data": None, "errors": [error_coercer(err) for err in errors]}

    return await execute_fields(
        operation.children,
        execution_ctx,
        request_ctx,
        initial_value=initial_value,
        error_coercer=error_coercer,
        allow_parallelization=operation.allow_parallelization,
    )


async def subscribe(
    operations: Dict[Optional[str], List["NodeOperationDefinition"]],
    operation_name: Optional[str],
    request_ctx: Optional[Dict[str, Any]],
    initial_value: Optional[Any],
    error_coercer: Callable[[Exception], dict],
) -> AsyncIterable[Dict[str, Any]]:
    # pylint: disable=too-many-locals
    execution_ctx = ExecutionContext()

    operation, errors = get_operation(operations, operation_name)

    if errors:
        yield {"data": None, "errors": [error_coercer(err) for err in errors]}

    root_nodes = operation.children

    source_event_stream = await root_nodes[0].create_source_event_stream(
        execution_ctx, request_ctx, parent_result=initial_value
    )

    async for message in source_event_stream:
        yield await execute_fields(
            root_nodes,
            execution_ctx,
            request_ctx,
            initial_value=message,
            error_coercer=error_coercer,
            allow_parallelization=operation.allow_parallelization,
        )


async def execute_fields(
    fields,
    execution_ctx,
    request_ctx,
    initial_value,
    error_coercer,
    allow_parallelization=True,
):
    await _execute(
        fields,
        execution_ctx,
        request_ctx,
        initial_value=initial_value,
        allow_parallelization=allow_parallelization,
    )

    results = {
        "data": _get_datas(fields),
        "errors": [error_coercer(err) for err in execution_ctx.errors if err],
    }

    if not results["errors"]:
        del results["errors"]

    return results
