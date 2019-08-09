import pytest


@pytest.mark.parametrize(
    "val,expected",
    [
        ("3.6", 3.6),
        (1, 1.0),
        (None, TypeError),
        (Exception(), TypeError),
        (Exception, TypeError),
        ("A", ValueError),
    ],
)
def test_scalar_float_coerce_output(val, expected):
    from tartiflette.scalar.builtins.float import ScalarFloat

    if type(expected) is type and issubclass(expected, Exception):
        with pytest.raises(expected):
            ScalarFloat().coerce_output(val)
    else:
        assert ScalarFloat().coerce_output(val) == expected


@pytest.mark.parametrize(
    "val,expected",
    [
        ("3.6", TypeError),
        (1, 1.0),
        (None, TypeError),
        (Exception(), TypeError),
        (Exception, TypeError),
        ("A", TypeError),
    ],
)
def test_scalar_float_coerce_input(val, expected):
    from tartiflette.scalar.builtins.float import ScalarFloat

    if type(expected) is type and issubclass(expected, Exception):
        with pytest.raises(expected):
            ScalarFloat().coerce_input(val)
    else:
        assert ScalarFloat().coerce_input(val) == expected
