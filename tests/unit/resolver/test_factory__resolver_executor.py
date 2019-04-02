from unittest.mock import MagicMock, Mock, patch

import pytest

from tartiflette.types.exceptions.tartiflette import MultipleException
from tests.unit.utils import AsyncMock


def test_resolver_factory__resolver_executor_instance():
    from tartiflette.resolver.factory import _ResolverExecutor

    field = Mock()
    field.schema = None
    field.gql_type = "aType"

    res_ex = _ResolverExecutor("A", field)
    assert res_ex._raw_func == "A"
    assert res_ex._func == "A"
    assert res_ex._schema_field is field
    assert res_ex._coercer is None
    assert not res_ex._shall_produce_list

    res_ex = _ResolverExecutor("A", field)
    assert res_ex._raw_func == "A"
    assert res_ex._func == "A"
    assert res_ex._schema_field is field
    assert res_ex._coercer is None
    assert not res_ex._shall_produce_list


class FakeAsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        return "aResult"


@pytest.fixture
def _resolver_executor_mock():
    from tartiflette.resolver.factory import _ResolverExecutor

    field = Mock()
    field.schema = None
    field.gql_type = "aType"
    field.arguments = {}

    res_ex = _ResolverExecutor(FakeAsyncMock(), field)
    return res_ex


@pytest.mark.asyncio
async def test_resolver_factory__resolver_executor__introspection(
    _resolver_executor_mock
):
    with patch(
        "tartiflette.resolver.factory._execute_introspection_directives",
        return_value=["A"],
    ) as mocked_intro:
        r = await _resolver_executor_mock._introspection(["T"], None, None)
        assert mocked_intro.call_args_list == [((["T"], None, None),)]
        assert r == ["A"]

    with patch(
        "tartiflette.resolver.factory._execute_introspection_directives",
        return_value=["A"],
    ) as mocked_intro:
        r = await _resolver_executor_mock._introspection("T", None, None)
        assert mocked_intro.call_args_list == [((["T"], None, None),)]
        assert r == "A"


@pytest.mark.asyncio
async def test_resolver_factory__resolver_executor___call__(
    _resolver_executor_mock
):
    p_r = Mock()

    arg_mock = Mock()
    arg_mock.name = "AB"
    arg_mock.value = "M2B"
    args = {"AB": arg_mock}
    req_ctx = {"M2B": "AB"}
    info = Mock()
    info.execution_ctx = Mock()
    info.execution_ctx.is_introspection = False

    _resolver_executor_mock._coercer = Mock(return_value="LOL")
    _resolver_executor_mock._introspection = FakeAsyncMock()

    with patch(
        "tartiflette.resolver.factory.coerce_arguments",
        new_callable=AsyncMock,
        return_value={"AB": "M2B"},
    ) as coerce_arguments_mock:
        r, c = await _resolver_executor_mock(p_r, arg_mock, req_ctx, info)
        coerce_arguments_mock.assert_called_once_with(
            {}, arg_mock, req_ctx, info
        )
        assert r == "aResult"
        assert c == "LOL"

    assert _resolver_executor_mock._func.call_args_list == [
        ((p_r, {"AB": "M2B"}, req_ctx, info),)
    ]
    assert _resolver_executor_mock._coercer.call_args_list == [
        (("aResult", info),)
    ]

    info.execution_ctx.is_introspection = True
    r, c = await _resolver_executor_mock(p_r, args, req_ctx, info)

    assert _resolver_executor_mock._introspection.call_args_list == [
        (("aResult", req_ctx, info),)
    ]

    async def a_raising_func(*args, **kwargs):
        raise Exception("A")

    _resolver_executor_mock._func = a_raising_func

    r, c = await _resolver_executor_mock(p_r, args, req_ctx, info)
    assert isinstance(r, Exception)
    assert c is None


def test_resolver_factory__resolver_executor_apply_directives(
    _resolver_executor_mock
):
    _resolver_executor_mock._schema_field.directives = ["B"]

    with patch(
        "tartiflette.resolver.factory._surround_with_execution_directives",
        return_value="LOL",
    ) as mocked_ex:
        assert _resolver_executor_mock.apply_directives() is None
        assert mocked_ex.call_args_list == [
            (
                (
                    _resolver_executor_mock._raw_func,
                    _resolver_executor_mock._schema_field.directives,
                ),
            )
        ]
        assert _resolver_executor_mock._func == "LOL"

    del _resolver_executor_mock._schema_field.directives

    assert _resolver_executor_mock.apply_directives() is None
    assert _resolver_executor_mock._func is _resolver_executor_mock._raw_func


