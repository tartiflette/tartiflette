class Scalar:
    def __init__(self, name: str, schema):
        self.schema = schema
        self.name = name
        self.scalar = self.schema.find_scalar(self.name)

    def __call__(self, implementation):
        self.scalar.coerce_output = implementation.coerce_output
        self.scalar.coerce_input = implementation.coerce_input
        self.schema.prepare_custom_scalars()
        return implementation
