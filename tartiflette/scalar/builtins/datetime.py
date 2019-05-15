from datetime import datetime

from tartiflette import Scalar


class ScalarDateTime:
    def __init__(self, _config):
        pass

    def coerce_output(self, val: datetime) -> str:
        return val.isoformat()

    def coerce_input(self, val: str) -> datetime:
        return datetime.strptime(val, "%Y-%m-%dT%H:%M:%S")


def bake(schema_name, config):
    sdl = "scalar DateTime"

    Scalar("DateTime", schema_name=schema_name)(ScalarDateTime(config))

    return sdl
