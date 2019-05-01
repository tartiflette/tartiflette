from typing import Any, Union

from tartiflette.language.ast import StringValueNode
from tartiflette.utils.value_from_ast import UndefinedValue


class ScalarString:
    @staticmethod
    def coerce_output(val: Any) -> str:
        return str(val)

    @staticmethod
    def coerce_input(val: Any) -> str:
        if not isinstance(val, str):
            raise TypeError(
                f"String cannot represent a non string value: < {val} >"
            )
        return val

    @staticmethod
    def parse_literal(ast: "Node") -> Union[str, "UndefinedValue"]:
        return (
            ast.value if isinstance(ast, StringValueNode) else UndefinedValue
        )
