import asyncio
import inspect

from unittest.mock import Mock, patch

import pytest

from tartiflette.executors.basic import get_operation
from tartiflette.resolver.factory import default_error_coercer
from tartiflette.types.exceptions.tartiflette import (
    GraphQLError,
    UnknownAnonymousdOperation,
    UnknownNamedOperation,
)


@pytest.mark.asyncio
async def test_executor_basic__execute():

    from tartiflette.executors.basic import _execute

    a = Mock()
    b = Mock()

    exec_ctx = {}
    request_ctx = {}

    async def fcta(exec_ctx, request_ctx, *__, **___):
        a(exec_ctx, request_ctx)

    async def fctb(exec_ctx, request_ctx, *__, **___):
        b(exec_ctx, request_ctx)

    await _execute(
        [fcta, fctb],
        exec_ctx,
        request_ctx,
        initial_value=None,
        allow_parallelization=True,
    )

    assert b.called_with(exec_ctx, request_ctx)
    assert a.called_with(exec_ctx, request_ctx)


@pytest.mark.asyncio
@pytest.mark.parametrize("allow_parallelization", [True, False])
async def test_executor_basic_allow_parallelization(allow_parallelization):
    from tartiflette.executors.basic import _execute

    a = Mock()
    b = Mock()

    exec_ctx = {}
    request_ctx = {}

    async def fcta(exec_ctx, request_ctx, *__, **___):
        a(exec_ctx, request_ctx)

    async def fctb(exec_ctx, request_ctx, *__, **___):
        b(exec_ctx, request_ctx)

    with patch("asyncio.gather", wraps=asyncio.gather) as asyncio_gather_mock:
        await _execute(
            [fcta, fctb],
            exec_ctx,
            request_ctx,
            initial_value=None,
            allow_parallelization=allow_parallelization,
        )

    assert asyncio_gather_mock.called is allow_parallelization


def _get_mocked_root_nodes(cbn, marsh, alias):
    a = Mock()
    a.cant_be_null = cbn
    a.marshalled = marsh
    a.alias = alias
    a.is_execution_stopped = False
    return a


@pytest.mark.parametrize(
    "root_nodes,expected",
    [
        (None, TypeError),
        ([_get_mocked_root_nodes(True, {"b": "c"}, "a")], {"a": {"b": "c"}}),
        (
            [
                _get_mocked_root_nodes(True, {"b": "c"}, "a"),
                _get_mocked_root_nodes(True, {"b": "c"}, "b"),
            ],
            {"a": {"b": "c"}, "b": {"b": "c"}},
        ),
        ([_get_mocked_root_nodes(False, None, "v")], {"v": None}),
        ([_get_mocked_root_nodes(True, None, "v")], None),
    ],
)
def test_executor_basic__get_datas(root_nodes, expected):
    from tartiflette.executors.basic import _get_datas

    if inspect.isclass(expected) and issubclass(expected, Exception):
        with pytest.raises(expected):
            _get_datas(root_nodes)
    else:
        assert _get_datas(root_nodes) == expected


def _get_mocked_error():
    a = Mock()
    a.coerce_value = Mock(return_value={"a": "b"})
    return a


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "errors,expected",
    [
        ([], {"data": None}),
        ([_get_mocked_error()], {"data": None, "errors": [{"a": "b"}]}),
    ],
)
async def test_executor_basic_execute(errors, expected, monkeypatch):
    from tartiflette.executors import basic

    async def my_execute(_, exec_ctx, *__, **___):
        for err in errors:
            exec_ctx.add_error(err)

    monkeypatch.setattr(basic, "_execute", my_execute)

    from tartiflette.executors.basic import execute

    operation_mock = Mock()
    operation_mock.name = None
    operation_mock.children = []
    operation_mock.allow_parallelization = True

    a = await execute(
        {None: operation_mock},
        request_ctx={},
        initial_value=None,
        error_coercer=default_error_coercer,
        operation_name=None,
    )

    assert a == expected

    monkeypatch.undo()


@pytest.mark.asyncio
async def test_executor_basic_execute_custom_resolver(monkeypatch):
    from tartiflette.executors import basic

    async def my_execute(_, exec_ctx, *__, **___):
        exec_ctx.add_error(GraphQLError("My error"))

    def custom_error_coercer(exception):
        return {"message": "Error from custom_error_coercer"}

    monkeypatch.setattr(basic, "_execute", my_execute)

    from tartiflette.executors.basic import execute

    operation_mock = Mock()
    operation_mock.name = None
    operation_mock.children = []
    operation_mock.allow_parallelization = True

    a = await execute(
        {None: operation_mock},
        request_ctx={},
        initial_value=None,
        error_coercer=custom_error_coercer,
        operation_name=None,
    )

    assert a == {
        "data": None,
        "errors": [{"message": "Error from custom_error_coercer"}],
    }

    monkeypatch.undo()


@pytest.mark.asyncio
@pytest.mark.parametrize("initial_value", [None])
async def test_executor_basic_execute_initial_value(initial_value):
    from tartiflette.executors.basic import _execute

    a = Mock()
    b = Mock()

    exec_ctx = {}
    request_ctx = {}

    async def fcta(exec_ctx, request_ctx, parent_result, **___):
        assert parent_result == initial_value
        a(exec_ctx, request_ctx, parent_result)

    async def fctb(exec_ctx, request_ctx, parent_result, **___):
        assert parent_result == initial_value
        b(exec_ctx, request_ctx, parent_result)

    with patch("asyncio.gather", wraps=asyncio.gather) as asyncio_gather_mock:
        await _execute(
            [fcta, fctb],
            exec_ctx,
            request_ctx,
            initial_value=initial_value,
            allow_parallelization=True,
        )

    assert b.called_with(exec_ctx, request_ctx, initial_value)
    assert a.called_with(exec_ctx, request_ctx, initial_value)


_OPERATION_MOCK = Mock()


@pytest.mark.parametrize(
    "operations,operation_name,expected",
    [
        (
            {"operation_name": _OPERATION_MOCK},
            "operation_name",
            (_OPERATION_MOCK, None),
        ),
        (
            {"unknown": _OPERATION_MOCK},
            "operation_name",
            (
                None,
                [
                    UnknownNamedOperation(
                        "Unknown operation named < operation_name >."
                    )
                ],
            ),
        ),
        (
            {"unknown_1": _OPERATION_MOCK, "unknown_2": _OPERATION_MOCK},
            None,
            (
                None,
                [
                    UnknownAnonymousdOperation(
                        "Must provide operation name if query contains multiple "
                        "operations."
                    )
                ],
            ),
        ),
        ({"unknown": _OPERATION_MOCK}, None, (_OPERATION_MOCK, None)),
        ({None: _OPERATION_MOCK}, None, (_OPERATION_MOCK, None)),
    ],
)
def test_executor_get_operation(operations, operation_name, expected):
    operation, errors = get_operation(operations, operation_name)

    expected_operation, expected_errors = expected
    if expected_operation:
        assert operation == expected_operation
        assert errors is None
    if expected_errors:
        assert len(expected_errors) == len(errors)
        for expected_error, error in zip(expected_errors, errors):
            assert type(expected_error) is type(error)
            assert str(expected_error) == str(error)
        assert operation is None
