from typing import Any, Callable, Dict, Optional

from .common import CommonDirective


class NonIntrospectable(CommonDirective):
    @staticmethod
    async def on_introspection(
        _directive_args: Dict[str, Any],
        _next_directive: Callable,
        _introspected_element: Any,
        _ctx: Optional[Dict[str, Any]],
        _info: "Info",
    ) -> None:
        return None
