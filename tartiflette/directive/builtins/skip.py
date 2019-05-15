from tartiflette import Directive
from tartiflette.types.exceptions.tartiflette import SkipExecution


class Skip:
    def __init__(self, _config):
        pass

    async def on_field_execution(
        self, directive_args, next_resolver, parent_result, args, ctx, info
    ):
        if directive_args["if"]:
            raise SkipExecution()

        return await next_resolver(parent_result, args, ctx, info)


def bake(schema_name, config):
    sdl = "directive @skip(if: Boolean!) on FIELD | FRAGMENT_SPREAD | INLINE_FRAGMENT"

    Directive(name="skip", schema_name=schema_name)(Skip(config))

    return sdl
