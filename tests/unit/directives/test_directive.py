from unittest.mock import Mock

import pytest


def test_directive_implementation():
    from tartiflette.directive.directive import Directive

    class dontcare:
        async def on_field_execution(self, *args, **kwargs):
            pass

    a_directive = Directive("deprecated", schema_name="Ninja")

    assert a_directive(dontcare) == dontcare


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

    a_directive = Directive("deprecated", schema_name="Ninja3")

    def schema_find_directive(*_args, **_kwargs):
        raise KeyError

    schema = Mock()
    schema.find_directive = schema_find_directive

    class dontcare:
        async def on_field_execution(self, *args, **kwargs):
            pass

    a_directive(dontcare)

    with pytest.raises(UnknownDirectiveDefinition):
        a_directive.bake(schema)


def test_directive_bake(clean_registry):
    from tartiflette.directive.directive import Directive

    a_directive = Directive("deprecated", schema_name="Ninja")
    directive_internal = Mock()

    def schema_find_directive(*_args, **_kwargs):
        return directive_internal

    schema = Mock()
    schema.find_directive = schema_find_directive

    class dontcare:
        async def on_field_execution(self, *args, **kwargs):
            pass

    a_directive(dontcare)

    assert a_directive.bake(schema) is None
    assert isinstance(directive_internal.implementation, dontcare)
