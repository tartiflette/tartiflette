from unittest.mock import Mock, patch

import pytest


def test_scalar_custom_scalar_inst():
    from tartiflette.scalar.scalar import Scalar

    s = Scalar("A")
    assert s.name == "A"
    assert s._implementation is None
    assert s._schema_name == "default"


@pytest.fixture
def a_scalar():
    from tartiflette.scalar.scalar import Scalar

    return Scalar("A")


def test_scalar_custom_scalar_bake_raises(a_scalar):
    from tartiflette.types.exceptions.tartiflette import (
        UnknownScalarDefinition,
    )

    with pytest.raises(Exception):
        a_scalar.bake(None)

    sch = Mock()
    sch.find_scalar = Mock(return_value=None)

    a_scalar._implementation = "A"

    with pytest.raises(UnknownScalarDefinition):
        a_scalar.bake(sch)

    assert sch.find_scalar.call_args_list == [(("A",),)]


def test_scalar_custom_scalar_bake(a_scalar):
    a_gql_scalar = Mock()

    sch = Mock()
    sch.find_scalar = Mock(return_value=a_gql_scalar)

    a_scalar._implementation = Mock()
    a_scalar._implementation.coerce_output = Mock()
    a_scalar._implementation.coerce_input = Mock()

    assert a_scalar.bake(sch) is None
    assert a_gql_scalar.coerce_output is a_scalar._implementation.coerce_output
    assert a_gql_scalar.coerce_input is a_scalar._implementation.coerce_input
    assert sch.find_scalar.call_args_list == [(("A",),)]


def test_scalar_custom_scalar___call__(a_scalar):
    with patch(
        "tartiflette.schema.registry.SchemaRegistry.register_scalar",
        return_value=None,
    ) as mocked_register:
        r = a_scalar("R")
        assert r == "R"
        assert mocked_register.call_args_list == [(("default", a_scalar),)]
        assert a_scalar._implementation == "R"
