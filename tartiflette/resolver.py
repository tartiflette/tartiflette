import functools
from inspect import iscoroutinefunction
from typing import Optional, Callable

from tartiflette.executors.types import ExecutionData
from tartiflette.schema import DefaultGraphQLSchema, GraphQLSchema
from tartiflette.types.exceptions.tartiflette import \
    NonAwaitableResolver


def wrap_resolver(schema, field, resolver):
    """
    Currenty unused, this allows an easy wrapping of resolvers
    (for hooks, middlewares etc.)

    :param schema: The current schema
    :param field: The current field
    :param resolver: The field resolver
    :return: Any: the resolver result
    """

    @functools.wraps(resolver)
    async def wrapper(request_ctx, execution_data: ExecutionData):
        return await resolver(request_ctx, execution_data)

    return wrapper


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

        try:
            self.field.resolver = wrap_resolver(self.schema,
                                                self.field,
                                                resolver)
        except AttributeError:
            pass

        return resolver
