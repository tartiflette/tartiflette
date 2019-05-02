import pytest

from tartiflette.constants import INVALID_VALUE, UNDEFINED_VALUE
from tartiflette.utils.values import (
    is_invalid_value,
    is_undefined_value,
    is_usable_value,
)


@pytest.mark.parametrize(
    "value,expected",
    [
        (INVALID_VALUE, True),
        (UNDEFINED_VALUE, False),
        (True, False),
        ("aValue", False),
        (10, False),
    ],
)
def test_is_invalid_value(value, expected):
    assert is_invalid_value(value) is expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (UNDEFINED_VALUE, True),
        (INVALID_VALUE, False),
        (True, False),
        ("aValue", False),
        (10, False),
    ],
)
def test_is_undefined_value(value, expected):
    assert is_undefined_value(value) is expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (INVALID_VALUE, False),
        (UNDEFINED_VALUE, False),
        (True, True),
        ("aValue", True),
        (10, True),
    ],
)
def test_is_usable_value(value, expected):
    assert is_usable_value(value) is expected
