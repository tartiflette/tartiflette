from functools import partial
from typing import Any, Callable, Dict, List


async def _default_directive_endpoint(val, *_args, **_kwargs):
    return val


def wraps_with_directives(
    directives_definition: List[Dict[str, Any]],
    directive_hook: str,
    func: Callable = None,
) -> Callable:

    if func is None:
        func = _default_directive_endpoint

    for directive in reversed(directives_definition):
        func = partial(
            directive["callables"][directive_hook], directive["args"], func
        )
    return func
