from decimal import Decimal

import pytest

from tartiflette import TartifletteError
from tartiflette.scalar.builtins.boolean import ScalarBoolean


@pytest.mark.parametrize(
    "value,should_raise_exception,expected",
    [
        (
            None,
            True,
            "Boolean cannot represent a non boolean value: < None >.",
        ),
        (True, False, True),
        (False, False, False),
        ("", True, "Boolean cannot represent a non boolean value: <  >."),
        (0, False, False),
        (1, False, True),
        (3, False, True),
        (0.0, False, False),
        (1.0, False, True),
        (3.0, False, True),
        (0.1, False, True),
        (1.1, False, True),
        (3.1, False, True),
        (Decimal(0.0), False, False),
        (Decimal(1.0), False, True),
        (Decimal(3.0), False, True),
        (Decimal(0.1), False, True),
        (Decimal(1.1), False, True),
        (Decimal(3.1), False, True),
        ("0", True, "Boolean cannot represent a non boolean value: < 0 >."),
        ("1", True, "Boolean cannot represent a non boolean value: < 1 >."),
        ("3", True, "Boolean cannot represent a non boolean value: < 3 >."),
        (
            "0.0",
            True,
            "Boolean cannot represent a non boolean value: < 0.0 >.",
        ),
        (
            "1.0",
            True,
            "Boolean cannot represent a non boolean value: < 1.0 >.",
        ),
        (
            "3.0",
            True,
            "Boolean cannot represent a non boolean value: < 3.0 >.",
        ),
        (
            "0.1",
            True,
            "Boolean cannot represent a non boolean value: < 0.1 >.",
        ),
        (
            "1.1",
            True,
            "Boolean cannot represent a non boolean value: < 1.1 >.",
        ),
        (
            "3.1",
            True,
            "Boolean cannot represent a non boolean value: < 3.1 >.",
        ),
        (
            "0e0",
            True,
            "Boolean cannot represent a non boolean value: < 0e0 >.",
        ),
        (
            "1e0",
            True,
            "Boolean cannot represent a non boolean value: < 1e0 >.",
        ),
        (
            "3e0",
            True,
            "Boolean cannot represent a non boolean value: < 3e0 >.",
        ),
        (
            "0e1",
            True,
            "Boolean cannot represent a non boolean value: < 0e1 >.",
        ),
        (
            "1e1",
            True,
            "Boolean cannot represent a non boolean value: < 1e1 >.",
        ),
        (
            "3e1",
            True,
            "Boolean cannot represent a non boolean value: < 3e1 >.",
        ),
        (
            "0.1e1",
            True,
            "Boolean cannot represent a non boolean value: < 0.1e1 >.",
        ),
        (
            "1.1e1",
            True,
            "Boolean cannot represent a non boolean value: < 1.1e1 >.",
        ),
        (
            "3.1e1",
            True,
            "Boolean cannot represent a non boolean value: < 3.1e1 >.",
        ),
        (
            "0.11e1",
            True,
            "Boolean cannot represent a non boolean value: < 0.11e1 >.",
        ),
        (
            "1.11e1",
            True,
            "Boolean cannot represent a non boolean value: < 1.11e1 >.",
        ),
        (
            "3.11e1",
            True,
            "Boolean cannot represent a non boolean value: < 3.11e1 >.",
        ),
        (
            float("inf"),
            True,
            "Boolean cannot represent a non boolean value: < inf >.",
        ),
        ("A", True, "Boolean cannot represent a non boolean value: < A >."),
        ("{}", True, "Boolean cannot represent a non boolean value: < {} >."),
        ({}, True, "Boolean cannot represent a non boolean value: < {} >."),
        (
            Exception("LOL"),
            True,
            "Boolean cannot represent a non boolean value: < LOL >.",
        ),
        (
            Exception,
            True,
            "Boolean cannot represent a non boolean value: < <class 'Exception'> >.",
        ),
    ],
)
def test_scalar_boolean_coerce_output(value, should_raise_exception, expected):
    if should_raise_exception:
        with pytest.raises(TartifletteError, match=expected):
            ScalarBoolean().coerce_output(value)
    else:
        assert ScalarBoolean().coerce_output(value) == expected


