from inspect import isclass
from typing import Any

from tartiflette.schema.registry import SchemaRegistry
from tartiflette.types.exceptions.tartiflette import (
    MissingImplementation,
    UnknownScalarDefinition,
)

__all__ = ("Scalar",)


class Scalar:
    """
    This decorator allows you to link a GraphQL Scalar to a Scalar class.

    For example, for the following SDL:

        scalar DateTime

    Use the Scalar decorator the following way:

        @Scalar("DateTime")
        class ScalarDateTime:
            def coerce_output(self, value):
                return value.isoformat()

            def coerce_input(self, value):
                return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")

            def parse_literal(self, ast):
                if not isinstance(ast, StringValueNode):
                    return UNDEFINED_VALUE
                try:
                    return datetime.strptime(ast.value, "%Y-%m-%dT%H:%M:%S")
                except Exception:
                    pass
                return UNDEFINED_VALUE
    """

    def __init__(self, name: str, schema_name: str = "default") -> None:
        """
        :param name: name of the scalar
        :param schema_name: name of the schema to which link the scalar
        :type name: str
        :type schema_name: str
        """
        self.name = name
        self._implementation = None
        self._schema_name = schema_name

    def bake(self, schema: "GraphQLSchema") -> None:
        """
        Sets the scalar coercers into the schema scalar definition.
        :param schema: the GraphQLSchema instance linked to the scalar
        :type schema: GraphQLSchema
        """
        if not self._implementation:
            raise MissingImplementation(
                f"No implementation given for scalar < {self.name} >"
            )

        scalar = schema.find_scalar(self.name)
        if not scalar:
            raise UnknownScalarDefinition(
                f"Unknown Scalar Definition {self.name}"
            )

        scalar.coerce_output = self._implementation.coerce_output
        scalar.coerce_input = self._implementation.coerce_input
        scalar.parse_literal = self._implementation.parse_literal

    def __call__(self, implementation: Any) -> Any:
        """
        Registers the scalar into the schema.
        :param implementation: implementation of the scalar
        :type implementation: Any
        :return: the implementation of the scalar
        :rtype: Any
        """
        if isclass(implementation):
            self._implementation = implementation()
        else:
            self._implementation = implementation
        SchemaRegistry.register_scalar(self._schema_name, self)
        return implementation
