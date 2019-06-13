from typing import Any, Callable, Dict, Optional

from tartiflette import Directive


class NonIntrospectable:
    async def on_introspection(
        self,
        _directive_args: Dict[str, Any],
        _next_directive: Callable,
        _introspected_element: Any,
        _ctx: Optional[Dict[str, Any]],
        _info: "Info",
    ) -> None:
        return None


class NonIntrospectableDeprecated:
    async def on_introspection(
        self,
        _directive_args: Dict[str, Any],
        _next_directive: Callable,
        _introspected_element: Any,
        _ctx: Optional[Dict[str, Any]],
        _info: "Info",
    ) -> None:
        print(
            "@non_introspectable is deprecated, please use @nonIntrospectable, will be removed in 0.12.0"
        )
        return None


def bake(schema_name, _config):
    sdl = """
    directive @nonIntrospectable on FIELD_DEFINITION
    directive @non_introspectable on FIELD_DEFINITION
    """

    Directive(name="nonIntrospectable", schema_name=schema_name)(
        NonIntrospectable()
    )
    Directive(name="non_introspectable", schema_name=schema_name)(
        NonIntrospectableDeprecated()
    )

    return sdl
