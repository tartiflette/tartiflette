from functools import partial
from typing import Any, Callable, Dict, List


async def _default_directive_endpoint(val, *_args, **_kwargs):
    return val


def surround_with_directive(
    func: Callable, directives: List[Dict[str, Any]], directive_func: str
) -> Callable:

    if not func:
        func = _default_directive_endpoint

    for directive in reversed(directives):
        func = partial(
            directive["callables"][directive_func], directive["args"], func
        )
    return func
