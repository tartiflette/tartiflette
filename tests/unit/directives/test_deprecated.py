import pytest


@pytest.mark.asyncio
async def test_deprecated_on_introspection():
    from tartiflette.directive.deprecated import Deprecated
    from unittest.mock import Mock

    areturn_value = Mock()
    c = Mock(return_value=areturn_value)

    async def d2(*args, **kwargs):
        return c(*args, **kwargs)

    aschema = Mock()

    await Deprecated.on_introspection({"reason": "A"}, d2, aschema, None, None)

    assert areturn_value.isDeprecated
    assert areturn_value.deprecationReason == "A"

    assert c.called_with(aschema)
