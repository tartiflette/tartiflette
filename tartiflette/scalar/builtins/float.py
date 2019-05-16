from typing import Any

from tartiflette import Scalar


class ScalarFloat:
    def coerce_output(self, val: Any) -> float:
        return float(val)

    def coerce_input(self, val: Any) -> float:
        return float(val)


def bake(schema_name, _config):
    sdl = "scalar Float"

    Scalar(name="Float", schema_name=schema_name)(ScalarFloat())

    return sdl
