from tartiflette.schema.registry import SchemaRegistry
from tartiflette.types.exceptions.tartiflette import (
    MissingImplementation,
    UnknownDirectiveDefinition,
)


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
                "No implementation given for directive < %s >" % self._name
            )

        try:
            directive = schema.find_directive(self._name)
            directive.implementation = self._implementation
        except KeyError:
            raise UnknownDirectiveDefinition(
                "Unknow Directive Definition %s" % self._name
            )

    def __call__(self, implementation):
        self._implementation = implementation

        SchemaRegistry.register_directive(self._schema_name, self)

        return implementation
