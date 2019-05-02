from math import isfinite
from typing import Any, Union

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import FloatValueNode, IntValueNode


class ScalarFloat:
    @staticmethod
    def coerce_output(val: Any) -> float:
        return float(val)

    @staticmethod
    def coerce_input(val: Any) -> float:
        # ¯\_(ツ)_/¯ booleans are int: `assert isinstance(True, int) is True`
        if isinstance(val, bool) or not (
            isinstance(val, int) or (isinstance(val, float) and isfinite(val))
        ):
            raise TypeError(
                f"Float cannot represent non numeric value: < {val} >"
            )
        return float(val)

    @staticmethod
    def parse_literal(ast: "Node") -> Union[float, "UNDEFINED_VALUE"]:
        if not isinstance(ast, (FloatValueNode, IntValueNode)):
            return UNDEFINED_VALUE

        try:
            return float(ast.value)
        except Exception:
            pass
        return UNDEFINED_VALUE
