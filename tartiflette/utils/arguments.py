import asyncio

from functools import partial
from typing import Any, Callable, Dict, List, Optional, Union

from tartiflette.types.exceptions.tartiflette import (
    GraphQLError,
    MultipleException,
)
from tartiflette.types.helpers import reduce_type
from tartiflette.types.input_object import GraphQLInputObjectType
from tartiflette.utils.errors import to_graphql_error

UNDEFINED_VALUE = object()


def surround_with_argument_execution_directives(
    func: Callable, directives: List[Dict[str, Any]]
) -> Callable:
    for directive in reversed(directives):
        func = partial(
            directive["callables"].on_argument_execution,
            directive["args"],
            func,
        )
    return func


def get_argument_values(
    argument_definitions: "GraphQLField",
    node: Union["FieldNode", "DirectiveNode"],
    variable_values: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    TODO:
    :param schema_field: TODO:
    :param node: TODO:
    :param variable_values: TODO:
    :type schema_field: TODO:
    :type node: TODO:
    :type variable_values: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    from tartiflette.language.ast import VariableNode, NullValueNode
    from tartiflette.utils.value_from_ast import value_from_ast, is_invalid
    from tartiflette.types.helpers.definition import is_non_null_type

    # argument_definitions = schema_field.arguments
    argument_nodes = node.arguments
    if not argument_definitions or not argument_nodes:
        return {}

    coerced_values = {}
    argument_nodes_map = {
        argument_node.name.value: argument_node
        for argument_node in argument_nodes
    }

    for index, argument_definition in enumerate(
        list(argument_definitions.values())
    ):
        name = argument_definition.name
        arg_type = argument_definition.get_gql_type()
        argument_node = argument_nodes_map[name]

        if argument_node and isinstance(argument_node.value, VariableNode):
            variable_name = argument_node.value.name.value
            has_value = variable_values and variable_name in variable_values
            is_null = has_value and variable_values[variable_name] is None
        else:
            has_value = argument_node is not None
            is_null = argument_node and isinstance(
                argument_node.value, NullValueNode
            )

        if not has_value and argument_definition.default_value is not None:
            coerced_values[name] = argument_definition.default_value
        elif (not has_value and is_null) and is_non_null_type(arg_type):
            if is_null:
                raise GraphQLError(
                    f"Argument < {name} > of non-null type < {arg_type} > "
                    "must not be null.",
                    locations=[argument_node.value.location],
                )
            elif argument_node and isinstance(
                argument_node.value, VariableNode
            ):
                raise GraphQLError(
                    f"Argument < {name} > of required type < {arg_type} > "
                    f"was provided the variable < ${variable_name} > which "
                    "was not provided a runtime value.",
                    locations=[argument_node.value.location],
                )
            else:
                raise GraphQLError(
                    f"Argument < {name} > of required type < {arg_type} > was "
                    "not provided."
                )
        elif has_value:
            if isinstance(argument_node.value, NullValueNode):
                coerced_values[name] = None
            elif isinstance(argument_node.value, VariableNode):
                variable_name = argument_node.value.name.value
                coerced_values[name] = variable_values[variable_name]
            else:
                value_node = argument_node.value
                coerced_value = value_from_ast(
                    value_node, arg_type, variable_values
                )
                if is_invalid(coerced_value):
                    raise GraphQLError(
                        f"Argument < {name} > has invalid value "
                        f"< {value_node} >."
                    )
                coerced_values[name] = coerced_value
    return coerced_values


async def argument_coercer(
    argument_definition, args, ctx, info, input_coercer=None
):
    value = UNDEFINED_VALUE
    try:
        value = args[argument_definition.name]
    except KeyError:
        pass

    if value is UNDEFINED_VALUE and argument_definition.default_value:
        value = argument_definition.default_value

    if value is UNDEFINED_VALUE:
        return value

    try:
        value = (
            value.value
            if not input_coercer
            else input_coercer(value.value, info)
        )
    except AttributeError:
        pass

    if value is None:
        return None

    schema_type = argument_definition.schema.find_type(
        reduce_type(argument_definition.gql_type)
    )

    if (
        not isinstance(schema_type, GraphQLInputObjectType)
        or argument_definition.is_list_type
    ):
        return value

    if (
        not isinstance(argument_definition.gql_type, str)
        and argument_definition.is_list_type
    ):
        return await asyncio.gather(
            *[
                coerce_arguments(schema_type.arguments, x, ctx, info)
                for x in value
            ]
        )

    return await coerce_arguments(schema_type.arguments, value, ctx, info)


async def coerce_arguments(
    argument_definitions: Dict[str, "GraphQLArgument"],
    input_args: Dict[str, Any],
    ctx: Optional[Dict[str, Any]],
    info: "Info",
    variable_values,
) -> Dict[str, Any]:
    results = await asyncio.gather(
        *[
            argument_definition.coercer(variable_values, ctx, info)
            for argument_definition in argument_definitions.values()
        ],
        return_exceptions=True,
    )

    coerced_arguments = {}
    exceptions = []

    for argument_name, result in zip(argument_definitions, results):
        if isinstance(result, MultipleException):
            exceptions.extend(result.exceptions)
            continue

        if isinstance(result, Exception):
            exceptions.append(to_graphql_error(result))
            continue

        if result is not UNDEFINED_VALUE:
            coerced_arguments[argument_name] = result

    if exceptions:
        raise MultipleException(exceptions)

    return coerced_arguments
