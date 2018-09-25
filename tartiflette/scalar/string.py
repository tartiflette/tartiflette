from typing import Any


class ScalarString:
    @staticmethod
    def coerce_output(val: Any) -> str:
        return str(val)

    @staticmethod
    def coerce_input(val: Any) -> str:
        return str(val)
