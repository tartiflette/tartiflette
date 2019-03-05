from typing import Any, Callable, Dict, Optional


class OnBuildDirective:
    @staticmethod
    def on_build(_schema: "GraphQLSchema") -> None:
        pass


class OnExecutionDirective:
    @staticmethod
    async def on_field_execution(
        _directive_args: Dict[str, Any],
        next_resolver: Callable,
        parent_result: Optional[Any],
        args: Dict[str, Any],
        ctx: Optional[Dict[str, Any]],
        info: "Info",
    ) -> Any:
        return await next_resolver(parent_result, args, ctx, info)

    @staticmethod
    async def on_argument_execution(
        _directive_args: Dict[str, Any],
        next_directive: Callable,
        argument_definition: "GraphQLArgument",
        args: Dict[str, Any],
        ctx: Optional[Dict[str, Any]],
        info: "Info",
    ) -> Any:
        return await next_directive(argument_definition, args, ctx, info)


class OnIntrospectionDirective:
    @staticmethod
    def on_introspection(
        _directive_args: Dict[str, Any],
        next_directive: Callable,
        introspected_element: Any,
        _ctx: Optional[Dict[str, Any]],
        _info: "Info",
    ) -> Any:
        return next_directive(introspected_element)


class CommonDirective(
    OnBuildDirective, OnExecutionDirective, OnIntrospectionDirective
):
    pass
