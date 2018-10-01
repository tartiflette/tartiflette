from datetime import datetime


class ScalarDate:
    @staticmethod
    def coerce_output(val: datetime) -> str:
        return val.isoformat().split("T")[0]

    @staticmethod
    def coerce_input(val: str) -> datetime:
        return datetime.strptime(val, "%Y-%m-%d")
