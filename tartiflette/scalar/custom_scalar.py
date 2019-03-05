from tartiflette.schema.registry import SchemaRegistry
from tartiflette.types.exceptions.tartiflette import (
    MissingImplementation,
    UnknownScalarDefinition,
)


class Scalar:
    """
    This decorator allows you to link a GraphQL Scalar to a Scalar class.

    For example, for the following SDL:

        scalar DateTime

    Use the Directive decorator the following way:

        @Scalar("DateTime")
        class ScalarDateTime:
            @staticmethod
            def coerce_output(value):
                return value.isoformat()

            @staticmethod
            def coerce_input(value):
                return iso8601.parse_date(value)
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
                "No implementation given for scalar < %s >" % self._name
            )

        scalar = schema.find_scalar(self._name)
        if not scalar:
            raise UnknownScalarDefinition(
                "Unknow Scalar Definition %s" % self._name
            )

        scalar.coerce_output = self._implementation.coerce_output
        scalar.coerce_input = self._implementation.coerce_input

    def __call__(self, implementation):
        SchemaRegistry.register_scalar(self._schema_name, self)
        self._implementation = implementation
        return implementation
