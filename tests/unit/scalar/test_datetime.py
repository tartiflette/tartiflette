import datetime

import pytest


@pytest.mark.parametrize(
    "val,expected",
    [
        (datetime.datetime(1986, 12, 24, 15, 0, 4), "1986-12-24T15:00:04"),
        (None, AttributeError),
        ("A", AttributeError),
    ],
)
def test_scalar_datetime_coerce_output(val, expected):
    from tartiflette.scalar.builtins.datetime import ScalarDateTime

    if type(expected) is type and issubclass(expected, Exception):
        with pytest.raises(expected):
            ScalarDateTime().coerce_output(val)
    else:
        assert ScalarDateTime().coerce_output(val) == expected


@pytest.mark.skip(reason="TODO: fix it")
@pytest.mark.parametrize(
    "val,expected",
    [
        ("1986-12-24T15:00:04", datetime.datetime(1986, 12, 24, 15, 0, 4)),
        ("LOL", ValueError),
        (None, TypeError),
    ],
)
def test_scalar_datetime_coerce_input(val, expected):
    from tartiflette.scalar.builtins.datetime import ScalarDateTime

    if type(expected) is type and issubclass(expected, Exception):
        with pytest.raises(expected):
            ScalarDateTime().coerce_input(val)
    else:
        assert ScalarDateTime().coerce_input(val) == expected
