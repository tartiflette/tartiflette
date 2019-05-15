from datetime import datetime

from tartiflette import Scalar


class ScalarDate:
    def __init__(self, _config):
        pass

    def coerce_output(self, val: datetime) -> str:
        return val.isoformat().split("T")[0]

    def coerce_input(self, val: str) -> datetime:
        return datetime.strptime(val, "%Y-%m-%d")


def bake(schema_name, config):
    sdl = "scalar Date"

    Scalar("Date", schema_name=schema_name)(ScalarDate(config))

    return sdl
