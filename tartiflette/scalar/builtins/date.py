from datetime import datetime

from tartiflette import Scalar


class ScalarDate:

    # pylint: disable=no-self-use
    def coerce_output(self, val: datetime) -> str:
        return val.isoformat().split("T")[0]

    # pylint: disable=no-self-use
    def coerce_input(self, val: str) -> datetime:
        return datetime.strptime(val, "%Y-%m-%d")


def bake(schema_name, _config):
    sdl = "scalar Date"

    Scalar("Date", schema_name=schema_name)(ScalarDate())

    return sdl
