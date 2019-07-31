from typing import Any, Callable, Dict, Optional, Union

from tartiflette.coercers.common import CoercionResult
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import NullValueNode

__all__ = ("non_null_coercer",)


async def non_null_coercer(
    node: Union["ValueNode", "VariableNode"],
    ctx: Optional[Any],
    inner_coercer: Callable,
    variables: Optional[Dict[str, Any]] = None,
    path: Optional["Path"] = None,
    **kwargs,
) -> "CoercionResult":
    """
    Checks if the value is NullValueNode and will raise an error if its the
    case or will try to coerce it.
    :param node: the AST node to treat
    :param ctx: context passed to the query execution
    :param inner_coercer: the pre-computed coercer to use on the value
    :param variables: the variables provided in the GraphQL request
    :param path: the path traveled until this coercer
    :type node: Union[ValueNode, VariableNode]
    :type ctx: Optional[Any]
    :type inner_coercer: Callable
    :type variables: Optional[Dict[str, Any]]
    :type path: Optional[Path]
    :return: the computed value
    :rtype: CoercionResult
    """
    # pylint: disable=unused-argument
    if isinstance(node, NullValueNode):
        return CoercionResult(value=UNDEFINED_VALUE)

    return await inner_coercer(
        node, ctx, variables=variables, path=path, is_non_null_type=True
    )
