from inspect import iscoroutinefunction

from tartiflette.schema import DefaultGraphQLSchema, GraphQLSchema
from tartiflette.types.exceptions.tartiflette import \
    TartifletteNonAwaitableResolver


class Resolver:
    """
    Resolver is a decorator to link a resolver with a field defined in
    your Schema Definition Language.

    For example, for the following SDL:

        type SomeObject {
            field: Int
        }

    Use Resolver the following way:

        @Resolver("SomeObject.field")
        def field_resolver(ctx, execution_data):
            ... do stuff
            return 42
    """
    def __init__(self, name: str, schema: GraphQLSchema=None):
        self.schema = schema if schema else DefaultGraphQLSchema
        self.field = self.schema.get_field_by_name(name=name)

    def __call__(self, resolver, *args, **kwargs):
        if not iscoroutinefunction(resolver):
            raise TartifletteNonAwaitableResolver(
                "The resolver `{}` given for the field `{}` "
                "is not awaitable.".format(repr(resolver), self.field.name))
        try:
            async def resolver_wrapper(*args, **kwargs):
                return self.schema.to_value(
                    self.field.gql_type,
                    await resolver(*args, **kwargs)
                )
            self.field.resolver = resolver_wrapper
        except AttributeError:
            pass
        return resolver
