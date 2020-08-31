from typing import Any, Callable, Dict, List

from tartiflette.execution.collect import collect_subfields
from tartiflette.execution.execute import execute_fields
from tartiflette.utils.errors import located_error

__all__ = ("complete_value_catching_error", "complete_object_value")


def handle_field_error(
    raw_error: Exception,
    field_nodes: List["FieldNode"],
    path: "Path",
    return_type: "GraphQLOutputType",
    execution_context: "ExecutionContext",
) -> None:
    """
    Computes the raw error to a TartifletteError and add it to the execution
    context or bubble up the error if the field can't be null.
    :param raw_error: the raw exception to be treated
    :param field_nodes: AST nodes related to the resolved field
    :param path: the path traveled until this field
    :param return_type: GraphQLOutputType instance of the resolved field
    :param execution_context: instance of the query execution context
    :type raw_error: Exception
    :type field_nodes: List[FieldNode]
    :type path: Path
    :type return_type: GraphQLOutputType
    :type execution_context: ExecutionContext
    """
    error = located_error(raw_error, field_nodes, path.as_list())

    # If the field type is non-nullable, then it is resolved without any
    # protection from errors, however it still properly locates the error.
    if return_type.is_non_null_type:
        raise error

    # Otherwise, error protection is applied, logging the error and resolving
    # a null value for this field if one is encountered.
    execution_context.add_error(error)


async def complete_value_catching_error(
    result: Any,
    info: "ResolveInfo",
    execution_context: "ExecutionContext",
    field_nodes: List["FieldNode"],
    path: "Path",
    return_type: "GraphQLOutputType",
    output_coercer: Callable,
) -> Any:
    """
    Coerce the resolved field value or catch the resolver exception to add it
    to the execution context.
    :param result: resolved field value
    :param info: information related to the execution and the resolved field
    :param execution_context: instance of the query execution context
    :param field_nodes: AST nodes related to the resolved field
    :param path: the path traveled until this resolver
    :param return_type: GraphQLOutputType instance of the resolved field
    :param output_coercer: pre-computed callable to coerce the result value
    :type result: Any
    :type info: ResolveInfo
    :type execution_context: ExecutionContext
    :type field_nodes: List[FieldNode]
    :type path: Path
    :type return_type: GraphQLOutputType
    :type output_coercer: Callable
    :return: the coerced resolved field value
    :rtype: Any
    """
    try:
        if isinstance(result, Exception):
            raise result

        return await output_coercer(
            result, info, execution_context, field_nodes, path
        )
    except Exception as raw_exception:  # pylint: disable=broad-except
        return handle_field_error(
            raw_exception, field_nodes, path, return_type, execution_context
        )


async def complete_object_value(
    result: Any,
    info: "ResolveInfo",
    execution_context: "ExecutionContext",
    field_nodes: List["FieldNode"],
    path: "Path",
    return_type: "GraphQLOutputType",
) -> Dict[str, Any]:
    """
    Complete an Object value by executing all sub-selections.
    :param result: result to treat
    :param info: information related to the execution and the resolved field
    :param execution_context: instance of the query execution context
    :param field_nodes: AST nodes related to the coerced field
    :param path: the path traveled until this coercer
    :param return_type: the GraphQLObjectType instance of the object
    :type result: Any
    :type info: ResolveInfo
    :type execution_context: ExecutionContext
    :type field_nodes: List[FieldNode]
    :type path: Path
    :type return_type: GraphQLOutputType
    :return: the computed value
    :rtype: Dict[str, Any]
    """
    return await execute_fields(
        execution_context,
        return_type,
        result,
        path,
        await collect_subfields(execution_context, return_type, field_nodes),
        info.is_introspection,
    )
