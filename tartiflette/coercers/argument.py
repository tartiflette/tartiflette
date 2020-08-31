from typing import Any, Callable, Dict, Optional, Union

from tartiflette.coercers.common import CoercionResult
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import NullValueNode, VariableNode
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.utils.values import is_invalid_value

__all__ = ("argument_coercer",)


async def argument_coercer(
    argument_definition: "GraphQLArgument",
    node: Union["FieldNode", "DirectiveNode"],
    argument_node: Optional["ArgumentNode"],
    variable_values: Dict[str, Any],
    ctx: Optional[Any],
    directives: Optional[Callable],
) -> Union["CoercionResult", "UNDEFINED_VALUE"]:
    """
    Computes the value of an argument.
    :param argument_definition: the argument definition to treat
    :param node: AST node linked to the argument
    :param argument_node: AST node representing the argument
    :param variable_values: the variables provided in the GraphQL request
    :param ctx: context passed to the query execution
    :param directives: the directives to execute
    :type argument_definition: GraphQLArgument
    :type node: Union[FieldNode, DirectiveNode]
    :type argument_node: Optional[ArgumentNode]
    :type variable_values: Dict[str, Any]
    :type ctx: Optional[Any]
    :type directives: Optional[Callable]
    :return: the computed value
    :rtype: Union["CoercionResult", "UNDEFINED_VALUE"]
    """
    # pylint: disable=too-many-locals,too-many-branches,too-complex
    name = argument_definition.name
    arg_type = argument_definition.graphql_type

    if argument_node and isinstance(argument_node.value, VariableNode):
        variable_name = argument_node.value.name.value
        has_value = variable_values and variable_name in variable_values
        is_null = has_value and variable_values[variable_name] is None
    else:
        has_value = argument_node is not None
        is_null = argument_node and isinstance(
            argument_node.value, NullValueNode
        )

    coercion_result = UNDEFINED_VALUE
    value_node = None
    if not has_value and argument_definition.default_value is not None:
        value_node = argument_definition.default_value
    elif (not has_value or is_null) and arg_type.is_non_null_type:
        if is_null:
            return CoercionResult(
                errors=[
                    graphql_error_from_nodes(
                        f"Argument < {name} > of non-null type < {arg_type} > "
                        "must not be null.",
                        nodes=argument_node.value,
                    )
                ]
            )
        if argument_node and isinstance(argument_node.value, VariableNode):
            return CoercionResult(
                errors=[
                    graphql_error_from_nodes(
                        f"Argument < {name} > of required type < {arg_type} > "
                        f"was provided the variable < ${variable_name} > "
                        "which was not provided a runtime value.",
                        nodes=argument_node.value,
                    )
                ]
            )
        return CoercionResult(
            errors=[
                graphql_error_from_nodes(
                    f"Argument < {name} > of required type < {arg_type} > was "
                    "not provided.",
                    nodes=node,
                )
            ]
        )
    elif has_value:
        if isinstance(argument_node.value, NullValueNode):
            coercion_result = CoercionResult(value=None)
        elif isinstance(argument_node.value, VariableNode):
            coercion_result = CoercionResult(
                value=variable_values[argument_node.value.name.value]
            )
        else:
            value_node = argument_node.value

    if value_node:
        coercion_result = await argument_definition.literal_coercer(
            argument_definition.definition,
            value_node,
            ctx,
            variables=variable_values,
        )

    if is_invalid_value(coercion_result):
        return coercion_result

    value, errors = coercion_result
    if is_invalid_value(value):
        return CoercionResult(
            errors=[
                graphql_error_from_nodes(
                    f"Argument < {name} > has invalid value < {value_node} >.",
                    nodes=argument_node.value,
                )
            ]
        )
    if not directives or errors:
        return coercion_result

    return await directives(
        node, argument_definition.definition, value, ctx, context_coercer=ctx
    )
