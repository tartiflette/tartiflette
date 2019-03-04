def test_deprecated_on_introspection():
    from tartiflette.directive.deprecated import Deprecated
    from unittest.mock import Mock

    areturn_value = Mock()
    d2 = Mock(return_value=areturn_value)
    aschema = Mock()

    Deprecated.on_introspection({"reason": "A"}, d2, aschema, None, None)

    assert areturn_value.isDeprecated
    assert areturn_value.deprecationReason == "A"

    assert d2.called_with(aschema)
