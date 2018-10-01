class OnBuildDirective:
    @staticmethod
    def on_build(_schema):
        pass


class OnExecutionDirective:
    @staticmethod
    async def on_execution(
        _directive_args, next_resolver, parent, args, request_context, info
    ):
        return await next_resolver(parent, args, request_context, info)


class OnIntrospectionDirective:
    @staticmethod
    def on_introspection(
        _directive_args, next_directive, introspected_element
    ):
        return next_directive(introspected_element)


class CommonDirective(
    OnBuildDirective, OnExecutionDirective, OnIntrospectionDirective
):
    pass
