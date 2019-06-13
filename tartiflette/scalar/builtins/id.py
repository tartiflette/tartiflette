from tartiflette import Scalar

from .string import ScalarString


class ScalarId(ScalarString):
    # TODO :-), with @relay I think.
    pass


def bake(schema_name, _config):
    sdl = "scalar ID"

    Scalar(name="ID", schema_name=schema_name)(ScalarId())

    return sdl
