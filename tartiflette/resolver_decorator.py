from inspect import iscoroutinefunction

from tartiflette.schema import DefaultGraphQLSchema
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
    def __init__(self, name: str, schema=None):
        self._schema = schema if schema else DefaultGraphQLSchema
        self.field = self._schema.get_field_by_name(name=name)

    def __call__(self, resolver, *args, **kwargs):
        if not iscoroutinefunction(resolver):
            raise TartifletteNonAwaitableResolver(
                "The resolver `{}` given for the field `{}` "
                "is not awaitable.".format(repr(resolver), self.field.name))
        if self.field:
            self.field.resolver = resolver
        return resolver
