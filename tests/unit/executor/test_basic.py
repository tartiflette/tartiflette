import pytest
import inspect
from unittest.mock import Mock


@pytest.mark.asyncio
async def test_executor_basic__execute():

    from tartiflette.executors.basic import _execute

    a = Mock()
    b = Mock()

    exec_ctx = {}
    request_ctx = {}

    async def fcta(exec_ctx, request_ctx):
        a(exec_ctx, request_ctx)

    async def fctb(exec_ctx, request_ctx):
        b(exec_ctx, request_ctx)

    await _execute([fcta, fctb], exec_ctx, request_ctx)

    assert b.called_with(exec_ctx, request_ctx)
    assert a.called_with(exec_ctx, request_ctx)


def _get_mocked_root_nodes(cbn, marsh, alias):
    a = Mock()
    a.cant_be_null = cbn
    a.marshalled = marsh
    a.alias = alias
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
        ([], {"data": {}}),
        ([_get_mocked_error()], {"data": {}, "errors": [{"a": "b"}]}),
    ],
)
async def test_executor_basic_execute(errors, expected, monkeypatch):
    from tartiflette.executors import basic

    async def my_execute(_, exec_ctx, __):
        for err in errors:
            exec_ctx.errors.append(err)

    monkeypatch.setattr(basic, "_execute", my_execute)

    from tartiflette.executors.basic import execute

    a = await execute([], request_ctx={})

    assert a == expected

    monkeypatch.undo()
