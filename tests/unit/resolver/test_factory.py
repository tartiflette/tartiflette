import pytest
from unittest.mock import Mock


def test_resolver_factory__built_in_coercer():
    from tartiflette.resolver.factory import _built_in_coercer

    func = Mock(return_value="a")

    assert _built_in_coercer(func, 1, None) == "a"
    assert func.call_args_list == [((1,),)]


def test_resolver_factory__built_in_coercer_none_val():
    from tartiflette.resolver.factory import _built_in_coercer

    func = Mock(return_value="a")
    assert _built_in_coercer(func, None, None) is None
    assert func.called is False


def test_resolver_factory__object_coercer():
    from tartiflette.resolver.factory import _object_coercer

    assert _object_coercer(None, None, None) == {}


def test_resolver_factory__list_coercer():
    from tartiflette.resolver.factory import _list_coercer

    func = Mock(return_value="a")
    info = Mock()

    assert _list_coercer(func, "r", info) == ["a"]
    assert func.call_args_list == [(("r", info),)]


def test_resolver_factory__list_coercer_is_alist():
    from tartiflette.resolver.factory import _list_coercer

    func = Mock(return_value="a")
    info = Mock()

    assert _list_coercer(func, ["r", "d"], info) == ["a", "a"]
    assert func.call_args_list == [(("r", info),), (("d", info),)]


def test_resolver_factory__list_coercer_none_val():
    from tartiflette.resolver.factory import _list_coercer

    func = Mock(return_value="a")
    assert _list_coercer(func, None, None) is None
    assert func.called is False


def test_resolver_factory__not_null_coercer():
    from tartiflette.resolver.factory import _not_null_coercer

    func = Mock(return_value="a")
    info = Mock()

    assert _not_null_coercer(func, "T", info) == "a"
    assert func.call_args_list == [(("T", info),)]


def test_resolver_factory__not_null_coercer_none_value():
    from tartiflette.resolver.factory import _not_null_coercer
    from tartiflette.types.exceptions.tartiflette import NullError

    func = Mock(return_value="a")
    info = Mock()

    with pytest.raises(NullError):
        assert _not_null_coercer(func, None, info)
    assert func.called is False
