from inspect import iscoroutinefunction
from typing import Optional, Callable

from tartiflette.executors.types import ExecutionData
from tartiflette.schema import DefaultGraphQLSchema, GraphQLSchema
from tartiflette.types.exceptions.tartiflette import \
    NonAwaitableResolver


class Resolver:
    """
    This decorator allows you to link a GraphQL Schema field to a resolver.

    For example, for the following SDL:

        type SomeObject {
            field: Int
        }

    Use the Resolver decorator the following way:

        @Resolver("SomeObject.field")
        def field_resolver(ctx, execution_data):
            ... do your stuff
            return 42

    """
    def __init__(self, name: str, schema: Optional[GraphQLSchema]=None):
        self.schema = schema if schema else DefaultGraphQLSchema
        self.field = self.schema.get_field_by_name(name=name)

    def __call__(self, resolver: Callable, *args, **kwargs):
        if not iscoroutinefunction(resolver):
            raise NonAwaitableResolver(
                "The resolver `{}` given for the field `{}` "
                "is not awaitable.".format(repr(resolver), self.field.name))

        async def resolver_wrapper(request_ctx, execution_data: ExecutionData):
            return self.schema.collect_field_value(
                self.field,
                await resolver(request_ctx, execution_data),
                execution_data,
            )

        try:
            self.field.resolver = resolver_wrapper
        except AttributeError:
            pass

        return resolver
