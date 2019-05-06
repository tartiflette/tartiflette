from tartiflette.types.exceptions.tartiflette import (
    SkipCollection,
    SkipExecution,
)

from .common import CommonDirective


def _include_collection(directive_args, selection):
    if not directive_args["if"]:
        raise SkipCollection()
    return selection


class Include(CommonDirective):
    @staticmethod
    async def on_field_execution(
        directive_args, next_resolver, parent_result, args, ctx, info
    ):
        if not directive_args["if"]:
            raise SkipExecution()

        return await next_resolver(parent_result, args, ctx, info)

    @staticmethod
    async def on_field_collection(directive_args, next, selection):
        return _include_collection(directive_args, await next(selection))

    @staticmethod
    async def on_fragment_spread_collection(directive_args, next, selection):
        return _include_collection(directive_args, await next(selection))

    @staticmethod
    async def on_inline_fragment_collection(directive_args, next, selection):
        return _include_collection(directive_args, await next(selection))
