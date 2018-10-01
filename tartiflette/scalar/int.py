from typing import Any


class ScalarInt:
    @staticmethod
    def coerce_output(val: Any) -> int:
        return int(val)

    @staticmethod
    def coerce_input(val: Any) -> int:
        return int(val)
