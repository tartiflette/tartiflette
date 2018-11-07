from unittest.mock import Mock
import pytest


def test_directive_implementation():
    from tartiflette.directive.directive import Directive

    class NTM:
        async def on_execution(self, *args, **kwargs):
            pass

    a_directive = Directive("deprecated", schema_name="Ninja")

    assert a_directive(NTM) == NTM


def test_directive_implementation_except():
    from tartiflette.directive.directive import Directive
    from tartiflette.types.exceptions.tartiflette import NonAwaitableDirective

    class NTM:
        def on_execution(self, *args, **kwargs):
            pass

    a_directive = Directive("deprecated", schema_name="Ninja")

    with pytest.raises(NonAwaitableDirective):
        a_directive(NTM)


def test_directive_bake_except_no_implem():
    from tartiflette.directive.directive import Directive

    a_directive = Directive("deprecated", schema_name="Ninja")

    with pytest.raises(Exception):
        a_directive.bake(Mock())


def test_directive_bake_except_unknowdirective():
    from tartiflette.directive.directive import Directive
    from tartiflette.types.exceptions.tartiflette import (
        UnknownDirectiveDefinition,
    )

    a_directive = Directive("deprecated", schema_name="Ninja")

    def schema_find_directive(*_args, **_kwargs):
        raise KeyError

    schema = Mock()
    schema.find_directive = schema_find_directive

    class NTM:
        async def on_execution(self, *args, **kwargs):
            pass

    a_directive(NTM)

    with pytest.raises(UnknownDirectiveDefinition):
        a_directive.bake(schema)


def test_directive_bake():
    from tartiflette.directive.directive import Directive

    a_directive = Directive("deprecated", schema_name="Ninja")
    directive_internal = Mock()

    def schema_find_directive(*_args, **_kwargs):
        return directive_internal

    schema = Mock()
    schema.find_directive = schema_find_directive

    class NTM:
        async def on_execution(self, *args, **kwargs):
            pass

    a_directive(NTM)

    assert a_directive.bake(schema) is None
    assert directive_internal.implementation == NTM
