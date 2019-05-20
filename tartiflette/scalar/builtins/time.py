from datetime import datetime

from tartiflette import Scalar


class ScalarTime:

    # pylint: disable=no-self-use
    def coerce_output(self, val: datetime) -> str:
        return val.isoformat().split("T")[1]

    # pylint: disable=no-self-use
    def coerce_input(self, val: str) -> datetime:
        return datetime.strptime(val, "%H:%M:%S")


def bake(schema_name, _config):
    sdl = "scalar Time"

    Scalar("Time", schema_name=schema_name)(ScalarTime())

    return sdl
