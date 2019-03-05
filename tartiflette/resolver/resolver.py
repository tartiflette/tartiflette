from inspect import iscoroutinefunction
from typing import Callable

from tartiflette.schema.registry import SchemaRegistry
from tartiflette.types.exceptions.tartiflette import (
    MissingImplementation,
    NonAwaitableResolver,
    UnknownFieldDefinition,
)


class Resolver:
    """
    This decorator allows you to link a GraphQL Schema field to a resolver.

    For example, for the following SDL:

        type SomeObject {
            field: Int
        }

    Use the Resolver decorator the following way:

        @Resolver("SomeObject.field")
        async def field_resolver(parent, arguments, request_ctx, info):
            do your stuff
            return 42
    """

    def __init__(self, name: str, schema_name: str = "default") -> None:
        self._name = name
        self._implementation = None
        self._schema_name = schema_name

    @property
    def name(self) -> str:
        return self._name

    def bake(self, schema: "GraphQLSchema") -> None:
        if not self._implementation:
            raise MissingImplementation(
                "No implementation given for resolver < %s >" % self._name
            )

        try:
            field = schema.get_field_by_name(self._name)
            field.resolver.update_func(self._implementation)
        except KeyError:
            raise UnknownFieldDefinition(
                "Unknown Field Definition %s" % self._name
            )

    def __call__(self, resolver: Callable) -> Callable:
        if not iscoroutinefunction(resolver):
            raise NonAwaitableResolver(
                "The resolver `{}` given is not awaitable.".format(
                    repr(resolver)
                )
            )

        SchemaRegistry.register_resolver(self._schema_name, self)
        self._implementation = resolver
        return resolver
