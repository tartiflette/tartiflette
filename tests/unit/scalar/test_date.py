import datetime

import pytest


@pytest.mark.parametrize(
    "val,expected",
    [
        (datetime.datetime(1986, 12, 24, 15, 0, 0), "1986-12-24"),
        (None, AttributeError),
        ("A", AttributeError),
    ],
)
def test_scalar_date_coerce_output(val, expected):
    from tartiflette.scalar.builtins.date import ScalarDate

    if type(expected) is type and issubclass(expected, Exception):
        with pytest.raises(expected):
            ScalarDate().coerce_output(val)
    else:
        assert ScalarDate().coerce_output(val) == expected


@pytest.mark.parametrize(
    "val,expected",
    [
        ("1986-12-24", datetime.datetime(1986, 12, 24, 0, 0, 0)),
        ("LOL", ValueError),
        (None, TypeError),
    ],
)
def test_scalar_date_coerce_input(val, expected):
    from tartiflette.scalar.builtins.date import ScalarDate

    if type(expected) is type and issubclass(expected, Exception):
        with pytest.raises(expected):
            ScalarDate().coerce_input(val)
    else:
        assert ScalarDate().coerce_input(val) == expected
