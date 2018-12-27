from datetime import datetime


class ScalarDateTime:
    @staticmethod
    def coerce_output(val: datetime) -> str:
        return val.isoformat()

    @staticmethod
    def coerce_input(val: str) -> datetime:
        return datetime.strptime(val, "%Y-%m-%dT%H:%M:%S")
