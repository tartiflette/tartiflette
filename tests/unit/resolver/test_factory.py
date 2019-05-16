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
    from tartiflette.resolver.factoryyy import _shall_return_a_list

    assert _shall_return_a_list(field_type) == expected


@pytest.mark.asyncio
async def test_resolver_factory_default_resolver():
    from tartiflette.resolver.factoryyy import default_resolver

    info = Mock()
    info.schema_field = Mock()
    info.schema_field.name = "aField"

    assert await default_resolver(None, None, None, info) is None

    bob = Mock()
    bob.aField = "Lol"

    assert await default_resolver(bob, None, None, info) == "Lol"
    assert await default_resolver({"aField": "TTP"}, None, None, info) == "TTP"


def test_resolver_factory_resolver_executor_factory():
    from tartiflette.resolver.factoryyy import ResolverExecutorFactory
    from tartiflette.resolver.factoryyy import default_resolver

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
    from tartiflette.resolver.factoryyy import (
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
    with patch(
        "tartiflette.resolver.factory.wraps_with_directives"
    ) as wraps_with_directives_mock:
        from tartiflette.resolver.factoryyy import (
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

            wraps_with_directives_mock.assert_called_once_with(
                directives_definition=schema_field.directives,
                directive_hook="on_field_execution",
                func=resolver_executor._raw_func,
            )
