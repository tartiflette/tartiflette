import pytest


@pytest.mark.parametrize(
    "val,expected",
    [
        ("3.6", ValueError),
        (1, 1),
        (1.1, 1),
        (None, TypeError),
        (Exception("LOL"), TypeError),
        (Exception, TypeError),
        (True, 1),
        (False, 0),
    ],
)
def test_scalar_float_coerce_output(val, expected):
    from tartiflette.scalar.int import ScalarInt

    if type(expected) is type and issubclass(expected, Exception):
        with pytest.raises(expected):
            ScalarInt.coerce_output(val)
    else:
        assert ScalarInt.coerce_output(val) == expected


@pytest.mark.parametrize(
    "val,expected",
    [
        ("3.6", ValueError),
        (1, 1),
        (1.1, 1),
        (None, TypeError),
        (Exception("LOL"), TypeError),
        (Exception, TypeError),
        (True, 1),
        (False, 0),
    ],
)
def test_scalar_datetime_coerce_input(val, expected):
    from tartiflette.scalar.int import ScalarInt

    if type(expected) is type and issubclass(expected, Exception):
        with pytest.raises(expected):
            ScalarInt.coerce_input(val)
    else:
        assert ScalarInt.coerce_input(val) == expected
