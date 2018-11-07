from unittest.mock import Mock


def test_non_introspectable_introspection():
    from tartiflette.directive.non_introspectable import NonIntrospectable

    assert NonIntrospectable.on_introspection(Mock(), Mock(), Mock()) is None
