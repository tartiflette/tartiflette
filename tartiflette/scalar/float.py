from typing import Any


class ScalarFloat:
    @staticmethod
    def coerce_output(val: Any) -> float:
        return float(val)

    @staticmethod
    def coerce_input(val: Any) -> float:
        return float(val)
