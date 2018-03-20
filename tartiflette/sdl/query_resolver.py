from tartiflette.sdl.schema import DefaultGraphQLSchema


class QueryResolver(object):
    def __init__(self, name: str, schema=None):
        self._schema = schema if schema else DefaultGraphQLSchema
        self.field = self._schema.get_field_by_name(name=name)

    def __call__(self, resolver, *args, **kwargs):
        if self.field:
            self.field.resolver = resolver
        return resolver
