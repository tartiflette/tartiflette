from typing import Any, Union

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import IntValueNode

_MAX_INT = 2_147_483_647
_MIN_INT = -2_147_483_648


class ScalarInt:
    @staticmethod
    def coerce_output(val: Any) -> int:
        return int(val)

    @staticmethod
    def coerce_input(val: Any) -> int:
        # ¯\_(ツ)_/¯ booleans are int: `assert isinstance(True, int) is True`
        if not isinstance(val, int) or isinstance(val, bool):
            raise TypeError(
                f"Int cannot represent non-integer value: < {val} >"
            )
        if not _MIN_INT <= val <= _MAX_INT:
            raise TypeError(
                "Int cannot represent non 32-bit signed integer value: "
                f"< {val} >"
            )
        return val

    @staticmethod
    def parse_literal(ast: "Node") -> Union[int, "UNDEFINED_VALUE"]:
        if not isinstance(ast, IntValueNode):
            return UNDEFINED_VALUE

        try:
            value = int(ast.value)
            if _MIN_INT <= value <= _MAX_INT:
                return value
        except Exception:
            pass
        return UNDEFINED_VALUE
