from typing import Any, List

from tartiflette.coercers.outputs.null_coercer import null_coercer_wrapper
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.utils.values import is_invalid_value

__all__ = ("enum_coercer",)


@null_coercer_wrapper
async def enum_coercer(
    result: Any,
    info: "ResolveInfo",
    execution_context: "ExecutionContext",
    field_nodes: List["FieldNode"],
    path: "Path",
    enum_type: "GraphQLEnumType",
) -> Any:
    """
    Computes the value of an enum type.
    :param result: resolved value
    :param info: information related to the execution and the resolved field
    :param execution_context: instance of the query execution context
    :param field_nodes: AST nodes related to the resolved field
    :param path: the path traveled until this resolver
    :param enum_type: the GraphQLType instance of the enum
    :type result: Any
    :type info: ResolveInfo
    :type execution_context: ExecutionContext
    :type field_nodes: List[FieldNode]
    :type path: Path
    :type enum_type: GraphQLEnumType
    :return: the computed value
    :rtype: Any
    """
    # pylint: disable=unused-argument
    try:
        enum_value = enum_type.get_value(result)
        coerced_result = await enum_value.output_coercer(
            enum_value.definition,
            result,
            execution_context.context,
            info,
            context_coercer=execution_context.context,
        )
    except KeyError:
        coerced_result = UNDEFINED_VALUE

    if is_invalid_value(coerced_result):
        raise ValueError(
            f"Expected value of type {enum_type} but received {type(result)}."
        )
    return coerced_result
