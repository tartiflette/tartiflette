import datetime

import pytest


@pytest.mark.parametrize(
    "val,expected",
    [
        (datetime.datetime(1970, 11, 10, 15, 52, 52), "15:52:52"),
        (None, AttributeError),
        ("LOL", AttributeError),
    ],
)
def test_scalar_time_coerce_output(val, expected):
    from tartiflette.scalar.builtins.time import ScalarTime

    if type(expected) is type and issubclass(expected, Exception):
        with pytest.raises(expected):
            ScalarTime().coerce_output(val)
    else:
        assert ScalarTime().coerce_output(val) == expected


@pytest.mark.parametrize(
    "val,expected",
    [
        ("15:52:52", datetime.datetime(1900, 1, 1, 15, 52, 52)),
        (None, TypeError),
        ("LOL", ValueError),
    ],
)
def test_scalar_time_coerce_input(val, expected):
    from tartiflette.scalar.builtins.time import ScalarTime

    if type(expected) is type and issubclass(expected, Exception):
        with pytest.raises(expected):
            ScalarTime().coerce_input(val)
    else:
        assert ScalarTime().coerce_input(val) == expected
