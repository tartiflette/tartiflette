import functools
from inspect import iscoroutinefunction
from typing import Callable, Optional

from tartiflette.executors.types import Info
from tartiflette.schema import DefaultGraphQLSchema, GraphQLSchema
from tartiflette.types.exceptions.tartiflette import NonAwaitableResolver


def wrap_resolver(resolver):
    """
    Currenty unused, this allows an easy wrapping of resolvers
    (for hooks, middlewares etc.)

    :param resolver: The field resolver
    :return: Any: the resolver result
    """

    @functools.wraps(resolver)
    async def wrapper(parent, arguments, request_ctx, info: Info):
        return await resolver(parent, arguments, request_ctx, info)

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
        def field_resolver(parent, arguments, request_ctx, info):
            ... do your stuff
            return 42

    """

    def __init__(self, name: str, schema: Optional[GraphQLSchema] = None):
        self.schema = schema if schema else DefaultGraphQLSchema
        self.field = self.schema.get_field_by_name(name=name)

    def __call__(self, resolver: Callable, *args, **kwargs):
        if not iscoroutinefunction(resolver):
            raise NonAwaitableResolver(
                "The resolver `{}` given for the field `{}` "
                "is not awaitable.".format(repr(resolver), self.field.name)
            )

        try:
            self.field.resolver = wrap_resolver(
                resolver
            )
        except AttributeError:
            pass

        return resolver
