from typing import Any, Callable, List

__all__ = ("output_directives_coercer",)


async def output_directives_coercer(
    result: Any,
    info: "ResolveInfo",
    execution_context: "ExecutionContext",
    field_nodes: List["FieldNode"],
    path: "Path",
    coercer: Callable,
    directives: Callable,
) -> Any:
    """
    Executes the directives on the resolved value.
    :param result: resolved value
    :param info: information related to the execution and the resolved field
    :param execution_context: instance of the query execution context
    :param field_nodes: AST nodes related to the resolved field
    :param path: the path traveled until this resolver
    :param coercer: pre-computed coercer to use on the value
    :param directives: the directives to execute
    :type result: Any
    :type info: ResolveInfo
    :type execution_context: ExecutionContext
    :type field_nodes: List[FieldNode]
    :type path: Path
    :type coercer: Callable
    :type directives: Callable
    :return: the coerced result
    :rtype: Any
    """
    return await coercer(
        await directives(
            result,
            execution_context.context,
            info,
            context_coercer=execution_context.context,
        ),
        info,
        execution_context,
        field_nodes,
        path,
    )
