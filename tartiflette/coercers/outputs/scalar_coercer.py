from typing import Any, List

from tartiflette.coercers.outputs.null_coercer import null_coercer_wrapper
from tartiflette.utils.values import is_invalid_value

__all__ = ("scalar_coercer",)


@null_coercer_wrapper
async def scalar_coercer(
    result: Any,
    info: "ResolveInfo",
    execution_context: "ExecutionContext",
    field_nodes: List["FieldNode"],
    path: "Path",
    scalar_type: "GraphQLScalar",
) -> Any:
    """
    Computes the value of a scalar type.
    :param result: resolved value
    :param info: information related to the execution and the resolved field
    :param execution_context: instance of the query execution context
    :param field_nodes: AST nodes related to the resolved field
    :param path: the path traveled until this resolver
    :param scalar_type: the GraphQLType instance of the scalar
    :type result: Any
    :type info: ResolveInfo
    :type execution_context: ExecutionContext
    :type field_nodes: List[FieldNode]
    :type path: Path
    :type scalar_type: GraphQLScalar
    :return: the computed value
    :rtype: Any
    """
    # pylint: disable=unused-argument
    coerced_result = scalar_type.coerce_output(result)
    if is_invalid_value(coerced_result):
        raise ValueError(
            f"Expected value of type {scalar_type} but received {type(result)}."
        )
    return coerced_result
