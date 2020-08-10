import datetime

import pytest

from tartiflette import TartifletteError
from tartiflette.scalar.builtins.date import ScalarDate


@pytest.mark.parametrize(
    "value,should_raise_exception,expected",
    [
        (None, True, "Date cannot represent value: < None >."),
        (True, True, "Date cannot represent value: < True >."),
        (False, True, "Date cannot represent value: < False >."),
        ("", True, "Date cannot represent value: <  >."),
        (0, True, "Date cannot represent value: < 0 >."),
        (1, True, "Date cannot represent value: < 1 >."),
        (3, True, "Date cannot represent value: < 3 >."),
        (0.0, True, "Date cannot represent value: < 0.0 >."),
        (1.0, True, "Date cannot represent value: < 1.0 >."),
        (3.0, True, "Date cannot represent value: < 3.0 >."),
        (0.1, True, "Date cannot represent value: < 0.1 >."),
        (1.1, True, "Date cannot represent value: < 1.1 >."),
        (3.1, True, "Date cannot represent value: < 3.1 >."),
        ("0", True, "Date cannot represent value: < 0 >."),
        ("1", True, "Date cannot represent value: < 1 >."),
        ("3", True, "Date cannot represent value: < 3 >."),
        ("0.0", True, "Date cannot represent value: < 0.0 >."),
        ("1.0", True, "Date cannot represent value: < 1.0 >."),
        ("3.0", True, "Date cannot represent value: < 3.0 >."),
        ("0.1", True, "Date cannot represent value: < 0.1 >."),
        ("1.1", True, "Date cannot represent value: < 1.1 >."),
        ("3.1", True, "Date cannot represent value: < 3.1 >."),
        ("0e0", True, "Date cannot represent value: < 0e0 >."),
        ("1e0", True, "Date cannot represent value: < 1e0 >."),
        ("3e0", True, "Date cannot represent value: < 3e0 >."),
        ("0e1", True, "Date cannot represent value: < 0e1 >."),
        ("1e1", True, "Date cannot represent value: < 1e1 >."),
        ("3e1", True, "Date cannot represent value: < 3e1 >."),
        ("0.1e1", True, "Date cannot represent value: < 0.1e1 >."),
        ("1.1e1", True, "Date cannot represent value: < 1.1e1 >."),
        ("3.1e1", True, "Date cannot represent value: < 3.1e1 >."),
        ("0.11e1", True, "Date cannot represent value: < 0.11e1 >."),
        ("1.11e1", True, "Date cannot represent value: < 1.11e1 >."),
        ("3.11e1", True, "Date cannot represent value: < 3.11e1 >."),
        (float("inf"), True, "Date cannot represent value: < inf >."),
        ("A", True, "Date cannot represent value: < A >."),
        ("{}", True, "Date cannot represent value: < {} >."),
        ({}, True, "Date cannot represent value: < {} >."),
        (Exception("LOL"), True, "Date cannot represent value: < LOL >."),
        (
            Exception,
            True,
            "Date cannot represent value: < <class 'Exception'> >.",
        ),
        ("1986-12-24", True, "Date cannot represent value: < 1986-12-24 >."),
        (datetime.datetime(1986, 12, 24, 15, 0, 0), False, "1986-12-24"),
    ],
)
def test_scalar_date_coerce_output(value, should_raise_exception, expected):
    if should_raise_exception:
        with pytest.raises(TartifletteError, match=expected):
            ScalarDate().coerce_output(value)
    else:
        assert ScalarDate().coerce_output(value) == expected


@pytest.mark.parametrize(
    "value,should_raise_exception,expected",
    [
        (None, True, "Date cannot represent value: < None >."),
        (True, True, "Date cannot represent value: < True >."),
        (False, True, "Date cannot represent value: < False >."),
        ("", True, "Date cannot represent value: <  >."),
        (0, True, "Date cannot represent value: < 0 >."),
        (1, True, "Date cannot represent value: < 1 >."),
        (3, True, "Date cannot represent value: < 3 >."),
        (0.0, True, "Date cannot represent value: < 0.0 >."),
        (1.0, True, "Date cannot represent value: < 1.0 >."),
        (3.0, True, "Date cannot represent value: < 3.0 >."),
        (0.1, True, "Date cannot represent value: < 0.1 >."),
        (1.1, True, "Date cannot represent value: < 1.1 >."),
        (3.1, True, "Date cannot represent value: < 3.1 >."),
        ("0", True, "Date cannot represent value: < 0 >."),
        ("1", True, "Date cannot represent value: < 1 >."),
        ("3", True, "Date cannot represent value: < 3 >."),
        ("0.0", True, "Date cannot represent value: < 0.0 >."),
        ("1.0", True, "Date cannot represent value: < 1.0 >."),
        ("3.0", True, "Date cannot represent value: < 3.0 >."),
        ("0.1", True, "Date cannot represent value: < 0.1 >."),
        ("1.1", True, "Date cannot represent value: < 1.1 >."),
        ("3.1", True, "Date cannot represent value: < 3.1 >."),
        ("0e0", True, "Date cannot represent value: < 0e0 >."),
        ("1e0", True, "Date cannot represent value: < 1e0 >."),
        ("3e0", True, "Date cannot represent value: < 3e0 >."),
        ("0e1", True, "Date cannot represent value: < 0e1 >."),
        ("1e1", True, "Date cannot represent value: < 1e1 >."),
        ("3e1", True, "Date cannot represent value: < 3e1 >."),
        ("0.1e1", True, "Date cannot represent value: < 0.1e1 >."),
        ("1.1e1", True, "Date cannot represent value: < 1.1e1 >."),
        ("3.1e1", True, "Date cannot represent value: < 3.1e1 >."),
        ("0.11e1", True, "Date cannot represent value: < 0.11e1 >."),
        ("1.11e1", True, "Date cannot represent value: < 1.11e1 >."),
        ("3.11e1", True, "Date cannot represent value: < 3.11e1 >."),
        (float("inf"), True, "Date cannot represent value: < inf >."),
        ("A", True, "Date cannot represent value: < A >."),
        ("{}", True, "Date cannot represent value: < {} >."),
        ({}, True, "Date cannot represent value: < {} >."),
        (Exception("LOL"), True, "Date cannot represent value: < LOL >."),
        (
            Exception,
            True,
            "Date cannot represent value: < <class 'Exception'> >.",
        ),
        ("1986-12-24", False, datetime.datetime(1986, 12, 24, 0, 0, 0)),
        (
            datetime.datetime(1986, 12, 24, 15, 0, 0),
            True,
            "Date cannot represent value: < 1986-12-24 15:00:00 >.",
        ),
    ],
)
def test_scalar_date_coerce_input(value, should_raise_exception, expected):
    if should_raise_exception:
        with pytest.raises(TartifletteError, match=expected):
            ScalarDate().coerce_input(value)
    else:
        assert ScalarDate().coerce_input(value) == expected
