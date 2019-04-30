from functools import partial
from typing import Any, Callable, Dict, List


def surround_with_directive(
    func: Callable, directives: List[Dict[str, Any]], directive_func: str
) -> Callable:
    for directive in reversed(directives):
        func = partial(
            directive["callables"][directive_func], directive["args"], func
        )
    return func
