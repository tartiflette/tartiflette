from unittest.mock import Mock, patch

import pytest

from tartiflette.types.list import GraphQLList
from tartiflette.types.non_null import GraphQLNonNull


@pytest.mark.parametrize(
    "field_type,expected",
    [
        (GraphQLList(gql_type="aType"), True),
        (GraphQLNonNull(gql_type="aType"), False),
        (GraphQLNonNull(gql_type=GraphQLList(gql_type="aType")), True),
        (None, False),
    ],
)
def test_resolver_factory__shall_return_a_list(field_type, expected):
    from tartiflette.resolver.factory import _shall_return_a_list

    assert _shall_return_a_list(field_type) == expected


def test_resolver_factory__surround_with_execution_directives():
    from tartiflette.resolver.factory import (
        _surround_with_execution_directives,
    )

    cllbs_a = Mock()
    cllbs_a.on_field_execution = Mock()
    cllbs_b = Mock()
    cllbs_b.on_field_execution = Mock()

    directives = [
        {"callables": cllbs_a, "args": {"a": "b"}},
        {"callables": cllbs_b, "args": {"c": "d"}},
    ]

    r = _surround_with_execution_directives("A", directives)
    assert r is not None
    assert r.func is cllbs_a.on_field_execution
    a, b = r.args
    assert a == {"a": "b"}
    assert b.func is cllbs_b.on_field_execution
    a, b = b.args
    assert a == {"c": "d"}
    assert b == "A"

    assert _surround_with_execution_directives("A", []) == "A"


def test_resolver_factory__introspection_directive_endpoint():
    from tartiflette.resolver.factory import _introspection_directive_endpoint

    assert _introspection_directive_endpoint("A") == "A"
    assert _introspection_directive_endpoint(None) is None


@pytest.fixture
def directive_list_mock():
    cllbs_a = Mock()
    cllbs_a.on_introspection = Mock(return_val="intro_a")
    cllbs_b = Mock()
    cllbs_b.on_introspection = Mock(return_val="intro_b")

    directives = [
        {"callables": cllbs_a, "args": {"a": "b"}},
        {"callables": cllbs_b, "args": {"c": "d"}},
    ]
    return directives


def test_resolver_factory__introspection_directives(directive_list_mock):
    from tartiflette.resolver.factory import _introspection_directives
    from tartiflette.resolver.factory import _introspection_directive_endpoint

    r = _introspection_directives(directive_list_mock)
    assert r is not None
    assert r.func is directive_list_mock[0]["callables"].on_introspection
    a, b = r.args
    assert a == directive_list_mock[0]["args"]
    assert b.func is directive_list_mock[1]["callables"].on_introspection
    a, b = b.args
    assert a == directive_list_mock[1]["args"]
    assert b is _introspection_directive_endpoint

    assert _introspection_directives([]) is _introspection_directive_endpoint


def test_resolver_factory__execute_introspection_directives(
    directive_list_mock
):
    from tartiflette.resolver.factory import _execute_introspection_directives

    elements = ["A", "B"]

    assert _execute_introspection_directives(elements, None, None) == elements

    elem = Mock()
    elem.directives = directive_list_mock

    assert _execute_introspection_directives([elem], None, None) is not None
    directive_list_mock[0]["callables"].on_introspection.assert_called_once()


@pytest.mark.asyncio
async def test_resolver_factory_default_resolver():
    from tartiflette.resolver.factory import default_resolver

    info = Mock()
    info.schema_field = Mock()
    info.schema_field.name = "aField"

    assert await default_resolver(None, None, None, info) is None

    bob = Mock()
    bob.aField = "Lol"

    assert await default_resolver(bob, None, None, info) == "Lol"
    assert await default_resolver({"aField": "TTP"}, None, None, info) == "TTP"


def test_resolver_factory_resolver_executor_factory():
    from tartiflette.resolver.factory import ResolverExecutorFactory
    from tartiflette.resolver.factory import default_resolver

    field = Mock()
    field.gql_type = "aType"
    field.schema = None

    res_ex = ResolverExecutorFactory.get_resolver_executor("A", field)
    assert res_ex._raw_func == "A"
    assert res_ex._schema_field == field

    res_ex = ResolverExecutorFactory.get_resolver_executor(None, field)
    assert res_ex._raw_func is default_resolver
    assert res_ex._schema_field == field


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "parent_result",
    [
        None,
        1,
        "value",
        {
            "none": None,
            "int": 1,
            "string": "value",
            "dict": {"value": "value"},
        },
    ],
)
async def test_default_subscription_resolver(parent_result):
    from tartiflette.resolver.factory import (
        default_resolver,
        default_subscription_resolver,
    )

    info = Mock()
    info.schema_field = Mock()
    info.schema_field.name = "myField"

    default_resolver_mock = Mock(wraps=default_resolver)

    subscription_resolver = default_subscription_resolver(
        default_resolver_mock
    )

    assert (
        await subscription_resolver(parent_result, None, None, info)
        == parent_result
    )

    default_resolver_mock.assert_called_once_with(
        {"myField": parent_result}, None, None, info
    )


_CUSTOM_DEFAULT_RESOLVER = lambda *args, **kwargs: {}


@pytest.mark.parametrize(
    (
        "is_subscription",
        "custom_default_resolver",
        "update_func_called",
        "default_subscription_resolver_called",
    ),
    [
        (False, None, False, False),
        (True, None, False, True),
        (False, _CUSTOM_DEFAULT_RESOLVER, True, False),
        (True, _CUSTOM_DEFAULT_RESOLVER, True, False),
    ],
)
def test_resolverexecutor_bake(
    is_subscription,
    custom_default_resolver,
    update_func_called,
    default_subscription_resolver_called,
):
    from tartiflette.resolver.factory import (
        _ResolverExecutor,
        default_resolver,
        default_subscription_resolver,
    )

    schema_field = Mock(schema=None)
    schema_field.directives = Mock()
    schema_field.subscribe = Mock() if is_subscription else None

    with patch(
        "tartiflette.resolver.factory.default_subscription_resolver",
        wraps=default_subscription_resolver,
    ) as default_subscription_resolver_mock:
        with patch(
            "tartiflette.resolver.factory._surround_with_execution_directives"
        ) as surround_with_execution_directives_mock:
            resolver_executor = _ResolverExecutor(
                default_resolver, schema_field
            )
            resolver_executor.update_coercer = Mock()
            resolver_executor.update_func = Mock(
                wraps=resolver_executor.update_func
            )

            resolver_executor.bake(custom_default_resolver)

            resolver_executor.update_coercer.assert_called_once()

            if update_func_called:
                resolver_executor.update_func.assert_called_once_with(
                    custom_default_resolver
                )
            else:
                resolver_executor.update_func.assert_not_called()

            if default_subscription_resolver_called:
                default_subscription_resolver_mock.assert_called_once_with(
                    default_resolver
                )
            else:
                default_subscription_resolver_mock.assert_not_called()

            surround_with_execution_directives_mock.assert_called_once_with(
                resolver_executor._raw_func, schema_field.directives
            )
