from typing import Any


class ObjectValue(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__ttftt_key: str = None
        self.__ttftt_parent: Any = None

    def set_key(self, key: str) -> None:
        self.__ttftt_key = key

    def set_value(self, value: Any) -> None:
        self[self.__ttftt_key] = value

    @property
    def parent(self) -> Any:
        return self.__ttftt_parent

    @parent.setter
    def parent(self, value: Any):
        self.__ttftt_parent = value
