from typing import Any

from tartiflette import Scalar


class ScalarString:
    def __init__(self, _config):
        pass

    def coerce_output(self, val: Any) -> str:
        return str(val)

    def coerce_input(self, val: Any) -> str:
        return str(val)


def bake(schema_name, config):
    sdl = "scalar String"

    Scalar(name="String", schema_name=schema_name)(ScalarString(config))

    return sdl
