import asyncio

from typing import Any, Dict, Optional, Union

from tartiflette.coercers.common import CoercionResult, Path
from tartiflette.coercers.literals.null_and_variable_coercer import (
    null_and_variable_coercer_wrapper,
)
from tartiflette.coercers.literals.utils import is_missing_variable
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import ObjectValueNode
from tartiflette.utils.values import is_invalid_value

__all__ = ("input_object_coercer",)

SKIP_FIELD = object()


async def input_field_value_coercer(
    input_field: "GraphQLInputField",
    value_node: Union["ValueNode", "VariableNode", "UNDEFINED_VALUE"],
    ctx: Optional[Any],
    variables: Optional[Dict[str, Any]],
    path: Optional["Path"],
) -> Union["CoercionResult", "UNDEFINED_VALUE", "SKIP_FIELD"]:
    """
    Computes the value of an input field.
    :param input_field: the input field to compute
    :param value_node: the value node to compute
    :param ctx: context passed to the query execution
    :param variables: the variables used in the GraphQL request
    :param path: the path traveled until this coercer
    :type input_field: GraphQLInputField
    :type value_node: Union[ValueNode, VariableNode, UNDEFINED_VALUE]
    :type ctx: Optional[Any]
    :type variables: Optional[Dict[str, Any]]
    :type path: Optional[Path]
    :return: the computed value
    :rtype: Union[CoercionResult, UNDEFINED_VALUE, SKIP_FIELD]
    """
    if is_invalid_value(value_node) or is_missing_variable(
        value_node.value, variables
    ):
        if input_field.default_value is not None:
            input_field_node = input_field.default_value
        elif input_field.graphql_type.is_non_null_type:
            return UNDEFINED_VALUE
        else:
            return SKIP_FIELD
    else:
        input_field_node = value_node.value

    return await input_field.literal_coercer(
        input_field_node, ctx, variables=variables, path=path
    )


@null_and_variable_coercer_wrapper
async def input_object_coercer(
    node: Union["ValueNode", "VariableNode"],
    ctx: Optional[Any],
    input_object_type: "GraphQLInputObjectType",
    variables: Optional[Dict[str, Any]] = None,
    path: Optional["Path"] = None,
) -> "CoercionResult":
    """
    Computes the value of an input object.
    :param node: the AST node to treat
    :param ctx: context passed to the query execution
    :param input_object_type: the GraphQLInputObjectType instance of the input
    object
    :param variables: the variables used in the GraphQL request
    :param path: the path traveled until this coercer
    :type node: Union[ValueNode, VariableNode]
    :type ctx: Optional[Any]
    :type input_object_type: GraphQLInputObjectType
    :type variables: Optional[Dict[str, Any]]
    :type path: Optional[Path]
    :return: the computed value
    :rtype: CoercionResult
    """
    # pylint: disable=too-many-locals
    if not isinstance(node, ObjectValueNode):
        return CoercionResult(value=UNDEFINED_VALUE)

    field_nodes = {
        field_node.name.value: field_node for field_node in node.fields
    }

    input_fields = input_object_type.input_fields

    results = await asyncio.gather(
        *[
            input_field_value_coercer(
                input_field,
                field_nodes.get(input_field_name, UNDEFINED_VALUE),
                ctx,
                variables,
                path=Path(path, input_field_name),
            )
            for input_field_name, input_field in input_fields.items()
        ]
    )

    errors = []
    coerced_values = {}
    for input_field_name, input_field_result in zip(input_fields, results):
        if input_field_result is SKIP_FIELD:
            continue

        if is_invalid_value(input_field_result):
            return CoercionResult(value=UNDEFINED_VALUE)

        input_field_value, input_field_errors = input_field_result
        if is_invalid_value(input_field_value):
            return CoercionResult(value=UNDEFINED_VALUE)
        if input_field_errors:
            errors.extend(input_field_errors)
        elif not errors:
            coerced_values[input_field_name] = input_field_value

    return CoercionResult(value=coerced_values, errors=errors)
