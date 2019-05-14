from typing import Any, Callable, Dict, Optional

from .common import CommonDirective


class Deprecated(CommonDirective):
    @staticmethod
    async def on_introspection(
        directive_args: Dict[str, Any],
        next_directive: Callable,
        introspected_element: Any,
        ctx: Optional[Dict[str, Any]],
        info: "Info",
    ):

        introspected_element = await next_directive(
            introspected_element, ctx, info
        )

        setattr(introspected_element, "isDeprecated", True)
        setattr(
            introspected_element, "deprecationReason", directive_args["reason"]
        )

        return introspected_element
