from typing import Any

from tartiflette import Scalar


class ScalarInt:
    def coerce_output(self, val: Any) -> int:
        return int(val)

    def coerce_input(self, val: Any) -> int:
        return int(val)


def bake(schema_name, _config):
    sdl = "scalar Int"

    Scalar(name="Int", schema_name=schema_name)(ScalarInt())

    return sdl
