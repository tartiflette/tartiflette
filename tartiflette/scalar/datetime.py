from datetime import datetime
from typing import Union

from tartiflette.language.ast import StringValueNode
from tartiflette.utils.value_from_ast import UndefinedValue


class ScalarDateTime:
    @staticmethod
    def coerce_output(val: datetime) -> str:
        return val.isoformat()

    @staticmethod
    def coerce_input(val: str) -> datetime:
        return datetime.strptime(val, "%Y-%m-%dT%H:%M:%S")

    @staticmethod
    def parse_literal(ast: "Node") -> Union[datetime, "UndefinedValue"]:
        if not isinstance(ast, StringValueNode):
            return UndefinedValue

        try:
            return datetime.strptime(ast.value, "%Y-%m-%dT%H:%M:%S")
        except Exception:
            pass
        return UndefinedValue
