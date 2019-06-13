from typing import Any

from tartiflette import Scalar


class ScalarString:
    # pylint: disable=no-self-use
    def coerce_output(self, val: Any) -> str:
        return str(val)

    # pylint: disable=no-self-use
    def coerce_input(self, val: Any) -> str:
        return str(val)


def bake(schema_name, _config):
    sdl = "scalar String"

    Scalar(name="String", schema_name=schema_name)(ScalarString())

    return sdl
