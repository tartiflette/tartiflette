from inspect import iscoroutinefunction
from typing import Callable, Optional

from tartiflette.schema import DEFAULT_GRAPHQL_SCHEMA, GraphQLSchema
from tartiflette.types.exceptions.tartiflette import NonAwaitableResolver


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

    def __init__(self, name: str, schema: Optional[GraphQLSchema] = None):
        self.schema = schema if schema else DEFAULT_GRAPHQL_SCHEMA
        self.field = self.schema.get_field_by_name(name=name)

    def __call__(self, resolver: Callable, *args, **kwargs):
        if not iscoroutinefunction(resolver):
            raise NonAwaitableResolver(
                "The resolver `{}` given for the field `{}` "
                "is not awaitable.".format(repr(resolver), self.field.name)
            )

        self.field.resolver.update_func(resolver)

        return self.field.resolver
