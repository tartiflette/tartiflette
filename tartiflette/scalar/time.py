from datetime import datetime


class ScalarTime:
    @staticmethod
    def coerce_output(val: datetime) -> str:
        return val.isoformat().split("T")[1]

    @staticmethod
    def coerce_input(val: str) -> datetime:
        return datetime.strptime(val, "%H:%M:%S")
