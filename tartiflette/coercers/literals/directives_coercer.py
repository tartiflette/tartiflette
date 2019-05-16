from typing import Any, Callable, Dict, Optional, Union

from tartiflette.coercers.common import CoercionResult, coercion_error
from tartiflette.language.ast import VariableNode
from tartiflette.types.exceptions.tartiflette import MultipleException
from tartiflette.utils.errors import is_coercible_exception
from tartiflette.utils.values import is_invalid_value

__all__ = ("literal_directives_coercer",)


async def literal_directives_coercer(
    node: Union["ValueNode", "VariableNode"],
    ctx: Optional[Any],
    coercer: Callable,
    directives: Optional[Callable],
    variables: Optional[Dict[str, Any]] = None,
    path: Optional["Path"] = None,
    is_input_field: bool = False,
) -> Any:
    """
    Executes the directives on the coerced value.
    :param node: the AST node to treat
    :param ctx: context passed to the query execution
    :param coercer: pre-computed coercer to use on the value
    :param directives: the directives to execute
    :param variables: the variables used in the GraphQL request
    :param path: the path traveled until this coercer
    :param is_input_field: determines whether or not the node is an InputField
    :type node: Union[ValueNode, VariableNode]
    :type ctx: Optional[Any]
    :type coercer: Callable
    :type directives: Optional[Callable]
    :type variables: Optional[Dict[str, Any]]
    :type path: Optional[Path]
    :type is_input_field: bool
    :return: the computed value
    :rtype: Any
    """
    # pylint: disable=too-many-locals
    coercion_result = await coercer(node, ctx, variables=variables, path=path)

    if not directives or (
        isinstance(node, VariableNode) and not is_input_field
    ):
        return coercion_result

    value, errors = coercion_result
    if is_invalid_value(value) or errors:
        return coercion_result

    try:
        return CoercionResult(
            value=await directives(value, ctx, context_coercer=ctx)
        )
    except Exception as raw_exception:  # pylint: disable=broad-except
        return CoercionResult(
            errors=[
                coercion_error(
                    str(raw_exception),
                    node,
                    path,
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
