from typing import List, Optional, Union

from tartiflette.types.exceptions.tartiflette import GraphQLError


def is_coercible_exception(exception: Exception) -> bool:
    """
    Determines whether or not the exception is coercible.
    :param value: exception to check
    :type value: Any
    :return: whether or not the exception is coercible
    :rtype: bool
    """
    return hasattr(exception, "coerce_value") and callable(
        exception.coerce_value
    )


def to_graphql_error(
    exception: Exception, message: Optional[str] = None
) -> Union["GraphQLError", Exception]:
    """
    TODO:
    :param exception: TODO:
    :param message: TODO:
    :type exception: TODO:
    :type message: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    if is_coercible_exception(exception):
        return exception
    return GraphQLError(message or str(exception), original_error=exception)


def graphql_error_from_nodes(
    message: str, nodes: Optional[Union["Node", List["Node"]]] = None
) -> "GraphQLError":
    """
    TODO:
    :param message: TODO:
    :param nodes: TODO:
    :type message: TODO:
    :type nodes: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    if nodes is None:
        nodes = []

    if not isinstance(nodes, list):
        nodes = [nodes]

    return GraphQLError(message, locations=[node.location for node in nodes])
