import time


class ScalarTime:
    @staticmethod
    def coerce_output(val: time.struct_time) -> str:
        return "%s:%s:%s" % (val.tm_hour, val.tm_min, val.tm_sec)

    @staticmethod
    def coerce_input(val: str) -> time.struct_time:
        return time.strptime(val, "%H:%M:%S.%f")
