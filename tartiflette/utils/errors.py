from functools import partial
from typing import Any, Callable, Dict, List, Optional, Union

from tartiflette.coercers.common import Path
from tartiflette.types.exceptions.tartiflette import (
    MultipleException,
    TartifletteError,
)

__all__ = (
    "is_coercible_exception",
    "to_graphql_error",
    "graphql_error_from_nodes",
    "located_error",
    "default_error_coercer",
    "error_coercer_factory",
)


def is_coercible_exception(exception: Exception) -> bool:
    """
    Determines whether or not the exception is coercible.
    :param exception: exception to check
    :type exception: Any
    :return: whether or not the exception is coercible
    :rtype: bool
    """
    return hasattr(exception, "coerce_value") and callable(
        exception.coerce_value
    )


def to_graphql_error(
    raw_exception: Exception, message: Optional[str] = None
) -> Union["TartifletteError", Exception]:
    """
    Converts the raw exception into a TartifletteError if its not coercible or
    returns the raw exception if coercible.
    :param raw_exception: the raw exception to be treated
    :param message: message replacing the raw exception message when it's not
    coercible
    :type raw_exception: Exception
    :type message: Optional[str]
    :return: a coercible exception
    :rtype: Union["TartifletteError", Exception]
    """
    return (
        raw_exception
        if is_coercible_exception(raw_exception)
        else TartifletteError(
            message or str(raw_exception), original_error=raw_exception
        )
    )


def graphql_error_from_nodes(
    message: str,
    nodes: Union["Node", List["Node"]],
    path: Optional[Union[List[str], "Path"]] = None,
    original_error: Optional[Exception] = None,
    extensions: Optional[Dict[str, Any]] = None,
) -> "TartifletteError":
    """
    Returns a TartifletteError linked to a list of AST nodes which make it
    possible to fill in the location of the error.
    :param message: error message
    :param nodes: AST nodes to link to the error
    :param path: the path where the original exception occurred
    :param original_error: the original raised exception
    :param extensions: Extensions dict to add to the error.
    :type message: str
    :type nodes: Union[Node, List[Node]]
    :type path: Optional[List[str]]
    :type original_error: Optional[Exception]
    :type extensions: Optional[Dict[str, Any]]
    :return: a TartifletteError with locations
    :rtype: TartifletteError
    """
    if not isinstance(nodes, list):
        nodes = [nodes]

    if isinstance(path, Path):
        path = path.as_list()

    return TartifletteError(
        message,
        locations=[node.location for node in nodes],
        path=path,
        original_error=original_error,
        extensions=extensions,
    )


def located_error(
    original_error: Exception,
    nodes: List["Node"],
    path: Optional[List[str]] = None,
) -> "MultipleException":
    """
    Returns a MultipleException exception with exceptions from the original
    error and apply the proper path and locations to them.
    :param original_error: the original raised exception
    :param nodes: AST nodes to link to the error
    :param path: the path where the original exception occurred
    :type original_error: Exception
    :type nodes: List[Node]
    :type path: Optional[List[str]]
    :return: a MultipleException exception with exceptions from the original
    error
    :rtype: MultipleException
    """
    if nodes is None:
        nodes = []

    if not isinstance(nodes, list):
        nodes = [nodes]

    exceptions = (
        original_error.exceptions
        if isinstance(original_error, MultipleException)
        else [original_error]
    )

    computed_exceptions = []
    for exception in exceptions:
        graphql_error = (
            exception
            if is_coercible_exception(exception)
            else graphql_error_from_nodes(
                str(exception),
                nodes=nodes,
                path=path,
                original_error=exception,
            )
        )

        # TODO: this is ugly AF... we should refactor it :D
        is_partial = isinstance(graphql_error.coerce_value, partial)
        if path and (
            not hasattr(graphql_error, "path") or not graphql_error.path
        ):
            if (
                not is_partial
                or "path" not in graphql_error.coerce_value.keywords
            ):
                graphql_error.coerce_value = partial(
                    graphql_error.coerce_value, path=path
                )
                is_partial = True

        if nodes and (
            not hasattr(graphql_error, "locations")
            or not graphql_error.locations
        ):
            if (
                not is_partial
                or "locations" not in graphql_error.coerce_value.keywords
            ):
                graphql_error.coerce_value = partial(
                    graphql_error.coerce_value,
                    locations=[node.location for node in nodes],
                )

        computed_exceptions.append(graphql_error)

    return MultipleException(exceptions=computed_exceptions)


def extract_exceptions_from_results(
    results: List[Any]
) -> Optional["MultipleException"]:
    """
    Extracts and concatenates multiple exceptions instances from the results.
    :param results: results list to loop over
    :type results: List[Any]
    :return: a multiple exceptions instance with all exceptions contained in
    the result
    :rtype: Optional[MultipleException]
    """
    exceptions = MultipleException()
    for result in results:
        if isinstance(result, MultipleException):
            exceptions += result
    return exceptions or None


async def default_error_coercer(
    exception: Exception, error: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Coerce and returns the error related to the exception.
    :param exception: exception raised
    :param error: coerced error
    :type exception: Exception
    :type error: Dict[str, Any]
    :return: the coerced error
    :rtype: Dict[str, Any]
    """
    # pylint: disable=unused-argument
    return error


def error_coercer_factory(error_coercer: Callable) -> Callable:
    """
    Returns a callable in charge of the error coercion of raised exceptions.
    :param error_coercer: callable to use in order to coerce exception
    :type error_coercer: Callable
    :return: a callable in charge of the error coercion of raised exceptions
    :rtype: Callable
    """

    async def func_wrapper(exception: Exception) -> Dict[str, Any]:
        error = exception.coerce_value()
        return await error_coercer(exception, error)

    return func_wrapper


def did_you_mean(suggestion_list: List[str]) -> str:
    """
    Returns a message containing a suggestion list.
    :param suggestion_list: list of suggested values
    :type suggestion_list: List[str]
    :return: a message containing a suggestion list
    :rtype: str
    """
    if not suggestion_list:
        return ""
    message = "Did you mean"
    nb_suggestions = len(suggestion_list)
    if nb_suggestions == 1:
        return f"{message} {suggestion_list[0]}?"
    if nb_suggestions == 2:
        return f"{message} {suggestion_list[0]} or {suggestion_list[1]}?"

    last_suggestion = suggestion_list.pop()
    return f"{message} {', '.join(suggestion_list)}, or {last_suggestion}?"
