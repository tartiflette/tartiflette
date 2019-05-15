from typing import Any

from tartiflette import Scalar


class ScalarBoolean:
    def __init__(self, _config):
        pass

    def coerce_output(self, val: Any) -> bool:
        return bool(val)

    def coerce_input(self, val: Any) -> bool:
        return bool(val)


def bake(schema_name, config):
    sdl = "scalar Boolean"

    Scalar(name="Boolean", schema_name=schema_name)(ScalarBoolean(config))

    return sdl
