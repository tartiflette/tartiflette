import asyncio

from typing import Any, Callable, Optional, Union

from tartiflette.coercers.common import CoercionResult, Path
from tartiflette.coercers.inputs.null_coercer import null_coercer_wrapper

__all__ = ("list_coercer",)


@null_coercer_wrapper
async def list_coercer(
    parent_node: Union["VariableDefinitionNode", "InputValueDefinitionNode"],
    node: "Node",
    value: Any,
    ctx: Optional[Any],
    inner_coercer: Callable,
    path: Optional["Path"] = None,
) -> "CoercionResult":
    """
    Computes the value of a list.
    :param parent_node: the root parent AST node
    :param node: the AST node to treat
    :param value: the raw value to compute
    :param ctx: context passed to the query execution
    :param inner_coercer: the pre-computed coercer to use on each value in the
    list
    :param path: the path traveled until this coercer
    :type parent_node: Union[VariableDefinitionNode, InputValueDefinitionNode]
    :type node: Node
    :type value: Any
    :type ctx: Optional[Any]
    :type inner_coercer: Callable
    :type path: Optional[Path]
    :return: the coercion result
    :rtype: CoercionResult
    """
    # pylint: disable=too-many-locals
    if isinstance(value, list):
        results = await asyncio.gather(
            *[
                inner_coercer(
                    parent_node, node, item_value, ctx, path=Path(path, index)
                )
                for index, item_value in enumerate(value)
            ]
        )

        errors = []
        coerced_values = []
        for coerced_value, coerced_errors in results:
            if coerced_errors:
                errors.extend(coerced_errors)
            elif not errors:
                coerced_values.append(coerced_value)

        return CoercionResult(value=coerced_values, errors=errors)

    coerced_item_value, coerced_item_errors = await inner_coercer(
        parent_node, node, value, ctx, path=path
    )
    return CoercionResult(
        value=[coerced_item_value], errors=coerced_item_errors
    )
