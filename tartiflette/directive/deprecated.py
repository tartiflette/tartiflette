class Deprecated:
    @staticmethod
    def on_build(schema):
        pass

    @staticmethod
    async def on_execution(resolver, parent, arguments, request_ctx, info):
        return await resolver(parent, arguments, request_ctx, info)

    @staticmethod
    async def on_introspection(resolver, parent, arguments, request_ctx, info):
        pass
        # TODO Implement later
