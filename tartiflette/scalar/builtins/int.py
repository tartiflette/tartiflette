from typing import Any

from tartiflette import Scalar


class ScalarInt:
    def __init__(self, _config):
        pass

    def coerce_output(self, val: Any) -> int:
        return int(val)

    def coerce_input(self, val: Any) -> int:
        return int(val)


def bake(schema_name, config):
    sdl = "scalar Int"

    Scalar(name="Int", schema_name=schema_name)(ScalarInt(config))

    return sdl
