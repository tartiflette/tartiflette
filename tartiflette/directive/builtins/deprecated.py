from typing import Any, Callable, Dict, Optional

from tartiflette import Directive


class Deprecated:
    async def on_introspection(
        self,
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


def bake(schema_name, _config):
    sdl = """
    directive @deprecated(
        reason: String = "Deprecated"
    ) on FIELD_DEFINITION | ENUM_VALUE
    """

    Directive("deprecated", schema_name=schema_name)(Deprecated())

    return sdl
