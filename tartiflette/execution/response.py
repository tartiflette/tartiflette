import asyncio

from typing import Any, Callable, Dict, List, Optional

__all__ = ("build_response",)


async def build_response(
    error_coercer: Callable,
    data: Optional[Dict[str, Any]] = None,
    errors: Optional[List["TartifletteError"]] = None,
) -> Dict[str, Any]:
    """
    Returns and formats the data and errors into a proper GraphQL response.
    :param error_coercer: callable in charge of transforming a couple
    Exception/error into an error dictionary
    :param data: the data from fields execution
    :param errors: the errors encountered during the request execution
    :type error_coercer: Callable
    :type data: Optional[Dict[str, Any]]
    :type errors: Optional[List[TartifletteError]]
    :return: a GraphQL response
    :rtype: Dict[str, Any]
    """
    coerced_errors = (
        await asyncio.gather(*[error_coercer(error) for error in errors])
        if errors
        else None
    )
    if coerced_errors:
        return {"data": data, "errors": coerced_errors}
    return {"data": data}
