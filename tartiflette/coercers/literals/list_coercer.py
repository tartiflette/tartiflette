import asyncio

from typing import Any, Callable, Dict, Optional, Union

from tartiflette.coercers.common import CoercionResult, Path
from tartiflette.coercers.literals.null_and_variable_coercer import (
    null_and_variable_coercer_wrapper,
)
from tartiflette.coercers.literals.utils import is_missing_variable
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import ListValueNode
from tartiflette.utils.values import is_invalid_value

__all__ = ("list_coercer",)


async def list_item_coercer(
    item_node: Union["ValueNode", "VariableNode"],
    ctx: Optional[Any],
    is_non_null_item_type: bool,
    inner_coercer: Callable,
    variables: Optional[Dict[str, Any]] = None,
    path: Optional["Path"] = None,
) -> Union["CoercionResult", "UNDEFINED_VALUE"]:
    """
    Computes the value of a, item list.
    :param item_node: the AST item node to treat
    :param ctx: context passed to the query execution
    :param is_non_null_item_type: determines whether or not the item is
    nullable
    :param inner_coercer: the pre-computed coercer to use for the item
    :param variables: the variables used in the GraphQL request
    :param path: the path traveled until this coercer
    :type item_node: Union[ValueNode, VariableNode]
    :type ctx: Optional[Any]
    :type is_non_null_item_type: bool
    :type inner_coercer: Callable
    :type variables: Optional[Dict[str, Any]]
    :type path: Optional[Path]
    :return: the computed value
    :rtype: Union[CoercionResult, UNDEFINED_VALUE]
    """
    if is_missing_variable(item_node, variables):
        if is_non_null_item_type:
            return UNDEFINED_VALUE
        return CoercionResult(value=None)

    return await inner_coercer(item_node, ctx, variables=variables, path=path)


@null_and_variable_coercer_wrapper
async def list_coercer(
    node: Union["ValueNode", "VariableNode"],
    ctx: Optional[Any],
    is_non_null_item_type: bool,
    inner_coercer: Callable,
    variables: Optional[Dict[str, Any]] = None,
    path: Optional["Path"] = None,
) -> "CoercionResult":
    """
    Computes the value of a list.
    :param node: the AST node to treat
    :param ctx: context passed to the query execution
    :param is_non_null_item_type: determines whether or not the inner value is
    nullable
    :param inner_coercer: the pre-computed coercer to use on each value in the
    list
    :param variables: the variables used in the GraphQL request
    :type node: Union[ValueNode, VariableNode]
    :type ctx: Optional[Any]
    :type is_non_null_item_type: bool
    :type inner_coercer: Callable
    :type variables: Optional[Dict[str, Any]]
    :return: the computed value
    :rtype: CoercionResult
    """
    # pylint: disable=too-many-locals
    if isinstance(node, ListValueNode):
        results = await asyncio.gather(
            *[
                list_item_coercer(
                    item_node,
                    ctx,
                    is_non_null_item_type,
                    inner_coercer,
                    variables,
                    path=Path(path, index),
                )
                for index, item_node in enumerate(node.values)
            ]
        )

        errors = []
        coerced_values = []
        for coerced_result in results:
            if is_invalid_value(coerced_result):
                return CoercionResult(value=UNDEFINED_VALUE)

            coerced_value, coerced_errors = coerced_result
            if is_invalid_value(coerced_value):
                return CoercionResult(value=UNDEFINED_VALUE)
            if coerced_errors:
                errors.extend(coerced_errors)
            elif not errors:
                coerced_values.append(coerced_value)

        return CoercionResult(value=coerced_values, errors=errors)

    coerced_item_value, coerced_item_errors = await inner_coercer(
        node, ctx, variables=variables, path=path
    )
    if is_invalid_value(coerced_item_value):
        return CoercionResult(value=UNDEFINED_VALUE)
    return CoercionResult(
        value=[coerced_item_value], errors=coerced_item_errors
    )
