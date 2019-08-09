import pytest


@pytest.mark.parametrize(
    "val,expected",
    [
        ("true", True),
        ("false", True),
        ("1", True),
        (1, True),
        (0, False),
        ("0", True),
        (3.6, True),
        (0.0, False),
        ("a", True),
        (True, True),
        (None, False),
        (False, False),
    ],
)
def test_scalar_boolean_coerce_output(val, expected):
    from tartiflette.scalar.builtins.boolean import ScalarBoolean

    assert ScalarBoolean().coerce_output(val) == expected


@pytest.mark.skip(reason="TODO: fix it")
@pytest.mark.parametrize(
    "val,expected",
    [
        ("true", True),
        ("false", True),
        ("1", True),
        (1, True),
        (0, False),
        ("0", True),
        (3.6, True),
        (0.0, False),
        ("a", True),
        (True, True),
        (None, False),
        (False, False),
    ],
)
def test_scalar_boolean_coerce_input(val, expected):
    from tartiflette.scalar.builtins.boolean import ScalarBoolean

    assert ScalarBoolean().coerce_input(val) == expected