def test_resolver_factory__resolver_executor_update_func(
    _resolver_executor_mock
):
    assert _resolver_executor_mock._func is not "g"
    assert _resolver_executor_mock._raw_func is not "g"
    assert _resolver_executor_mock.update_func("g") is None
    assert _resolver_executor_mock._func is not "g"
    assert _resolver_executor_mock._raw_func == "g"


def test_resolver_factory__resolver_executor_update_coercer(
    _resolver_executor_mock
):

    with patch(
        "tartiflette.resolver.factory.get_coercer", return_value="T"
    ) as mocked_g_co:

        assert _resolver_executor_mock.update_coercer() is None
        assert mocked_g_co.call_args_list == [
            ((_resolver_executor_mock._schema_field,),)
        ]
        assert _resolver_executor_mock._coercer == "T"


def test_resolver_factory__resolver_executor_update_bake(
    _resolver_executor_mock
):
    from tartiflette.resolver.factory import default_resolver

    _resolver_executor_mock._schema_field.subscribe = None
    _resolver_executor_mock.update_func = Mock()
    _resolver_executor_mock.update_coercer = Mock()
    _resolver_executor_mock.apply_directives = Mock()

    assert _resolver_executor_mock.bake(None) is None
    _resolver_executor_mock.update_coercer.assert_called_once()
    _resolver_executor_mock.apply_directives.assert_called_once()
    assert not _resolver_executor_mock.update_func.called
    assert _resolver_executor_mock._raw_func is not "T"

    assert _resolver_executor_mock.bake("T") is None
    assert not _resolver_executor_mock.update_func.called
    assert _resolver_executor_mock._raw_func is not "T"

    _resolver_executor_mock._raw_func = default_resolver

    assert _resolver_executor_mock.bake(None) is None
    assert not _resolver_executor_mock.update_func.called
    assert _resolver_executor_mock._raw_func is not "T"
    assert _resolver_executor_mock._raw_func is default_resolver

    assert _resolver_executor_mock.bake("T") is None
    assert _resolver_executor_mock.update_func.called


def test_resolver_factory__resolver_executor_update_prop_schema_field(
    _resolver_executor_mock
):
    _resolver_executor_mock._schema_field = 3
    assert 3 == _resolver_executor_mock.schema_field


def test_resolver_factory__resolver_executor_update_prop_shall_produce_list(
    _resolver_executor_mock
):
    _resolver_executor_mock._shall_produce_list = 3
    assert 3 == _resolver_executor_mock.shall_produce_list


def test_resolver_factory__resolver_executor_update_prop_cant_be_null(
    _resolver_executor_mock
):
    from tartiflette.types.field import GraphQLField
    from tartiflette.types.non_null import GraphQLNonNull

    _resolver_executor_mock._schema_field = GraphQLField("A", gql_type="F")

    assert not _resolver_executor_mock.cant_be_null
    _resolver_executor_mock._schema_field = GraphQLField(
        "A", gql_type=GraphQLNonNull(gql_type="F")
    )
    assert _resolver_executor_mock.cant_be_null


def test_resolver_factory__resolver_executor_update_prop_contains_not_null(
    _resolver_executor_mock
):
    from tartiflette.types.field import GraphQLField
    from tartiflette.types.non_null import GraphQLNonNull
    from tartiflette.types.list import GraphQLList

    _resolver_executor_mock._schema_field = GraphQLField("A", gql_type="F")

    assert not _resolver_executor_mock.contains_not_null
    _resolver_executor_mock._schema_field = GraphQLField(
        "A", gql_type=GraphQLNonNull(gql_type="F")
    )
    assert _resolver_executor_mock.contains_not_null

    _resolver_executor_mock._schema_field = GraphQLField(
        "A", gql_type=GraphQLList(gql_type=GraphQLNonNull(gql_type="F"))
    )
    assert _resolver_executor_mock.contains_not_null

    _resolver_executor_mock._schema_field = GraphQLField(
        "A", gql_type=GraphQLList(gql_type="F")
    )
    assert not _resolver_executor_mock.contains_not_null
