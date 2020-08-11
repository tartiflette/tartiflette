from decimal import Decimal

import pytest

from tartiflette import TartifletteError
from tartiflette.scalar.builtins.int import ScalarInt


@pytest.mark.parametrize(
    "value,should_raise_exception,expected",
    [
        (None, True, "Int cannot represent non-integer value: < None >."),
        (True, False, 1),
        (False, False, 0),
        ("", True, "Int cannot represent non-integer value: <  >."),
        (0, False, 0),
        (1, False, 1),
        (3, False, 3),
        (
            -2_147_483_649,
            True,
            "Int cannot represent non 32-bit signed integer value: < -2147483649 >.",
        ),
        (
            2_147_483_648,
            True,
            "Int cannot represent non 32-bit signed integer value: < 2147483648 >.",
        ),
        (0.0, False, 0),
        (1.0, False, 1),
        (3.0, False, 3),
        (0.1, True, "Int cannot represent non-integer value: < 0.1 >."),
        (1.1, True, "Int cannot represent non-integer value: < 1.1 >."),
        (3.1, True, "Int cannot represent non-integer value: < 3.1 >."),
        (Decimal(0.0), False, 0),
        (Decimal(1.0), False, 1),
        (Decimal(3.0), False, 3),
        (
            Decimal(0.1),
            True,
            "Int cannot represent non-integer value: < 0.1000000000000000055511151231257827021181583404541015625 >.",
        ),
        (
            Decimal(1.1),
            True,
            "Int cannot represent non-integer value: < 1.100000000000000088817841970012523233890533447265625 >.",
        ),
        (
            Decimal(3.1),
            True,
            "Int cannot represent non-integer value: < 3.100000000000000088817841970012523233890533447265625 >.",
        ),
        ("0", False, 0),
        ("1", False, 1),
        ("3", False, 3),
        ("0.0", False, 0),
        ("1.0", False, 1),
        ("3.0", False, 3),
        ("0.1", True, "Int cannot represent non-integer value: < 0.1 >."),
        ("1.1", True, "Int cannot represent non-integer value: < 1.1 >."),
        ("3.1", True, "Int cannot represent non-integer value: < 3.1 >."),
        ("0e0", False, 0),
        ("1e0", False, 1),
        ("3e0", False, 3),
        ("0e1", False, 0),
        ("1e1", False, 10),
        ("3e1", False, 30),
        ("0.1e1", False, 1),
        ("1.1e1", False, 11),
        ("3.1e1", False, 31),
        (
            "0.11e1",
            True,
            "Int cannot represent non-integer value: < 0.11e1 >.",
        ),
        (
            "1.11e1",
            True,
            "Int cannot represent non-integer value: < 1.11e1 >.",
        ),
        (
            "3.11e1",
            True,
            "Int cannot represent non-integer value: < 3.11e1 >.",
        ),
        (
            float("inf"),
            True,
            "Int cannot represent non-integer value: < inf >.",
        ),
        ("A", True, "Int cannot represent non-integer value: < A >."),
        ("{}", True, "Int cannot represent non-integer value: < {} >."),
        ({}, True, "Int cannot represent non-integer value: < {} >."),
        (
            Exception("LOL"),
            True,
            "Int cannot represent non-integer value: < LOL >.",
        ),
        (
            Exception,
            True,
            "Int cannot represent non-integer value: < <class 'Exception'> >.",
        ),
    ],
)
def test_scalar_int_coerce_output(value, should_raise_exception, expected):
    if should_raise_exception:
        with pytest.raises(TartifletteError, match=expected):
            ScalarInt().coerce_output(value)
    else:
        assert ScalarInt().coerce_output(value) == expected


@pytest.mark.parametrize(
    "value,should_raise_exception,expected",
    [
        (None, True, "Int cannot represent non-integer value: < None >."),
        (True, True, "Int cannot represent non-integer value: < True >."),
        (False, True, "Int cannot represent non-integer value: < False >."),
        ("", True, "Int cannot represent non-integer value: <  >."),
        (0, False, 0),
        (1, False, 1),
        (3, False, 3),
        (0.0, False, 0),
        (1.0, False, 1),
        (3.0, False, 3),
        (
            -2_147_483_649,
            True,
            "Int cannot represent non 32-bit signed integer value: < -2147483649 >.",
        ),
        (
            2_147_483_648,
            True,
            "Int cannot represent non 32-bit signed integer value: < 2147483648 >.",
        ),
        (0.1, True, "Int cannot represent non-integer value: < 0.1 >."),
        (1.1, True, "Int cannot represent non-integer value: < 1.1 >."),
        (3.1, True, "Int cannot represent non-integer value: < 3.1 >."),
        ("0", True, "Int cannot represent non-integer value: < 0 >."),
        ("1", True, "Int cannot represent non-integer value: < 1 >."),
        ("3", True, "Int cannot represent non-integer value: < 3 >."),
        ("0.0", True, "Int cannot represent non-integer value: < 0.0 >."),
        ("1.0", True, "Int cannot represent non-integer value: < 1.0 >."),
        ("3.0", True, "Int cannot represent non-integer value: < 3.0 >."),
        ("0.1", True, "Int cannot represent non-integer value: < 0.1 >."),
        ("1.1", True, "Int cannot represent non-integer value: < 1.1 >."),
        ("3.1", True, "Int cannot represent non-integer value: < 3.1 >."),
        ("0e0", True, "Int cannot represent non-integer value: < 0e0 >."),
        ("1e0", True, "Int cannot represent non-integer value: < 1e0 >."),
        ("3e0", True, "Int cannot represent non-integer value: < 3e0 >."),
        ("0e1", True, "Int cannot represent non-integer value: < 0e1 >."),
        ("1e1", True, "Int cannot represent non-integer value: < 1e1 >."),
        ("3e1", True, "Int cannot represent non-integer value: < 3e1 >."),
        ("0.1e1", True, "Int cannot represent non-integer value: < 0.1e1 >."),
        ("1.1e1", True, "Int cannot represent non-integer value: < 1.1e1 >."),
        ("3.1e1", True, "Int cannot represent non-integer value: < 3.1e1 >."),
        (
            "0.11e1",
            True,
            "Int cannot represent non-integer value: < 0.11e1 >.",
        ),
        (
            "1.11e1",
            True,
            "Int cannot represent non-integer value: < 1.11e1 >.",
        ),
        (
            "3.11e1",
            True,
            "Int cannot represent non-integer value: < 3.11e1 >.",
        ),
        (
            float("inf"),
            True,
            "Int cannot represent non-integer value: < inf >.",
        ),
        ("A", True, "Int cannot represent non-integer value: < A >."),
        ("{}", True, "Int cannot represent non-integer value: < {} >."),
        ({}, True, "Int cannot represent non-integer value: < {} >."),
        (
            Exception("LOL"),
            True,
            "Int cannot represent non-integer value: < LOL >.",
        ),
        (
            Exception,
            True,
            "Int cannot represent non-integer value: < <class 'Exception'> >.",
        ),
    ],
)
def test_scalar_int_coerce_input(value, should_raise_exception, expected):
    if should_raise_exception:
        with pytest.raises(TartifletteError, match=expected):
            ScalarInt().coerce_input(value)
    else:
        assert ScalarInt().coerce_input(value) == expected
