from typing import Callable, Optional

from tartiflette.schema import DefaultGraphQLSchema, GraphQLSchema


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
        self.directive = self.schema.directives[name]

    def __call__(self, implementation: Callable, *args, **kwargs):
        self.directive.implementation = implementation
        return implementation
