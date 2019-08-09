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
def test_scalar_int_coerce_output(val, expected):
    from tartiflette.scalar.builtins.int import ScalarInt

    if type(expected) is type and issubclass(expected, Exception):
        with pytest.raises(expected):
            ScalarInt().coerce_output(val)
    else:
        assert ScalarInt().coerce_output(val) == expected


@pytest.mark.parametrize(
    "val,expected",
    [
        ("3.6", TypeError),
        (1, 1),
        (1.1, TypeError),
        (None, TypeError),
        (Exception("LOL"), TypeError),
        (Exception, TypeError),
        (True, TypeError),
        (False, TypeError),
    ],
)
def test_scalar_int_coerce_input(val, expected):
    from tartiflette.scalar.builtins.int import ScalarInt

    if type(expected) is type and issubclass(expected, Exception):
        with pytest.raises(expected):
            ScalarInt().coerce_input(val)
    else:
        assert ScalarInt().coerce_input(val) == expected