@pytest.mark.parametrize(
    "value,should_raise_exception,expected",
    [
        (
            None,
            True,
            "Boolean cannot represent a non boolean value: < None >.",
        ),
        (True, False, True),
        (False, False, False),
        ("", True, "Boolean cannot represent a non boolean value: <  >."),
        (0, True, "Boolean cannot represent a non boolean value: < 0 >."),
        (1, True, "Boolean cannot represent a non boolean value: < 1 >."),
        (3, True, "Boolean cannot represent a non boolean value: < 3 >."),
        (0.0, True, "Boolean cannot represent a non boolean value: < 0.0 >."),
        (1.0, True, "Boolean cannot represent a non boolean value: < 1.0 >."),
        (3.0, True, "Boolean cannot represent a non boolean value: < 3.0 >."),
        (0.1, True, "Boolean cannot represent a non boolean value: < 0.1 >."),
        (1.1, True, "Boolean cannot represent a non boolean value: < 1.1 >."),
        (3.1, True, "Boolean cannot represent a non boolean value: < 3.1 >."),
        ("0", True, "Boolean cannot represent a non boolean value: < 0 >."),
        ("1", True, "Boolean cannot represent a non boolean value: < 1 >."),
        ("3", True, "Boolean cannot represent a non boolean value: < 3 >."),
        (
            "0.0",
            True,
            "Boolean cannot represent a non boolean value: < 0.0 >.",
        ),
        (
            "1.0",
            True,
            "Boolean cannot represent a non boolean value: < 1.0 >.",
        ),
        (
            "3.0",
            True,
            "Boolean cannot represent a non boolean value: < 3.0 >.",
        ),
        (
            "0.1",
            True,
            "Boolean cannot represent a non boolean value: < 0.1 >.",
        ),
        (
            "1.1",
            True,
            "Boolean cannot represent a non boolean value: < 1.1 >.",
        ),
        (
            "3.1",
            True,
            "Boolean cannot represent a non boolean value: < 3.1 >.",
        ),
        (
            "0e0",
            True,
            "Boolean cannot represent a non boolean value: < 0e0 >.",
        ),
        (
            "1e0",
            True,
            "Boolean cannot represent a non boolean value: < 1e0 >.",
        ),
        (
            "3e0",
            True,
            "Boolean cannot represent a non boolean value: < 3e0 >.",
        ),
        (
            "0e1",
            True,
            "Boolean cannot represent a non boolean value: < 0e1 >.",
        ),
        (
            "1e1",
            True,
            "Boolean cannot represent a non boolean value: < 1e1 >.",
        ),
        (
            "3e1",
            True,
            "Boolean cannot represent a non boolean value: < 3e1 >.",
        ),
        (
            "0.1e1",
            True,
            "Boolean cannot represent a non boolean value: < 0.1e1 >.",
        ),
        (
            "1.1e1",
            True,
            "Boolean cannot represent a non boolean value: < 1.1e1 >.",
        ),
        (
            "3.1e1",
            True,
            "Boolean cannot represent a non boolean value: < 3.1e1 >.",
        ),
        (
            "0.11e1",
            True,
            "Boolean cannot represent a non boolean value: < 0.11e1 >.",
        ),
        (
            "1.11e1",
            True,
            "Boolean cannot represent a non boolean value: < 1.11e1 >.",
        ),
        (
            "3.11e1",
            True,
            "Boolean cannot represent a non boolean value: < 3.11e1 >.",
        ),
        (
            float("inf"),
            True,
            "Boolean cannot represent a non boolean value: < inf >.",
        ),
        ("A", True, "Boolean cannot represent a non boolean value: < A >."),
        ("{}", True, "Boolean cannot represent a non boolean value: < {} >."),
        ({}, True, "Boolean cannot represent a non boolean value: < {} >."),
        (
            Exception("LOL"),
            True,
            "Boolean cannot represent a non boolean value: < LOL >.",
        ),
        (
            Exception,
            True,
            "Boolean cannot represent a non boolean value: < <class 'Exception'> >.",
        ),
    ],
)
def test_scalar_boolean_coerce_input(value, should_raise_exception, expected):
    if should_raise_exception:
        with pytest.raises(TartifletteError, match=expected):
            ScalarBoolean().coerce_input(value)
    else:
        assert ScalarBoolean().coerce_input(value) == expected
