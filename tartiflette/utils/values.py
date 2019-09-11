from math import floor, isfinite
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


def is_integer(value: Any) -> bool:
    """
    Determines whether or not the value is an integer or a valid equivalent.
    :param value: value to check
    :type value: Any
    :return: whether or not the value is an integer or a valid equivalent
    :rtype: bool
    """
    try:
        if isinstance(value, bool):
            return False

        return isinstance(value, int) or (
            isfinite(value) and floor(value) == value
        )
    except Exception:  # pylint: disable=broad-except
        pass
    return False
