from typing import Any, Callable, Dict

from .common import CommonDirective


class Deprecated(CommonDirective):
    @staticmethod
    def on_introspection(
        directive_args: Dict[str, Any],
        next_directive: Callable,
        introspected_element: Any,
    ):
        introspected_element = next_directive(introspected_element)
        setattr(introspected_element, "isDeprecated", True)
        setattr(
            introspected_element, "deprecationReason", directive_args["reason"]
        )
        return introspected_element
