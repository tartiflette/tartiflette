import asyncio

from functools import partial
from typing import Any, Callable, Dict, List, Optional, Union

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.types.exceptions.tartiflette import (
    GraphQLError,
    MultipleException,
)
from tartiflette.types.helpers import reduce_type
from tartiflette.types.input_object import GraphQLInputObjectType
from tartiflette.utils.errors import to_graphql_error


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


async def argument_coercer(
    argument_definition, args, ctx, info, input_coercer=None
):
    value = UNDEFINED_VALUE
    try:
        value = args[argument_definition.name]
    except KeyError:
        pass

    if value is UNDEFINED_VALUE:
        return value

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
    values: Dict[str, Any],
    ctx: Optional[Dict[str, Any]],
    info: "Info",
) -> Dict[str, Any]:
    results = await asyncio.gather(
        *[
            argument_definition.coercer(values, ctx, info)
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
