from typing import Any, Callable, Dict

from .common import CommonDirective


class NonIntrospectable(CommonDirective):
    @staticmethod
    def on_introspection(
        _directive_args: Dict[str, Any],
        _next_directive: Callable,
        _introspected_element: Any,
    ) -> None:
        return None
