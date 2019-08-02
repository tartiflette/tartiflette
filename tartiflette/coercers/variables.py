import asyncio

from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from tartiflette.coercers.common import CoercionResult
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.types.exceptions.tartiflette import CoercionError
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.utils.values import is_invalid_value

__all__ = ("variable_coercer", "coerce_variables")


async def variable_coercer(
    executable_variable_definition: "ExecutableVariableDefinition",
    raw_variable_values: Dict[str, Any],
    ctx: Optional[Any],
    input_coercer: Callable,
    literal_coercer: Callable,
) -> Union["CoercionResult", "UNDEFINED_VALUE"]:
    """
    Computes the value of a variable.
    :param executable_variable_definition: the variable definition to treat
    :param raw_variable_values: the raw variables values to coerce
    :param ctx: context passed to the query execution
    :param input_coercer: callable to use to compute the variable value
    :param literal_coercer: callable to use to compute AST node into value
    :type executable_variable_definition: ExecutableVariableDefinition
    :type raw_variable_values: Dict[str, Any]
    :type ctx: Optional[Any]
    :type input_coercer: Callable
    :type literal_coercer: Callable
    :return: the computed value of the variable definition
    :rtype: Union[CoercionResult, UNDEFINED_VALUE]
    """
    # pylint: disable=too-many-locals
    var_name = executable_variable_definition.name
    var_type = executable_variable_definition.graphql_type
    has_value = var_name in raw_variable_values
    value = raw_variable_values.get(var_name, UNDEFINED_VALUE)
    default_value = executable_variable_definition.default_value
    variable_definition_node = executable_variable_definition.definition

    if not has_value and not is_invalid_value(default_value):
        # TODO: we should be able to remove this once the `ValuesOfCorrectType`
        # rule of `validate_document` will be implemented
        coercion_result = await literal_coercer(
            variable_definition_node, default_value, ctx
        )
        value, _ = coercion_result
        if is_invalid_value(value):
            return CoercionResult(
                errors=[
                    graphql_error_from_nodes(
                        f"Variable < ${var_name} > got invalid default value "
                        f"< {default_value} >.",
                        nodes=default_value,
                    )
                ]
            )
        return coercion_result

    if (not has_value or value is None) and var_type.is_non_null_type:
        return CoercionResult(
            errors=[
                graphql_error_from_nodes(
                    (
                        f"Variable < ${var_name} > of non-null type "
                        f"< {var_type} > must not be null."
                    )
                    if has_value
                    else (
                        f"Variable < ${var_name} > of required type "
                        f"< {var_type} > was not provided."
                    ),
                    nodes=variable_definition_node,
                )
            ]
        )

    if has_value:
        coerced_value, coerce_errors = await input_coercer(
            variable_definition_node, value, ctx
        )
        if coerce_errors:
            for coerce_error in coerce_errors:
                if isinstance(coerce_error, CoercionError):
                    coerce_error.message = (
                        f"Variable < ${var_name} > got invalid value "
                        f"< {value} >; {coerce_error.message}"
                    )
            return CoercionResult(errors=coerce_errors)
        return CoercionResult(value=coerced_value)

    return UNDEFINED_VALUE


async def coerce_variables(
    executable_variable_definitions: List["ExecutableVariableDefinition"],
    raw_variable_values: Dict[str, Any],
    ctx: Optional[Any],
) -> Tuple[Dict[str, Any], List["TartifletteError"]]:
    """
    Returns the computed values of the variables.
    :param executable_variable_definitions: the variable definitions to treat
    :param raw_variable_values: the raw variables values to coerce
    :param ctx: context passed to the query execution
    :type executable_variable_definitions: List[ExecutableVariableDefinition]
    :type raw_variable_values: Dict[str, Any]
    :type ctx: Optional[Any]
    :return: the computed values of the variables
    :rtype: Tuple[Dict[str, Any], List["TartifletteError"]]
    """
    # pylint: disable=too-many-locals
    results = await asyncio.gather(
        *[
            executable_variable_definition.coercer(raw_variable_values, ctx)
            for executable_variable_definition in executable_variable_definitions
        ],
        return_exceptions=True,
    )

    coercion_errors: List["TartifletteError"] = []
    coerced_values: Dict[str, Any] = {}

    for executable_variable_definition, result in zip(
        executable_variable_definitions, results
    ):
        if is_invalid_value(result):
            continue

        value, errors = result
        if errors:
            coercion_errors.extend(errors)
        else:
            coerced_values[executable_variable_definition.name] = value

    return coerced_values, coercion_errors
