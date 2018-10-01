from asyncio import iscoroutinefunction

from tartiflette.types.exceptions.tartiflette import (
    UnknownDirectiveDefinition,
    NonAwaitableDirective,
)
from tartiflette.schema.registry import SchemaRegistry


class Directive:
    """
    This decorator allows you to link a GraphQL Directive to a Directive class.

    For example, for the following SDL:

        directive @deprecated(
            reason: String = "No longer supported"
        ) on FIELD_DEFINITION | ENUM_VALUE

    Use the Directive decorator the following way:

        @Directive("deprecated")
        class MyDirective:
            ... callbacks here ...

    """

    def __init__(self, name: str, schema_name="default"):
        self._name = name
        self._implementation = None
        self._schema_name = schema_name

    def bake(self, schema):
        if not self._implementation:
            raise Exception("No implementation given")

        try:
            directive = schema.find_directive(self._name)
            directive.implementation = self._implementation
        except KeyError:
            raise UnknownDirectiveDefinition(
                "Unknow Directive Definition %s" % self._name
            )

    def __call__(self, implementation):
        if not iscoroutinefunction(implementation.on_execution):
            raise NonAwaitableDirective(
                "%s is not awaitable" % repr(implementation)
            )

        SchemaRegistry.register_directive(self._schema_name, self)

        self._implementation = implementation
        return implementation
