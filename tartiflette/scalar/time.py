from datetime import datetime
from typing import Union

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode


class ScalarTime:
    @staticmethod
    def coerce_output(val: datetime) -> str:
        return val.isoformat().split("T")[1]

    @staticmethod
    def coerce_input(val: str) -> datetime:
        return datetime.strptime(val, "%H:%M:%S")

    @staticmethod
    def parse_literal(ast: "Node") -> Union[datetime, "UNDEFINED_VALUE"]:
        if not isinstance(ast, StringValueNode):
            return UNDEFINED_VALUE

        try:
            return datetime.strptime(ast.value, "%H:%M:%S")
        except Exception:
            pass
        return UNDEFINED_VALUE
