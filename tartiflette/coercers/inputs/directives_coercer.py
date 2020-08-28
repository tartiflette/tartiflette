from typing import Any, Callable, Optional, Union

from tartiflette.coercers.common import CoercionResult
from tartiflette.types.exceptions.tartiflette import MultipleException
from tartiflette.utils.errors import (
    graphql_error_from_nodes,
    is_coercible_exception,
)

__all__ = ("input_directives_coercer",)


async def input_directives_coercer(
    parent_node: Union["VariableDefinitionNode", "InputValueDefinitionNode"],
    node: "Node",
    value: Any,
    ctx: Optional[Any],
    coercer: Callable,
    directives: Optional[Callable],
    definition_node: "Node",
    path: Optional["Path"] = None,
) -> "CoercionResult":
    """
    Executes the directives on the coerced value.
    :param parent_node: the root parent AST node
    :param node: the AST node to treat
    :param value: the raw value to compute
    :param ctx: context passed to the query execution
    :param coercer: pre-computed coercer to use on the value
    :param directives: the directives to execute
    :param definition_node: the definition AST node to coerce
    :param path: the path traveled until this coercer
    :type parent_node: Union[VariableDefinitionNode, InputValueDefinitionNode]
    :type node: Node
    :type value: Any
    :type ctx: Optional[Any]
    :type coercer: Callable
    :type directives: Optional[Callable]
    :type definition_node: Node
    :type path: Optional[Path]
    :return: the coercion result
    :rtype: CoercionResult
    """
    coercion_result = await coercer(parent_node, node, value, ctx, path=path)

    if not directives:
        return coercion_result

    value, errors = coercion_result
    if errors:
        return coercion_result

    try:
        return CoercionResult(
            value=await directives(
                parent_node, definition_node, value, ctx, context_coercer=ctx
            )
        )
    except Exception as raw_exception:  # pylint: disable=broad-except
        return CoercionResult(
            errors=[
                graphql_error_from_nodes(
                    str(raw_exception),
                    node,
                    original_error=(
                        raw_exception
                        if not is_coercible_exception(raw_exception)
                        else None
                    ),
                )
                for raw_exception in (
                    raw_exception.exceptions
                    if isinstance(raw_exception, MultipleException)
                    else [raw_exception]
                )
            ]
        )
