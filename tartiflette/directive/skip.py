from tartiflette.types.exceptions.tartiflette import SkipExecution

from .common import CommonDirective


class Skip(CommonDirective):
    @staticmethod
    async def on_field_execution(
        directive_args, next_resolver, parent_result, args, ctx, info
    ):
        if directive_args["if"]:
            raise SkipExecution()

        return await next_resolver(parent_result, args, ctx, info)
