import datetime

import pytest

from tartiflette import TartifletteError
from tartiflette.scalar.builtins.time import ScalarTime


@pytest.mark.parametrize(
    "value,should_raise_exception,expected",
    [
        (None, True, "Time cannot represent value: < None >."),
        (True, True, "Time cannot represent value: < True >."),
        (False, True, "Time cannot represent value: < False >."),
        ("", True, "Time cannot represent value: <  >."),
        (0, True, "Time cannot represent value: < 0 >."),
        (1, True, "Time cannot represent value: < 1 >."),
        (3, True, "Time cannot represent value: < 3 >."),
        (0.0, True, "Time cannot represent value: < 0.0 >."),
        (1.0, True, "Time cannot represent value: < 1.0 >."),
        (3.0, True, "Time cannot represent value: < 3.0 >."),
        (0.1, True, "Time cannot represent value: < 0.1 >."),
        (1.1, True, "Time cannot represent value: < 1.1 >."),
        (3.1, True, "Time cannot represent value: < 3.1 >."),
        ("0", True, "Time cannot represent value: < 0 >."),
        ("1", True, "Time cannot represent value: < 1 >."),
        ("3", True, "Time cannot represent value: < 3 >."),
        ("0.0", True, "Time cannot represent value: < 0.0 >."),
        ("1.0", True, "Time cannot represent value: < 1.0 >."),
        ("3.0", True, "Time cannot represent value: < 3.0 >."),
        ("0.1", True, "Time cannot represent value: < 0.1 >."),
        ("1.1", True, "Time cannot represent value: < 1.1 >."),
        ("3.1", True, "Time cannot represent value: < 3.1 >."),
        ("0e0", True, "Time cannot represent value: < 0e0 >."),
        ("1e0", True, "Time cannot represent value: < 1e0 >."),
        ("3e0", True, "Time cannot represent value: < 3e0 >."),
        ("0e1", True, "Time cannot represent value: < 0e1 >."),
        ("1e1", True, "Time cannot represent value: < 1e1 >."),
        ("3e1", True, "Time cannot represent value: < 3e1 >."),
        ("0.1e1", True, "Time cannot represent value: < 0.1e1 >."),
        ("1.1e1", True, "Time cannot represent value: < 1.1e1 >."),
        ("3.1e1", True, "Time cannot represent value: < 3.1e1 >."),
        ("0.11e1", True, "Time cannot represent value: < 0.11e1 >."),
        ("1.11e1", True, "Time cannot represent value: < 1.11e1 >."),
        ("3.11e1", True, "Time cannot represent value: < 3.11e1 >."),
        (float("inf"), True, "Time cannot represent value: < inf >."),
        ("A", True, "Time cannot represent value: < A >."),
        ("{}", True, "Time cannot represent value: < {} >."),
        ({}, True, "Time cannot represent value: < {} >."),
        (Exception("LOL"), True, "Time cannot represent value: < LOL >."),
        (
            Exception,
            True,
            "Time cannot represent value: < <class 'Exception'> >.",
        ),
        ("15:52:52", True, "Time cannot represent value: < 15:52:52 >."),
        (datetime.datetime(1970, 11, 10, 15, 52, 52), False, "15:52:52"),
    ],
)
def test_scalar_time_coerce_output(value, should_raise_exception, expected):
    if should_raise_exception:
        with pytest.raises(TartifletteError, match=expected):
            ScalarTime().coerce_output(value)
    else:
        assert ScalarTime().coerce_output(value) == expected


@pytest.mark.parametrize(
    "value,should_raise_exception,expected",
    [
        (None, True, "Time cannot represent value: < None >."),
        (True, True, "Time cannot represent value: < True >."),
        (False, True, "Time cannot represent value: < False >."),
        ("", True, "Time cannot represent value: <  >."),
        (0, True, "Time cannot represent value: < 0 >."),
        (1, True, "Time cannot represent value: < 1 >."),
        (3, True, "Time cannot represent value: < 3 >."),
        (0.0, True, "Time cannot represent value: < 0.0 >."),
        (1.0, True, "Time cannot represent value: < 1.0 >."),
        (3.0, True, "Time cannot represent value: < 3.0 >."),
        (0.1, True, "Time cannot represent value: < 0.1 >."),
        (1.1, True, "Time cannot represent value: < 1.1 >."),
        (3.1, True, "Time cannot represent value: < 3.1 >."),
        ("0", True, "Time cannot represent value: < 0 >."),
        ("1", True, "Time cannot represent value: < 1 >."),
        ("3", True, "Time cannot represent value: < 3 >."),
        ("0.0", True, "Time cannot represent value: < 0.0 >."),
        ("1.0", True, "Time cannot represent value: < 1.0 >."),
        ("3.0", True, "Time cannot represent value: < 3.0 >."),
        ("0.1", True, "Time cannot represent value: < 0.1 >."),
        ("1.1", True, "Time cannot represent value: < 1.1 >."),
        ("3.1", True, "Time cannot represent value: < 3.1 >."),
        ("0e0", True, "Time cannot represent value: < 0e0 >."),
        ("1e0", True, "Time cannot represent value: < 1e0 >."),
        ("3e0", True, "Time cannot represent value: < 3e0 >."),
        ("0e1", True, "Time cannot represent value: < 0e1 >."),
        ("1e1", True, "Time cannot represent value: < 1e1 >."),
        ("3e1", True, "Time cannot represent value: < 3e1 >."),
        ("0.1e1", True, "Time cannot represent value: < 0.1e1 >."),
        ("1.1e1", True, "Time cannot represent value: < 1.1e1 >."),
        ("3.1e1", True, "Time cannot represent value: < 3.1e1 >."),
        ("0.11e1", True, "Time cannot represent value: < 0.11e1 >."),
        ("1.11e1", True, "Time cannot represent value: < 1.11e1 >."),
        ("3.11e1", True, "Time cannot represent value: < 3.11e1 >."),
        (float("inf"), True, "Time cannot represent value: < inf >."),
        ("A", True, "Time cannot represent value: < A >."),
        ("{}", True, "Time cannot represent value: < {} >."),
        ({}, True, "Time cannot represent value: < {} >."),
        (Exception("LOL"), True, "Time cannot represent value: < LOL >."),
        (
            Exception,
            True,
            "Time cannot represent value: < <class 'Exception'> >.",
        ),
        ("15:52:52", False, datetime.datetime(1900, 1, 1, 15, 52, 52)),
        (
            datetime.datetime(1970, 11, 10, 15, 52, 52),
            True,
            "Time cannot represent value: < 1970-11-10 15:52:52 >.",
        ),
    ],
)
def test_scalar_time_coerce_input(value, should_raise_exception, expected):
    if should_raise_exception:
        with pytest.raises(TartifletteError, match=expected):
            ScalarTime().coerce_input(value)
    else:
        assert ScalarTime().coerce_input(value) == expected
