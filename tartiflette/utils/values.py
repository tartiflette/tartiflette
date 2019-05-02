from typing import Any

from tartiflette.constants import INVALID_VALUE, UNDEFINED_VALUE

__all__ = ["is_invalid_value", "is_undefined_value", "is_usable_value"]


def is_invalid_value(value: Any) -> bool:
    """
    Determines whether or not the value is invalid.
    :param value: value to check
    :type value: Any
    :return: whether or not the value is invalid
    :rtype: bool
    """
    # return value is INVALID_VALUE
    return value is UNDEFINED_VALUE


def is_undefined_value(value: Any) -> bool:
    """
    Determines whether or not the value is undefined.
    :param value: value to check
    :type value: Any
    :return: whether or not the value is undefined
    :rtype: bool
    """
    return value is UNDEFINED_VALUE


def is_usable_value(value: Any) -> bool:
    """
    Determines whether or not the value is usable.
    :param value: value to check
    :type value: Any
    :return: whether or not the value is usable
    :rtype: bool
    """
    return not is_invalid_value(value) and not is_undefined_value(value)
