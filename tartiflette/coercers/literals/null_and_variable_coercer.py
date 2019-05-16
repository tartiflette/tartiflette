from typing import Any, Callable, Dict, Optional

from tartiflette.coercers.common import CoercionResult
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import NullValueNode, VariableNode
from tartiflette.utils.values import is_invalid_value

__all__ = ("null_and_variable_coercer_wrapper",)


def null_and_variable_coercer_wrapper(coercer: Callable) -> Callable:
    """
    Factorization of the treatment making it possible to coerce a NullValueNode
    or a VariableNode.
    :param coercer: the pre-computed coercer to use on the value if not a
    NullValueNode neither a VariableNode
    :type coercer: Callable
    :return: the wrapped coercer
    :rtype: Callable
    """

    async def wrapper(
        node: "Node",
        ctx: Optional[Any],
        variables: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> "CoercionResult":
        if not node:
            return CoercionResult(value=UNDEFINED_VALUE)

        if isinstance(node, NullValueNode):
            return CoercionResult(value=None)

        if isinstance(node, VariableNode):
            if not variables:
                return CoercionResult(value=UNDEFINED_VALUE)

            value = variables.get(node.name.value, UNDEFINED_VALUE)
            if is_invalid_value(value):
                return CoercionResult(value=UNDEFINED_VALUE)

            # TODO: check this
            # if value is None and schema_type.is_non_null_type:
            #     return CoercionResult(value=UNDEFINED_VALUE)
            return CoercionResult(value=value)

        return await coercer(node, ctx, variables=variables, **kwargs)

    return wrapper
