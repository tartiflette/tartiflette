from typing import Any, Callable, Dict, List, Optional, Union

from tartiflette.coercers.common import CoercionResult
from tartiflette.types.exceptions.tartiflette import MultipleException
from tartiflette.utils.errors import located_error
from tartiflette.utils.values import is_invalid_value

__all__ = ("coerce_arguments",)


async def coerce_arguments(
    argument_definitions: Dict[str, "GraphQLArgument"],
    node: Union["FieldNode", "DirectiveNode"],
    variable_values: Dict[str, Any],
    ctx: Optional[Any],
    coercer: Callable,
) -> Dict[str, Any]:
    """
    Returns the computed values of the arguments.
    :param argument_definitions: the argument definitions to treat
    :param node: the parent AST node of the arguments
    :param variable_values: the variables provided in the GraphQL request
    :param ctx: context passed to the query execution
    :param coercer: callable to use to coerce arguments
    :type argument_definitions: Dict[str, GraphQLArgument]
    :type node: Union[FieldNode, DirectiveNode]
    :type variable_values: Dict[str, Any]
    :type ctx: Optional[Any]
    :type coercer: Callable
    :return: the computed values of the arguments
    :rtype: Dict[str, Any]
    """
    # pylint: disable=too-many-locals
    argument_nodes = node.arguments
    if not argument_definitions or argument_nodes is None:
        return {}

    argument_nodes_map = {
        argument_node.name.value: argument_node
        for argument_node in argument_nodes
    }

    results = await coercer(
        *[
            argument_definition.coercer(
                argument_definition,
                node,
                argument_nodes_map.get(argument_definition.name),
                variable_values,
                ctx,
            )
            for argument_definition in argument_definitions.values()
        ],
    )

    coercion_errors: List["TartifletteError"] = []
    coerced_values: Dict[str, Any] = {}

    for argument_name, result in zip(argument_definitions, results):
        if isinstance(result, Exception):
            coercion_errors.extend(
                located_error(
                    result, nodes=argument_nodes_map.get(argument_name)
                ).exceptions
            )
            continue

        if is_invalid_value(result):
            continue

        if not isinstance(result, CoercionResult):
            coerced_values[argument_name] = result
            continue

        value, errors = result
        if errors:
            coercion_errors.extend(errors)
        elif not is_invalid_value(result):
            coerced_values[argument_name] = value

    if coercion_errors:
        raise MultipleException(coercion_errors)

    return coerced_values
