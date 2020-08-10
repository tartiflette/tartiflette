import datetime

import pytest

from tartiflette import TartifletteError
from tartiflette.scalar.builtins.datetime import ScalarDateTime


@pytest.mark.parametrize(
    "value,should_raise_exception,expected",
    [
        (None, True, "DateTime cannot represent value: < None >."),
        (True, True, "DateTime cannot represent value: < True >."),
        (False, True, "DateTime cannot represent value: < False >."),
        ("", True, "DateTime cannot represent value: <  >."),
        (0, True, "DateTime cannot represent value: < 0 >."),
        (1, True, "DateTime cannot represent value: < 1 >."),
        (3, True, "DateTime cannot represent value: < 3 >."),
        (0.0, True, "DateTime cannot represent value: < 0.0 >."),
        (1.0, True, "DateTime cannot represent value: < 1.0 >."),
        (3.0, True, "DateTime cannot represent value: < 3.0 >."),
        (0.1, True, "DateTime cannot represent value: < 0.1 >."),
        (1.1, True, "DateTime cannot represent value: < 1.1 >."),
        (3.1, True, "DateTime cannot represent value: < 3.1 >."),
        ("0", True, "DateTime cannot represent value: < 0 >."),
        ("1", True, "DateTime cannot represent value: < 1 >."),
        ("3", True, "DateTime cannot represent value: < 3 >."),
        ("0.0", True, "DateTime cannot represent value: < 0.0 >."),
        ("1.0", True, "DateTime cannot represent value: < 1.0 >."),
        ("3.0", True, "DateTime cannot represent value: < 3.0 >."),
        ("0.1", True, "DateTime cannot represent value: < 0.1 >."),
        ("1.1", True, "DateTime cannot represent value: < 1.1 >."),
        ("3.1", True, "DateTime cannot represent value: < 3.1 >."),
        ("0e0", True, "DateTime cannot represent value: < 0e0 >."),
        ("1e0", True, "DateTime cannot represent value: < 1e0 >."),
        ("3e0", True, "DateTime cannot represent value: < 3e0 >."),
        ("0e1", True, "DateTime cannot represent value: < 0e1 >."),
        ("1e1", True, "DateTime cannot represent value: < 1e1 >."),
        ("3e1", True, "DateTime cannot represent value: < 3e1 >."),
        ("0.1e1", True, "DateTime cannot represent value: < 0.1e1 >."),
        ("1.1e1", True, "DateTime cannot represent value: < 1.1e1 >."),
        ("3.1e1", True, "DateTime cannot represent value: < 3.1e1 >."),
        ("0.11e1", True, "DateTime cannot represent value: < 0.11e1 >."),
        ("1.11e1", True, "DateTime cannot represent value: < 1.11e1 >."),
        ("3.11e1", True, "DateTime cannot represent value: < 3.11e1 >."),
        (float("inf"), True, "DateTime cannot represent value: < inf >."),
        ("A", True, "DateTime cannot represent value: < A >."),
        ("{}", True, "DateTime cannot represent value: < {} >."),
        ({}, True, "DateTime cannot represent value: < {} >."),
        (Exception("LOL"), True, "DateTime cannot represent value: < LOL >."),
        (
            Exception,
            True,
            "DateTime cannot represent value: < <class 'Exception'> >.",
        ),
        (
            "1986-12-24T15:00:04",
            True,
            "DateTime cannot represent value: < 1986-12-24T15:00:04 >.",
        ),
        (
            datetime.datetime(1986, 12, 24, 15, 0, 4),
            False,
            "1986-12-24T15:00:04",
        ),
    ],
)
def test_scalar_datetime_coerce_output(
    value, should_raise_exception, expected
):
    if should_raise_exception:
        with pytest.raises(TartifletteError, match=expected):
            ScalarDateTime().coerce_output(value)
    else:
        assert ScalarDateTime().coerce_output(value) == expected


@pytest.mark.parametrize(
    "value,should_raise_exception,expected",
    [
        (None, True, "DateTime cannot represent value: < None >."),
        (True, True, "DateTime cannot represent value: < True >."),
        (False, True, "DateTime cannot represent value: < False >."),
        ("", True, "DateTime cannot represent value: <  >."),
        (0, True, "DateTime cannot represent value: < 0 >."),
        (1, True, "DateTime cannot represent value: < 1 >."),
        (3, True, "DateTime cannot represent value: < 3 >."),
        (0.0, True, "DateTime cannot represent value: < 0.0 >."),
        (1.0, True, "DateTime cannot represent value: < 1.0 >."),
        (3.0, True, "DateTime cannot represent value: < 3.0 >."),
        (0.1, True, "DateTime cannot represent value: < 0.1 >."),
        (1.1, True, "DateTime cannot represent value: < 1.1 >."),
        (3.1, True, "DateTime cannot represent value: < 3.1 >."),
        ("0", True, "DateTime cannot represent value: < 0 >."),
        ("1", True, "DateTime cannot represent value: < 1 >."),
        ("3", True, "DateTime cannot represent value: < 3 >."),
        ("0.0", True, "DateTime cannot represent value: < 0.0 >."),
        ("1.0", True, "DateTime cannot represent value: < 1.0 >."),
        ("3.0", True, "DateTime cannot represent value: < 3.0 >."),
        ("0.1", True, "DateTime cannot represent value: < 0.1 >."),
        ("1.1", True, "DateTime cannot represent value: < 1.1 >."),
        ("3.1", True, "DateTime cannot represent value: < 3.1 >."),
        ("0e0", True, "DateTime cannot represent value: < 0e0 >."),
        ("1e0", True, "DateTime cannot represent value: < 1e0 >."),
        ("3e0", True, "DateTime cannot represent value: < 3e0 >."),
        ("0e1", True, "DateTime cannot represent value: < 0e1 >."),
        ("1e1", True, "DateTime cannot represent value: < 1e1 >."),
        ("3e1", True, "DateTime cannot represent value: < 3e1 >."),
        ("0.1e1", True, "DateTime cannot represent value: < 0.1e1 >."),
        ("1.1e1", True, "DateTime cannot represent value: < 1.1e1 >."),
        ("3.1e1", True, "DateTime cannot represent value: < 3.1e1 >."),
        ("0.11e1", True, "DateTime cannot represent value: < 0.11e1 >."),
        ("1.11e1", True, "DateTime cannot represent value: < 1.11e1 >."),
        ("3.11e1", True, "DateTime cannot represent value: < 3.11e1 >."),
        (float("inf"), True, "DateTime cannot represent value: < inf >."),
        ("A", True, "DateTime cannot represent value: < A >."),
        ("{}", True, "DateTime cannot represent value: < {} >."),
        ({}, True, "DateTime cannot represent value: < {} >."),
        (Exception("LOL"), True, "DateTime cannot represent value: < LOL >."),
        (
            Exception,
            True,
            "DateTime cannot represent value: < <class 'Exception'> >.",
        ),
        (
            "1986-12-24T15:00:04",
            False,
            datetime.datetime(1986, 12, 24, 15, 0, 4),
        ),
        (
            datetime.datetime(1986, 12, 24, 15, 0, 4),
            True,
            "DateTime cannot represent value: < 1986-12-24 15:00:04 >.",
        ),
    ],
)
def test_scalar_datetime_coerce_input(value, should_raise_exception, expected):
    if should_raise_exception:
        with pytest.raises(TartifletteError, match=expected):
            ScalarDateTime().coerce_input(value)
    else:
        assert ScalarDateTime().coerce_input(value) == expected
