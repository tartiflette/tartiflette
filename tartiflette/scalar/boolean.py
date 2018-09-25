from typing import Any


class ScalarBoolean:
    @staticmethod
    def coerce_output(val: Any) -> bool:
        return bool(val)

    @staticmethod
    def coerce_input(val: Any) -> bool:
        return bool(val)
