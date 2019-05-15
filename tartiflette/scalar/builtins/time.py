from datetime import datetime

from tartiflette import Scalar


class ScalarTime:
    def __init__(self, _config):
        pass

    def coerce_output(self, val: datetime) -> str:
        return val.isoformat().split("T")[1]

    def coerce_input(self, val: str) -> datetime:
        return datetime.strptime(val, "%H:%M:%S")


def bake(schema_name, config):
    sdl = "scalar Time"

    Scalar("Time", schema_name=schema_name)(ScalarTime(config))

    return sdl
