import pytest


@pytest.mark.parametrize(
    "val,expected",
    [
        ("3.6", "3.6"),
        (1, "1"),
        (None, "None"),
        (Exception("LOL"), "LOL"),
        (Exception, "<class 'Exception'>"),
        (True, "True"),
        (False, "False"),
    ],
)
def test_scalar_float_coerce_output(val, expected):
    from tartiflette.scalar.builtins.id import ScalarId

    if type(expected) is type and issubclass(expected, Exception):
        with pytest.raises(expected):
            ScalarId().coerce_output(val)
    else:
        assert ScalarId().coerce_output(val) == expected


@pytest.mark.parametrize(
    "val,expected",
    [
        ("3.6", "3.6"),
        (1, "1"),
        (None, "None"),
        (Exception("LOL"), "LOL"),
        (Exception, "<class 'Exception'>"),
        (True, "True"),
        (False, "False"),
    ],
)
def test_scalar_datetime_coerce_input(val, expected):
    from tartiflette.scalar.builtins.id import ScalarId

    if type(expected) is type and issubclass(expected, Exception):
        with pytest.raises(expected):
            ScalarId().coerce_input(val)
    else:
        assert ScalarId().coerce_input(val) == expected
