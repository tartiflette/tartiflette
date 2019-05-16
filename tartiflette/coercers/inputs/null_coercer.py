from typing import Any, Callable, Optional

from tartiflette.coercers.common import CoercionResult

__all__ = ("null_coercer_wrapper",)


def null_coercer_wrapper(coercer: Callable) -> Callable:
    """
    Skips the node coercion if the value is `None` and directly returns it.
    :param coercer: the pre-computed coercer to use on the value
    :type coercer: Callable
    :return: the wrapped coercer
    :rtype: Callable
    """

    async def wrapper(
        node: "Node", value: Any, ctx: Optional[Any], **kwargs
    ) -> "CoercionResult":
        if value is None:
            return CoercionResult(value=None)

        return await coercer(node, value, ctx, **kwargs)

    return wrapper
