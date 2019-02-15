from unittest.mock import Mock, patch

import pytest


def test_subscription_inst():
    from tartiflette.resolver.subscription import Subscription

    r = Subscription("a")
    assert r._implementation is None
    assert r._schema_name == "default"
    assert r._name == "a"


@pytest.fixture
def a_subscription():
    from tartiflette.resolver.subscription import Subscription

    a_subscription = Subscription("a_subscription")
    a_subscription._implementation = "A"
    return a_subscription


def test_subscription_bake_raise_missing_implementation(a_subscription):
    from tartiflette.types.exceptions.tartiflette import MissingImplementation

    schema_mock = Mock()

    a_subscription._implementation = None

    with pytest.raises(MissingImplementation):
        a_subscription.bake(schema_mock)


def test_subscription_bake_unknown_field_definition(a_subscription):
    from tartiflette.types.exceptions.tartiflette import UnknownFieldDefinition

    a_field_mock = Mock()
    a_field_mock.parent_type = Mock()

    schema_mock = Mock()
    schema_mock.get_field_by_name = Mock(side_effect=KeyError())

    with pytest.raises(UnknownFieldDefinition):
        a_subscription.bake(schema_mock)

    assert schema_mock.get_field_by_name.call_args_list == [
        (("a_subscription",),)
    ]


def test_subscription_bake_not_subscription_field(a_subscription):
    from tartiflette.types.exceptions.tartiflette import NotSubscriptionField

    schema_mock = Mock()
    schema_mock.subscription_type = "Subscription"
    schema_mock.find_type = Mock()

    with pytest.raises(NotSubscriptionField):
        a_subscription.bake(schema_mock)

    assert schema_mock.find_type.call_args_list == [(("Subscription",),)]


def test_subscription_bake(a_subscription):
    subscription_type_mock = Mock()

    a_field_mock = Mock()
    a_field_mock.parent_type = subscription_type_mock

    schema_mock = Mock()
    schema_mock.get_field_by_name = Mock(return_value=a_field_mock)
    schema_mock.find_type = Mock(return_value=subscription_type_mock)

    assert a_subscription.bake(schema_mock) is None
    assert schema_mock.get_field_by_name.call_args_list == [
        (("a_subscription",),)
    ]
    assert a_field_mock.subscribe is a_subscription._implementation


def test_subscription__call__not_async_generator(a_subscription):
    from tartiflette.types.exceptions.tartiflette import (
        NonAsyncGeneratorSubscription,
    )

    with pytest.raises(NonAsyncGeneratorSubscription):

        def implementation():
            pass

        a_subscription(implementation)


def test_subscription__call__(a_subscription):
    async def implementation():
        yield None

    with patch(
        "tartiflette.schema.registry.SchemaRegistry.register_subscription"
    ) as register_subscription_mock:
        subscription = a_subscription(implementation)
        assert subscription is implementation
        assert register_subscription_mock.call_args_list == [
            (("default", a_subscription),)
        ]
        assert a_subscription._implementation is implementation
