from datetime import datetime
from typing import Union

from tartiflette.language.ast import StringValueNode
from tartiflette.utils.value_from_ast import UndefinedValue


class ScalarTime:
    @staticmethod
    def coerce_output(val: datetime) -> str:
        return val.isoformat().split("T")[1]

    @staticmethod
    def coerce_input(val: str) -> datetime:
        return datetime.strptime(val, "%H:%M:%S")

    @staticmethod
    def parse_literal(ast: "Node") -> Union[datetime, "UndefinedValue"]:
        if not isinstance(ast, StringValueNode):
            return UndefinedValue

        try:
            return datetime.strptime(ast.value, "%H:%M:%S")
        except Exception:
            pass
        return UndefinedValue
