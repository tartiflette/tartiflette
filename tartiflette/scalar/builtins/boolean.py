from typing import Any

from tartiflette import Scalar


class ScalarBoolean:

    # pylint: disable=no-self-use
    def coerce_output(self, val: Any) -> bool:
        return bool(val)

    # pylint: disable=no-self-use
    def coerce_input(self, val: Any) -> bool:
        return bool(val)


def bake(schema_name, _config):
    sdl = "scalar Boolean"

    Scalar(name="Boolean", schema_name=schema_name)(ScalarBoolean())

    return sdl
