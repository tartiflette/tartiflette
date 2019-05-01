from typing import Any, Union

from tartiflette.language.ast import BooleanValueNode
from tartiflette.utils.value_from_ast import UndefinedValue


class ScalarBoolean:
    @staticmethod
    def coerce_output(val: Any) -> bool:
        return bool(val)

    @staticmethod
    def coerce_input(val: Any) -> bool:
        if not isinstance(val, bool):
            raise TypeError(
                f"Boolean cannot represent a non boolean value: < {val} >"
            )
        return val

    @staticmethod
    def parse_literal(ast: "Node") -> Union[bool, "UndefinedValue"]:
        return (
            ast.value if isinstance(ast, BooleanValueNode) else UndefinedValue
        )
