from unittest.mock import Mock

import pytest


@pytest.mark.asyncio
async def test_introspection___schema_resolver():
    from tartiflette.schema.introspection import __schema_resolver

    info = Mock()
    info.execution_ctx = Mock()
    info.execution_ctx.is_introspection = False
    info.schema = Mock()

    sch = await __schema_resolver(None, None, None, info)

    assert sch == info.schema
    assert info.execution_ctx.is_introspection is True


@pytest.mark.asyncio
async def test_introspection___type_resolver():
    from tartiflette.schema.introspection import __type_resolver

    info = Mock()
    info.execution_ctx = Mock()
    info.execution_ctx.is_introspection = False
    info.schema = Mock()
    info.schema.find_type = Mock(return_value="Ninja")

    args = {"name": "LOL"}

    atype = await __type_resolver(None, args, None, info)

    assert info.execution_ctx.is_introspection is True
    assert atype == "Ninja"
    assert info.schema.find_type.called_with("LOL")


def _get_parent_results_mock(typename):
    a = Mock()
    a._typename = typename
    return a


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "parent_result,expected",
    [
        (_get_parent_results_mock("LOL"), "LOL2"),
        (_get_parent_results_mock("dontcare"), "Ninja"),
    ],
)
async def test_introspection___typename_resolver(parent_result, expected):
    from tartiflette.schema.introspection import __typename_resolver

    def my_find_type(name):
        if name == "LOL":
            return "LOL2"

        raise AttributeError("Ninja")

    info = Mock()
    info.schema_field = Mock()
    info.schema_field.schema = Mock()
    info.schema_field.schema.find_type = my_find_type
    info.schema_field.parent_type = "Ninja"

    r = await __typename_resolver(parent_result, None, None, info)

    assert r == expected
