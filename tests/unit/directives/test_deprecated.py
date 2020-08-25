import pytest


@pytest.mark.asyncio
async def test_deprecated_on_introspection():
    from unittest.mock import Mock

    from tartiflette.directive.builtins.deprecated import DeprecatedDirective

    areturn_value = Mock()
    c = Mock(return_value=areturn_value)

    async def d2(*args, **kwargs):
        return c(*args, **kwargs)

    aschema = Mock()

    await DeprecatedDirective().on_post_bake({"reason": "A"}, d2, aschema)
    assert areturn_value.isDeprecated
    assert areturn_value.deprecationReason == "A"
    assert c.called_with(aschema)
