__all__ = ("SchemaStack",)


class SchemaStack:
    __slots__ = ("hash", "schema", "execute", "subscribe")

    def __init__(self, hash, schema, executor, subscriptor):
        self.hash = hash
        self.schema = schema
        self.execute = executor
        self.subscribe = subscriptor
