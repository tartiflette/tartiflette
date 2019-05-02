from datetime import datetime
from typing import Union

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode


class ScalarDateTime:
    @staticmethod
    def coerce_output(val: datetime) -> str:
        return val.isoformat()

    @staticmethod
    def coerce_input(val: str) -> datetime:
        return datetime.strptime(val, "%Y-%m-%dT%H:%M:%S")

    @staticmethod
    def parse_literal(ast: "Node") -> Union[datetime, "UNDEFINED_VALUE"]:
        if not isinstance(ast, StringValueNode):
            return UNDEFINED_VALUE

        try:
            return datetime.strptime(ast.value, "%Y-%m-%dT%H:%M:%S")
        except Exception:
            pass
        return UNDEFINED_VALUE
