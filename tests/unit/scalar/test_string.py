from decimal import Decimal

import pytest

from tartiflette import TartifletteError
from tartiflette.scalar.builtins.string import ScalarString


@pytest.mark.parametrize(
    "value,should_raise_exception,expected",
    [
        (None, False, "None"),
        (True, False, "true"),
        (False, False, "false"),
        ("", False, ""),
        (0, False, "0"),
        (1, False, "1"),
        (3, False, "3"),
        (0.0, False, "0.0"),
        (1.0, False, "1.0"),
        (3.0, False, "3.0"),
        (0.1, False, "0.1"),
        (1.1, False, "1.1"),
        (3.1, False, "3.1"),
        (Decimal(0.0), False, "0"),
        (Decimal(1.0), False, "1"),
        (Decimal(3.0), False, "3"),
        (
            Decimal(0.1),
            False,
            "0.1000000000000000055511151231257827021181583404541015625",
        ),
        (
            Decimal(1.1),
            False,
            "1.100000000000000088817841970012523233890533447265625",
        ),
        (
            Decimal(3.1),
            False,
            "3.100000000000000088817841970012523233890533447265625",
        ),
        ("0", False, "0"),
        ("1", False, "1"),
        ("3", False, "3"),
        ("0.0", False, "0.0"),
        ("1.0", False, "1.0"),
        ("3.0", False, "3.0"),
        ("0.1", False, "0.1"),
        ("1.1", False, "1.1"),
        ("3.1", False, "3.1"),
        ("0e0", False, "0e0"),
        ("1e0", False, "1e0"),
        ("3e0", False, "3e0"),
        ("0e1", False, "0e1"),
        ("1e1", False, "1e1"),
        ("3e1", False, "3e1"),
        ("0.1e1", False, "0.1e1"),
        ("1.1e1", False, "1.1e1"),
        ("3.1e1", False, "3.1e1"),
        ("0.11e1", False, "0.11e1"),
        ("1.11e1", False, "1.11e1"),
        ("3.11e1", False, "3.11e1"),
        (float("inf"), False, "inf"),
        ("A", False, "A"),
        ("{}", False, "{}"),
        ({}, False, "{}"),
        (Exception("LOL"), False, "LOL"),
        (Exception, False, "<class 'Exception'>"),
    ],
)
def test_scalar_string_coerce_output(value, should_raise_exception, expected):
    if should_raise_exception:
        with pytest.raises(TartifletteError, match=expected):
            ScalarString().coerce_output(value)
    else:
        assert ScalarString().coerce_output(value) == expected


@pytest.mark.parametrize(
    "value,should_raise_exception,expected",
    [
        (None, True, "String cannot represent a non string value: < None >."),
        (True, True, "String cannot represent a non string value: < True >."),
        (
            False,
            True,
            "String cannot represent a non string value: < False >.",
        ),
        ("", False, ""),
        (0, True, "String cannot represent a non string value: < 0 >."),
        (1, True, "String cannot represent a non string value: < 1 >."),
        (3, True, "String cannot represent a non string value: < 3 >."),
        (0.0, True, "String cannot represent a non string value: < 0.0 >."),
        (1.0, True, "String cannot represent a non string value: < 1.0 >."),
        (3.0, True, "String cannot represent a non string value: < 3.0 >."),
        (0.1, True, "String cannot represent a non string value: < 0.1 >."),
        (1.1, True, "String cannot represent a non string value: < 1.1 >."),
        (3.1, True, "String cannot represent a non string value: < 3.1 >."),
        ("0", False, "0"),
        ("1", False, "1"),
        ("3", False, "3"),
        ("0.0", False, "0.0"),
        ("1.0", False, "1.0"),
        ("3.0", False, "3.0"),
        ("0.1", False, "0.1"),
        ("1.1", False, "1.1"),
        ("3.1", False, "3.1"),
        ("0e0", False, "0e0"),
        ("1e0", False, "1e0"),
        ("3e0", False, "3e0"),
        ("0e1", False, "0e1"),
        ("1e1", False, "1e1"),
        ("3e1", False, "3e1"),
        ("0.1e1", False, "0.1e1"),
        ("1.1e1", False, "1.1e1"),
        ("3.1e1", False, "3.1e1"),
        ("0.11e1", False, "0.11e1"),
        ("1.11e1", False, "1.11e1"),
        ("3.11e1", False, "3.11e1"),
        (
            float("inf"),
            True,
            "String cannot represent a non string value: < inf >.",
        ),
        ("A", False, "A"),
        ("{}", False, "{}"),
        ({}, True, "String cannot represent a non string value: < {} >."),
        (
            Exception("LOL"),
            True,
            "String cannot represent a non string value: < LOL >.",
        ),
        (
            Exception,
            True,
            "String cannot represent a non string value: < <class 'Exception'> >.",
        ),
    ],
)
def test_scalar_string_coerce_input(value, should_raise_exception, expected):
    if should_raise_exception:
        with pytest.raises(TartifletteError, match=expected):
            ScalarString().coerce_input(value)
    else:
        assert ScalarString().coerce_input(value) == expected
