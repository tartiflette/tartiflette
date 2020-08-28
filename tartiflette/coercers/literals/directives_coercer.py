from typing import Any, Callable, Dict, Optional, Union

from tartiflette.coercers.common import CoercionResult
from tartiflette.language.ast import VariableNode
from tartiflette.types.exceptions.tartiflette import MultipleException
from tartiflette.utils.errors import (
    graphql_error_from_nodes,
    is_coercible_exception,
)
from tartiflette.utils.values import is_invalid_value

__all__ = ("literal_directives_coercer",)


async def literal_directives_coercer(
    parent_node: Union["VariableDefinitionNode", "InputValueDefinitionNode"],
    node: Union["ValueNode", "VariableNode"],
    ctx: Optional[Any],
    coercer: Callable,
    directives: Optional[Callable],
    definition_node: "Node",
    variables: Optional[Dict[str, Any]] = None,
    path: Optional["Path"] = None,
    is_input_field: bool = False,
    is_non_null_type: bool = False,
) -> Any:
    """
    Executes the directives on the coerced value.
    :param parent_node: the root parent AST node
    :param node: the AST node to treat
    :param ctx: context passed to the query execution
    :param coercer: pre-computed coercer to use on the value
    :param directives: the directives to execute
    :param definition_node: the definition AST node to coerce
    :param variables: the variables provided in the GraphQL request
    :param path: the path traveled until this coercer
    :param is_input_field: determines whether or not the node is an InputField
    :param is_non_null_type: determines whether or not the value is nullable
    :type parent_node: Union[VariableDefinitionNode, InputValueDefinitionNode]
    :type node: Union[ValueNode, VariableNode]
    :type ctx: Optional[Any]
    :type coercer: Callable
    :type directives: Optional[Callable]
    :type definition_node: Node
    :type variables: Optional[Dict[str, Any]]
    :type path: Optional[Path]
    :type is_input_field: bool
    :type is_non_null_type: bool
    :return: the computed value
    :rtype: Any
    """
    # pylint: disable=too-many-locals,too-many-arguments
    coercion_result = await coercer(
        parent_node,
        node,
        ctx,
        variables=variables,
        path=path,
        is_non_null_type=is_non_null_type,
    )

    if not directives or (
        isinstance(node, VariableNode) and not is_input_field
    ):
        return coercion_result

    value, errors = coercion_result
    if is_invalid_value(value) or errors:
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
