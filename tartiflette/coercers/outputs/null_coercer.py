from typing import Any, Callable

__all__ = ("null_coercer_wrapper",)


def null_coercer_wrapper(coercer: Callable) -> Callable:
    """
    Skips the node coercion if the value is `None` and directly returns it.
    :param coercer: the pre-computed coercer to use on the value
    :type coercer: Callable
    :return: the wrapped coercer
    :rtype: Callable
    """

    async def wrapper(result: Any, *args, **kwargs) -> Any:
        if result is None:
            return None
        return await coercer(result, *args, **kwargs)

    return wrapper
