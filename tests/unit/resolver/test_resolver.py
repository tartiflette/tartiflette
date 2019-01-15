from unittest.mock import Mock, patch

import pytest


def test_resolver_resolver_resolver_inst():
    from tartiflette.resolver.resolver import Resolver

    r = Resolver("a")
    assert r._implementation is None
    assert r._schema_name == "default"
    assert r._name == "a"


@pytest.fixture
def a_resolver():
    from tartiflette.resolver.resolver import Resolver

    a_resolver = Resolver("a_resolver")
    a_resolver._implementation = "A"
    return a_resolver


def test_resolver_resolver_resolver_bake_raises(a_resolver):
    from tartiflette.types.exceptions.tartiflette import UnknownFieldDefinition

    sch = Mock()
    sch.get_field_by_name = Mock(side_effect=KeyError())

    with pytest.raises(UnknownFieldDefinition):
        a_resolver.bake(sch)
    assert sch.get_field_by_name.call_args_list == [(("a_resolver",),)]

    a_resolver._implementation = None

    with pytest.raises(Exception):
        a_resolver.bake(None)


def test_resolver_resolver_resolver_bake(a_resolver):
    a_field = Mock()
    a_field.resolver = Mock()
    a_field.resolver.update_func = Mock()
    sch = Mock()
    sch.get_field_by_name = Mock(return_value=a_field)

    assert a_resolver.bake(sch) is None
    assert sch.get_field_by_name.call_args_list == [(("a_resolver",),)]
    assert a_field.resolver.update_func.call_args_list == [(("A",),)]


def test_resolver_resolver_resolver___call__(a_resolver):
    from tartiflette.types.exceptions.tartiflette import NonAwaitableResolver

    with pytest.raises(NonAwaitableResolver):

        def a():
            pass

        a_resolver(a)

    async def b():
        pass

    with patch(
        "tartiflette.schema.registry.SchemaRegistry.register_resolver"
    ) as mocked:
        r = a_resolver(b)
        assert r is b
        assert mocked.call_args_list == [(("default", a_resolver),)]
        assert a_resolver._implementation is b
