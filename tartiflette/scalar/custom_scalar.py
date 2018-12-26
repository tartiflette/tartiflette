from tartiflette.schema.registry import SchemaRegistry
from tartiflette.types.exceptions.tartiflette import UnknownScalarDefinition


class Scalar:
    def __init__(self, name: str, schema_name: str = "default"):
        self._name = name
        self._implementation = None
        self._schema_name = schema_name

    def bake(self, schema):
        if not self._implementation:
            raise Exception("No implementation given")

        scalar = schema.find_scalar(self._name)
        if scalar:
            scalar.coerce_output = self._implementation.coerce_output
            scalar.coerce_input = self._implementation.coerce_input
        else:
            raise UnknownScalarDefinition(
                "Unknow Scalar Definition %s" % self._name
            )

    def __call__(self, implementation):
        SchemaRegistry.register_scalar(self._schema_name, self)
        self._implementation = implementation
        return implementation
