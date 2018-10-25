from inspect import iscoroutinefunction
from typing import Callable

from tartiflette.types.exceptions.tartiflette import (
    NonAwaitableResolver,
    UnknownDirectiveDefinition,
)
from tartiflette.schema.registry import SchemaRegistry


class Resolver:
    """
    This decorator allows you to link a GraphQL Schema field to a resolver.

    For example, for the following SDL:

        type SomeObject {
            field: Int
        }

    Use the Resolver decorator the following way:

        @Resolver("SomeObject.field")
        def field_resolver(parent, arguments, request_ctx, info):
            do your stuff
            return 42
    """

    def __init__(self, name: str, schema_name: str = "default"):
        self._name = name
        self._implementation = None
        self._schema_name = schema_name

    def bake(self, schema):
        if not self._implementation:
            raise Exception("No implementation given")

        try:
            field = schema.get_field_by_name(self._name)
            field.resolver.update_func(self._implementation)

        except KeyError:
            raise UnknownDirectiveDefinition(
                "Unknow Directive Definition %s" % self._name
            )

    def __call__(self, resolver: Callable):
        if not iscoroutinefunction(resolver):
            raise NonAwaitableResolver(
                "The resolver `{}` given is not awaitable.".format(
                    repr(resolver)
                )
            )

        SchemaRegistry.register_resolver(self._schema_name, self)
        self._implementation = resolver
        return resolver
