from asyncio import iscoroutinefunction
from typing import Callable, Optional

from tartiflette.schema import DefaultGraphQLSchema, GraphQLSchema
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

    def __init__(self, name: str, schema: Optional[GraphQLSchema] = None):
        self.schema = schema if schema else DefaultGraphQLSchema
        try:
            self.directive = self.schema.directives[name]
        except KeyError:
            raise UnknownDirectiveDefinition(
                "Unknow Directive Definition %s" % name
            )

    def __call__(self, implementation: Callable, *_args, **_kwargs):
        if not iscoroutinefunction(implementation):
            raise NonAwaitableDirective(
                "The resolver `{}` given for the field `{}` "
                "is not awaitable.".format(repr(implementation), self.name)
            )

        self.directive.implementation = implementation
        return implementation
