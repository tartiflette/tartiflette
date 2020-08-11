from decimal import Decimal

import pytest

from tartiflette import TartifletteError
from tartiflette.scalar.builtins.float import ScalarFloat


@pytest.mark.parametrize(
    "value,should_raise_exception,expected",
    [
        (None, True, "Float cannot represent non numeric value: < None >."),
        (True, False, 1.0),
        (False, False, 0.0),
        ("", True, "Float cannot represent non numeric value: <  >."),
        (0, False, 0.0),
        (1, False, 1.0),
        (3, False, 3.0),
        (0.0, False, 0.0),
        (1.0, False, 1.0),
        (3.0, False, 3.0),
        (0.1, False, 0.1),
        (1.1, False, 1.1),
        (3.1, False, 3.1),
        (Decimal(0.0), False, 0.0),
        (Decimal(1.0), False, 1.0),
        (Decimal(3.0), False, 3.0),
        (Decimal(0.1), False, 0.1),
        (Decimal(1.1), False, 1.1),
        (Decimal(3.1), False, 3.1),
        ("0", False, 0.0),
        ("1", False, 1.0),
        ("3", False, 3.0),
        ("0.0", False, 0.0),
        ("1.0", False, 1.0),
        ("3.0", False, 3.0),
        ("0.1", False, 0.1),
        ("1.1", False, 1.1),
        ("3.1", False, 3.1),
        ("0e0", False, 0.0),
        ("1e0", False, 1.0),
        ("3e0", False, 3.0),
        ("0e1", False, 0.0),
        ("1e1", False, 10.0),
        ("3e1", False, 30.0),
        ("0.1e1", False, 1.0),
        ("1.1e1", False, 11.0),
        ("3.1e1", False, 31.0),
        ("0.11e1", False, 1.1),
        ("1.11e1", False, 11.1),
        ("3.11e1", False, 31.1),
        (
            float("inf"),
            True,
            "Float cannot represent non numeric value: < inf >.",
        ),
        ("A", True, "Float cannot represent non numeric value: < A >."),
        ("{}", True, "Float cannot represent non numeric value: < {} >."),
        ({}, True, "Float cannot represent non numeric value: < {} >."),
        (
            Exception("LOL"),
            True,
            "Float cannot represent non numeric value: < LOL >.",
        ),
        (
            Exception,
            True,
            "Float cannot represent non numeric value: < <class 'Exception'> >.",
        ),
    ],
)
def test_scalar_float_coerce_output(value, should_raise_exception, expected):
    if should_raise_exception:
        with pytest.raises(TartifletteError, match=expected):
            ScalarFloat().coerce_output(value)
    else:
        assert ScalarFloat().coerce_output(value) == expected


@pytest.mark.parametrize(
    "value,should_raise_exception,expected",
    [
        (None, True, "Float cannot represent non numeric value: < None >."),
        (True, True, "Float cannot represent non numeric value: < True >."),
        (False, True, "Float cannot represent non numeric value: < False >."),
        ("", True, "Float cannot represent non numeric value: <  >."),
        (0, False, 0.0),
        (1, False, 1.0),
        (3, False, 3.0),
        (0.0, False, 0.0),
        (1.0, False, 1.0),
        (3.0, False, 3.0),
        (0.1, False, 0.1),
        (1.1, False, 1.1),
        (3.1, False, 3.1),
        ("0", True, "Float cannot represent non numeric value: < 0 >."),
        ("1", True, "Float cannot represent non numeric value: < 1 >."),
        ("3", True, "Float cannot represent non numeric value: < 3 >."),
        ("0.0", True, "Float cannot represent non numeric value: < 0.0 >."),
        ("1.0", True, "Float cannot represent non numeric value: < 1.0 >."),
        ("3.0", True, "Float cannot represent non numeric value: < 3.0 >."),
        ("0.1", True, "Float cannot represent non numeric value: < 0.1 >."),
        ("1.1", True, "Float cannot represent non numeric value: < 1.1 >."),
        ("3.1", True, "Float cannot represent non numeric value: < 3.1 >."),
        ("0e0", True, "Float cannot represent non numeric value: < 0e0 >."),
        ("1e0", True, "Float cannot represent non numeric value: < 1e0 >."),
        ("3e0", True, "Float cannot represent non numeric value: < 3e0 >."),
        ("0e1", True, "Float cannot represent non numeric value: < 0e1 >."),
        ("1e1", True, "Float cannot represent non numeric value: < 1e1 >."),
        ("3e1", True, "Float cannot represent non numeric value: < 3e1 >."),
        (
            "0.1e1",
            True,
            "Float cannot represent non numeric value: < 0.1e1 >.",
        ),
        (
            "1.1e1",
            True,
            "Float cannot represent non numeric value: < 1.1e1 >.",
        ),
        (
            "3.1e1",
            True,
            "Float cannot represent non numeric value: < 3.1e1 >.",
        ),
        (
            "0.11e1",
            True,
            "Float cannot represent non numeric value: < 0.11e1 >.",
        ),
        (
            "1.11e1",
            True,
            "Float cannot represent non numeric value: < 1.11e1 >.",
        ),
        (
            "3.11e1",
            True,
            "Float cannot represent non numeric value: < 3.11e1 >.",
        ),
        (
            float("inf"),
            True,
            "Float cannot represent non numeric value: < inf >.",
        ),
        ("A", True, "Float cannot represent non numeric value: < A >."),
        ("{}", True, "Float cannot represent non numeric value: < {} >."),
        ({}, True, "Float cannot represent non numeric value: < {} >."),
        (
            Exception("LOL"),
            True,
            "Float cannot represent non numeric value: < LOL >.",
        ),
        (
            Exception,
            True,
            "Float cannot represent non numeric value: < <class 'Exception'> >.",
        ),
    ],
)
def test_scalar_float_coerce_input(value, should_raise_exception, expected):
    if should_raise_exception:
        with pytest.raises(TartifletteError, match=expected):
            ScalarFloat().coerce_input(value)
    else:
        assert ScalarFloat().coerce_input(value) == expected
