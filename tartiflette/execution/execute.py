import asyncio

from typing import Any, AsyncIterable, Callable, Dict, List, Optional


def _get_executable_fields_data(
    operation_executable_fields: List["ExecutableFieldNode"]
) -> Optional[Dict[str, Any]]:
    data = {}
    for field in operation_executable_fields:
        if field.cant_be_null and field.marshalled is None:
            return None
        if not field.is_execution_stopped:
            data[field.alias] = field.marshalled

    return data or None


async def _execute_fields_serially(
    fields: List["ExecutableFieldNode"],
    execution_context: "ExecutionContext",
    initial_value: Optional[Any],
) -> None:
    for field in fields:
        await field(
            execution_context,
            execution_context.context,
            parent_result=initial_value,
        )


async def _execute_fields(
    fields: List["ExecutableFieldNode"],
    execution_context: "ExecutionContext",
    initial_value: Optional[Any],
) -> None:
    await asyncio.gather(
        *[
            field(
                execution_context,
                execution_context.context,
                parent_result=initial_value,
            )
            for field in fields
        ],
        return_exceptions=False,
    )


async def execute_operation(
    execution_context: "ExecutionContext", error_coercer: Callable
) -> Dict[str, Any]:
    from tartiflette.execution.collect import collect_executables
    from tartiflette.execution import build_response

    operation_type = execution_context.schema.find_type(
        execution_context.schema.get_operation_type(
            execution_context.operation.operation_type.capitalize()
        )
    )

    operation_executable_map_fields, errors = await collect_executables(
        execution_context,
        operation_type,
        execution_context.operation.selection_set,
    )

    if errors:
        return build_response(errors=errors, error_coercer=error_coercer)

    if not operation_executable_map_fields:
        return build_response(error_coercer=error_coercer)

    operation_executable_fields = list(
        operation_executable_map_fields[operation_type.name].values()
    )

    if execution_context.operation.operation_type == "mutation":
        await _execute_fields_serially(
            operation_executable_fields,
            execution_context,
            execution_context.root_value,
        )
    else:
        await _execute_fields(
            operation_executable_fields,
            execution_context,
            execution_context.root_value,
        )

    return build_response(
        data=_get_executable_fields_data(operation_executable_fields),
        errors=execution_context.errors,
        error_coercer=error_coercer,
    )


async def run_subscription(
    execution_context: "ExecutionContext", error_coercer: Callable
) -> AsyncIterable[Dict[str, Any]]:
    from tartiflette.execution.collect import collect_executables
    from tartiflette.execution import build_response

    operation_type = execution_context.schema.find_type(
        execution_context.schema.get_operation_type(
            execution_context.operation.operation_type.capitalize()
        )
    )

    operation_executable_map_fields, errors = await collect_executables(
        execution_context,
        operation_type,
        execution_context.operation.selection_set,
    )

    if errors:
        yield build_response(errors=errors, error_coercer=error_coercer)
        return

    if not operation_executable_map_fields:
        yield build_response(error_coercer=error_coercer)
        return

    operation_executable_fields = list(
        operation_executable_map_fields[operation_type.name].values()
    )

    source_event_stream = await operation_executable_fields[
        0
    ].create_source_event_stream(
        execution_context, execution_context.root_value
    )

    async for message in source_event_stream:
        await _execute_fields(
            operation_executable_fields, execution_context, message
        )
        yield build_response(
            data=_get_executable_fields_data(operation_executable_fields),
            errors=execution_context.errors,
            error_coercer=error_coercer,
        )
