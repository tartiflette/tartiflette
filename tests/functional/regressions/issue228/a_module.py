from tartiflette import Directive, Resolver, Scalar

_SDL = """
scalar NinjaGo

directive @Blah on FIELD_DEFINITION

type Lol {
    ninja: NinjaGo @Blah
}
"""


class BlahDir:
    def __init__(self, config):
        self._blah_value = config["val"]

    async def on_field_execution(
        self, _dirargs, nextdirective, *args, **kwargs
    ):
        return await nextdirective(*args, **kwargs) + " " + self._blah_value


class NinjaGo:
    @staticmethod
    def coerce_output(val):
        return val + "GO !"

    @staticmethod
    def coerce_input(val):
        return val


async def resolver_of_lol_ninja(pr, *_args, **_kwargs):
    return pr["ninja"] + " Ninja"


def bake(schema_name, config):
    Directive("Blah", schema_name=schema_name)(BlahDir(config))
    Scalar("NinjaGo", schema_name=schema_name)(NinjaGo)
    Resolver("Lol.ninja", schema_name=schema_name)(resolver_of_lol_ninja)
    return _SDL
