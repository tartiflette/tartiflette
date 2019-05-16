import asyncio

from typing import Any, Optional, Union

from tartiflette.coercers.common import CoercionResult, Path, coercion_error
from tartiflette.coercers.inputs.null_coercer import null_coercer_wrapper
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.utils.values import is_invalid_value

__all__ = ("input_object_coercer",)


async def input_field_value_coercer(
    node: "Node",
    value: Any,
    ctx: Optional[Any],
    input_field: "GraphQLInputField",
    path: "Path",
) -> Union["CoercionResult", "UNDEFINED_VALUE"]:
    """
    Computes the value of an input field object.
    :param node: the AST node to treat
    :param value: the raw value to compute
    :param ctx: context passed to the query execution
    :param input_field: the input field to compute
    :param path: the path traveled until this coercer
    :type node: Node
    :type value: Any
    :type ctx: Optional[Any]
    :type input_field: GraphQLInputField
    :type path: Path
    :return: the coercion result
    :rtype: Union[CoercionResult, UNDEFINED_VALUE]
    """
    if is_invalid_value(value):
        if input_field.default_value is not None:
            return await input_field.literal_coercer(
                input_field.default_value, ctx
            )
        if input_field.graphql_type.is_non_null_type:
            return CoercionResult(
                errors=[
                    coercion_error(
                        f"Field < {path} > of required type "
                        f"< {input_field.gql_type} > was not provided",
                        node,
                    )
                ]
            )
        return UNDEFINED_VALUE

    return await input_field.input_coercer(node, value, ctx, path=path)


@null_coercer_wrapper
async def input_object_coercer(
    node: "Node",
    value: Any,
    ctx: Optional[Any],
    input_object_type: "GraphQLInputObjectType",
    path: Optional["Path"] = None,
) -> "CoercionResult":
    """
    Computes the value of an input object.
    :param node: the AST node to treat
    :param value: the raw value to compute
    :param ctx: context passed to the query execution
    :param input_object_type: the GraphQLInputObjectType instance of the input
    object
    :param path: the path traveled until this coercer
    :type node: Node
    :type value: Any
    :type ctx: Optional[Any]
    :type input_object_type: GraphQLInputObjectType
    :type path: Optional[Path]
    :return: the coercion result
    :rtype: CoercionResult
    """
    # pylint: disable=too-many-locals
    if not isinstance(value, dict):
        return CoercionResult(
            errors=[
                coercion_error(
                    f"Expected type < {input_object_type.name} > to be an object",
                    node,
                    path,
                )
            ]
        )

    input_fields = input_object_type.input_fields

    results = await asyncio.gather(
        *[
            input_field_value_coercer(
                node,
                value.get(input_field_name, UNDEFINED_VALUE),
                ctx,
                input_field,
                path=Path(path, input_field_name),
            )
            for input_field_name, input_field in input_fields.items()
        ]
    )

    errors = []
    coerced_values = {}
    for input_field_name, input_field_result in zip(input_fields, results):
        if is_invalid_value(input_field_result):
            continue

        input_field_value, input_field_errors = input_field_result
        if input_field_errors:
            errors.extend(input_field_errors)
        elif not errors:
            coerced_values[input_field_name] = input_field_value

    for input_field_name in value:
        if input_field_name not in input_fields:
            # TODO: try to compute a suggestion list of valid input fields
            # depending on the invalid field name returns it as
            # error sub message
            errors.append(
                coercion_error(
                    f"Field < {input_field_name} > is not defined by type "
                    f"< {input_object_type.name} >",
                    node,
                    path,
                )
            )

    return CoercionResult(value=coerced_values, errors=errors)
