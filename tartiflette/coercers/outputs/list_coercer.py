from typing import Any, Callable, List

from tartiflette.coercers.common import Path
from tartiflette.coercers.outputs.null_coercer import null_coercer_wrapper
from tartiflette.resolver.factory import complete_value_catching_error
from tartiflette.utils.errors import extract_exceptions_from_results

__all__ = ("list_coercer",)


@null_coercer_wrapper
async def list_coercer(
    result: Any,
    info: "ResolveInfo",
    execution_context: "ExecutionContext",
    field_nodes: List["FieldNode"],
    path: "Path",
    item_type: "GraphQLOutputType",
    inner_coercer: Callable,
) -> List[Any]:
    """
    Computes the value of a list.
    :param result: resolved value
    :param info: information related to the execution and the resolved field
    :param execution_context: instance of the query execution context
    :param field_nodes: AST nodes related to the resolved field
    :param path: the path traveled until this resolver
    :param item_type: GraphQLType of list items
    :param inner_coercer: the pre-computed coercer to use on the result
    :type result: Any
    :type info: ResolveInfo
    :type execution_context: ExecutionContext
    :type field_nodes: List[FieldNode]
    :type path: Path
    :type item_type: GraphQLOutputType
    :type inner_coercer: Callable
    :return: the computed value
    :rtype: List[Any]
    """
    # pylint: disable=too-many-locals
    if not isinstance(result, list):
        raise TypeError(
            "Expected Iterable, but did not find one for field "
            f"{info.parent_type.name}.{info.field_name}."
        )

    results = []
    for index, item in enumerate(result):
        try:
            value = await complete_value_catching_error(
                item,
                info,
                execution_context,
                field_nodes,
                Path(path, index),
                item_type,
                inner_coercer,
            )
        except Exception as e:  # pylint: disable=broad-except
            value = e
        results.append(value)

    exceptions = extract_exceptions_from_results(results)
    if exceptions:
        raise exceptions

    return results
