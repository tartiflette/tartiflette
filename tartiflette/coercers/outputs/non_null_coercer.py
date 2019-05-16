from typing import Any, Callable, List

__all__ = ("non_null_coercer",)


async def non_null_coercer(
    result: Any,
    info: "ResolveInfo",
    execution_context: "ExecutionContext",
    field_nodes: List["FieldNode"],
    path: "Path",
    inner_coercer: Callable,
) -> Any:
    """
    Checks if the result is None and will raise an error if its the case or
    will returns the coerced result.
    :param result: resolved value
    :param info: information related to the execution and the resolved field
    :param execution_context: instance of the query execution context
    :param field_nodes: AST nodes related to the resolved field
    :param path: the path traveled until this resolver
    :param inner_coercer: the pre-computed coercer to use on the result
    :type result: Any
    :type info: ResolveInfo
    :type execution_context: ExecutionContext
    :type field_nodes: List[FieldNode]
    :type path: Path
    :type inner_coercer: Callable
    :return: the computed value
    :rtype: Any
    """
    coerced_output = await inner_coercer(
        result, info, execution_context, field_nodes, path
    )
    if coerced_output is None:
        raise ValueError(
            "Cannot return null for non-nullable field "
            f"{info.parent_type.name}.{info.field_name}."
        )
    return coerced_output
