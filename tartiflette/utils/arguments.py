import asyncio

from functools import partial
from typing import Any, Callable, Dict, List, Optional

UNDEFINED_VALUE = object()


async def _coerce_argument(
    argument_definition: "GraphQLArgument",
    args: Dict[str, Any],
    ctx: Optional[Dict[str, Any]],
    info: "Info",
) -> Any:
    # pylint: disable=unused-argument
    try:
        return args[argument_definition.name].value
    except KeyError:
        pass

    if argument_definition.default_value:
        return argument_definition.default_value
    return UNDEFINED_VALUE


def _surround_with_argument_execution_directives(
    func: Callable, directives: List[Dict[str, Any]]
) -> Callable:
    for directive in reversed(directives):
        func = partial(
            directive["callables"].on_argument_execution,
            directive["args"],
            func,
        )
    return func


async def coerce_arguments(
    argument_definitions: Dict[str, "GraphQLArgument"],
    input_args: Dict[str, Any],
    ctx: Optional[Dict[str, Any]],
    info: "Info",
) -> Dict[str, Any]:
    results = await asyncio.gather(
        *[
            # TODO: surround argument with directives at bake time
            _surround_with_argument_execution_directives(
                _coerce_argument, argument_definition.directives
            )(argument_definition, input_args, ctx, info)
            for argument_definition in argument_definitions.values()
        ]
    )

    return {
        argument_name: result
        for argument_name, result in zip(argument_definitions, results)
        if result is not UNDEFINED_VALUE
    }
