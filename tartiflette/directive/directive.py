from asyncio import iscoroutinefunction
from typing import Callable, Optional

from tartiflette.types.exceptions.tartiflette import (
    UnknownDirectiveDefinition,
    NonAwaitableDirective,
)


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

    def __init__(self, name: str, schema):
        self.schema = schema
        try:
            self.directive = self.schema.directives[name]
        except KeyError:
            raise UnknownDirectiveDefinition(
                "Unknow Directive Definition %s" % name
            )

    def __call__(self, implementation: Callable, *_args, **_kwargs):
        if not iscoroutinefunction(
            implementation.on_execution
        ) or not iscoroutinefunction(implementation.on_introspection):
            raise NonAwaitableDirective(
                "%s is not awaitable" % repr(implementation)
            )
        self.directive.implementation = implementation
        self.schema.prepare_directives()
        return implementation
