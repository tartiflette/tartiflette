from typing import Any, Callable, Optional

from tartiflette.coercers.common import CoercionResult, coercion_error

__all__ = ("non_null_coercer",)


async def non_null_coercer(
    node: "Node",
    value: Any,
    ctx: Optional[Any],
    graphql_type: "GraphQLType",
    inner_coercer: Callable,
    path: Optional["Path"] = None,
) -> "CoercionResult":
    """
    Checks if the value is `None` and will raise an error if its the case or
    will try to coerce it.
    :param node: the AST node to treat
    :param value: the raw value to compute
    :param ctx: context passed to the query execution
    :param graphql_type: the schema type of the expected value
    :param inner_coercer: the pre-computed coercer to use on the value
    :param path: the path traveled until this coercer
    :type node: Node
    :type value: Any
    :type ctx: Optional[Any]
    :type graphql_type: GraphQLType
    :type inner_coercer: Callable
    :type path: Optional[Path]
    :return: the coercion result
    :rtype: CoercionResult
    """
    if value is None:
        return CoercionResult(
            errors=[
                coercion_error(
                    f"Expected non-nullable type < {graphql_type} > not to be "
                    "null",
                    node,
                    path,
                )
            ]
        )
    return await inner_coercer(node, value, ctx, path=path)
