from typing import Any

from tartiflette.constants import UNDEFINED_VALUE

__all__ = ("is_invalid_value",)


def is_invalid_value(value: Any) -> bool:
    """
    Determines whether or not the value is invalid.
    :param value: value to check
    :type value: Any
    :return: whether or not the value is invalid
    :rtype: bool
    """
    return value is UNDEFINED_VALUE
