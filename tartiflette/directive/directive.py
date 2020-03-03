from inspect import isclass
from typing import Any, Callable, Optional

from tartiflette.schema.registry import SchemaRegistry
from tartiflette.types.exceptions.tartiflette import (
    MissingImplementation,
    UnknownDirectiveDefinition,
)

__all__ = ("Directive",)


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

    def __init__(
        self,
        name: str,
        schema_name: str = "default",
        arguments_coercer: Optional[Callable] = None,
    ) -> None:
        """
        :param name: name of the directive
        :param schema_name: name of the schema to which link the directive
        :param arguments_coercer: callable to use to coerce directive arguments
        :type name: str
        :type schema_name: str
        :type arguments_coercer: Optional[Callable]
        """
        self.name = name
        self._implementation = None
        self._schema_name = schema_name
        self._arguments_coercer = arguments_coercer

    def bake(self, schema: "GraphQLSchema") -> None:
        """
        Sets the directive implementation into the schema directive definition.
        :param schema: the GraphQLSchema instance linked to the directive
        :type schema: GraphQLSchema
        """
        if not self._implementation:
            raise MissingImplementation(
                f"No implementation given for directive < {self.name} >"
            )

        try:
            directive = schema.find_directive(self.name)
            directive.implementation = self._implementation
            directive.arguments_coercer = (
                self._arguments_coercer or schema.default_arguments_coercer
            )
        except KeyError:
            raise UnknownDirectiveDefinition(
                f"Unknown Directive Definition {self.name}"
            )

    def __call__(self, implementation: type) -> Any:
        """
        Registers the directive into the schema.
        :param implementation: implementation of the directive
        :type implementation: type
        :return: the implementation of the directive
        :rtype: Any
        """
        if isclass(implementation):
            self._implementation = implementation()
        else:
            self._implementation = implementation
        SchemaRegistry.register_directive(self._schema_name, self)
        return implementation
