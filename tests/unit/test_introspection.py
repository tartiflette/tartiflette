from unittest.mock import Mock

import pytest


@pytest.mark.asyncio
async def test_introspection___schema_resolver():
    from tartiflette.schema.introspection import __schema_resolver

    info = Mock()
    info.is_introspection = False
    info.schema = Mock()

    sch = await __schema_resolver(None, None, None, info)

    assert sch == info.schema
    assert info.is_introspection


@pytest.mark.asyncio
async def test_introspection___type_resolver():
    from tartiflette.schema.introspection import __type_resolver

    info = Mock()
    info.is_introspection = False
    info.schema = Mock()
    info.schema.find_type = Mock(return_value="Ninja")

    args = {"name": "LOL"}

    atype = await __type_resolver(None, args, None, info)

    assert info.is_introspection
    assert atype == "Ninja"
    assert info.schema.find_type.called_with("LOL")


def _get_parent_results_mock(typename):
    a = Mock()
    a._typename = typename
    return a
