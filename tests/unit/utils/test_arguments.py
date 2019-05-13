from functools import partial
from unittest.mock import Mock

import pytest

from tartiflette.utils.arguments import (
    UNDEFINED_VALUE,
    argument_coercer,
    coerce_arguments,
)
from tests.functional.utils import AsyncMock


def _create_mock_arg(name, value):
    arg_mock = Mock()
    arg_mock.name = name
    arg_mock.value = value
    return arg_mock


def _create_mock_def_arg(name, default_value):
    arg_mock = Mock()
    arg_mock.name = name
    arg_mock.default_value = default_value
    arg_mock.directives = []
    arg_mock.coercer = Mock(
        wraps=partial(argument_coercer, arg_mock), new_callable=AsyncMock
    )
    return arg_mock


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "default_value,args,expected",
    [
        (None, {}, UNDEFINED_VALUE),
        (False, {}, UNDEFINED_VALUE),  # TODO: should fix it...
        (1, {}, 1),
        ("default", {}, "default"),
        (1, {"myArg": _create_mock_arg("myArg", 11)}, 11),
        (
            "default",
            {"myArg": _create_mock_arg("myArg", "myValue")},
            "myValue",
        ),
    ],
)
async def test_argument_coercer(default_value, args, expected):
    argument_definition_mock = Mock()
    argument_definition_mock.name = "myArg"
    argument_definition_mock.default_value = default_value
    assert (
        await argument_coercer(argument_definition_mock, args, {}, Mock())
        == expected
    )


def test_wraps_with_directives():
    from tartiflette.types.helpers import wraps_with_directives

    cllbs_a = Mock()
    cllbs_a.on_argument_execution = Mock()

    cllbs_b = Mock()
    cllbs_b.on_argument_execution = Mock()

    directives = [
        {
            "callables": {
                "on_argument_execution": cllbs_a.on_argument_execution
            },
            "args": {"a": "b"},
        },
        {
            "callables": {
                "on_argument_execution": cllbs_b.on_argument_execution
            },
            "args": {"c": "d"},
        },
    ]

    r = wraps_with_directives(directives, "on_argument_execution", "A")
    assert r is not None
    assert r.func is cllbs_a.on_argument_execution
    a, b = r.args
    assert a == {"a": "b"}
    assert b.func is cllbs_b.on_argument_execution
    a, b = b.args
    assert a == {"c": "d"}
    assert b == "A"

    assert wraps_with_directives([], "on_argument_execution", "A") == "A"


@pytest.mark.asyncio
async def test_coerce_arguments():
    argument_definitions = {
        "myFirstArg": _create_mock_def_arg("myFirstArg", "myFirstValue"),
        "mySecondArg": _create_mock_def_arg("mySecondArg", "mySecondValue"),
        "myThirdArg": _create_mock_def_arg("myThirdArg", None),
        "myFourthArg": _create_mock_def_arg("myFourthArg", None),
    }

    result = await coerce_arguments(
        argument_definitions,
        {
            "mySecondArg": _create_mock_arg(
                "mySecondArg", "customSecondArgValue"
            ),
            "myFourthArg": _create_mock_arg("myFourthArg", None),
        },
        {},
        Mock(),
    )

    assert result == {
        "myFirstArg": "myFirstValue",
        "mySecondArg": "customSecondArgValue",
        "myFourthArg": None,
    }
