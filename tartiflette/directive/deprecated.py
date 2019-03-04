from typing import Any, Callable, Dict, Optional

from .common import CommonDirective


class Deprecated(CommonDirective):
    @staticmethod
    def on_introspection(
        directive_args: Dict[str, Any],
        next_directive: Callable,
        introspected_element: Any,
        _ctx: Optional[Dict[str, Any]],
        _info: "Info",
    ):
        introspected_element = next_directive(introspected_element)
        setattr(introspected_element, "isDeprecated", True)
        setattr(
            introspected_element, "deprecationReason", directive_args["reason"]
        )
        return introspected_element
