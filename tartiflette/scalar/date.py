from datetime import datetime
from typing import Union

from tartiflette.language.ast import StringValueNode
from tartiflette.utils.value_from_ast import UndefinedValue


class ScalarDate:
    @staticmethod
    def coerce_output(val: datetime) -> str:
        return val.isoformat().split("T")[0]

    @staticmethod
    def coerce_input(val: str) -> datetime:
        return datetime.strptime(val, "%Y-%m-%d")

    @staticmethod
    def parse_literal(ast: "Node") -> Union[datetime, "UndefinedValue"]:
        if not isinstance(ast, StringValueNode):
            return UndefinedValue

        try:
            return datetime.strptime(ast.value, "%Y-%m-%d")
        except Exception:
            pass
        return UndefinedValue
