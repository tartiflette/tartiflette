from typing import Any, List


class ExecutionContext:
    # See if we should keep it here or move it to the visitor ?
    def __init__(self) -> None:
        self._errors: List[Exception] = []
        self.is_introspection: bool = False

    @property
    def errors(self) -> List[Exception]:
        return self._errors

    def add_error(self, error: Exception) -> None:
        self._errors.append(error)


class Info:
    def __init__(
        self,
        query_field: "NodeField",
        schema_field: "GraphQLField",
        schema: "GraphQLSchema",
        path: List[str],
        location: "Location",
        execution_ctx: ExecutionContext,
    ) -> None:
        self.query_field = query_field
        self.schema_field = schema_field
        self.schema = schema
        self.path = path
        self.location = location
        self.execution_ctx = execution_ctx

    def __repr__(self) -> str:
        return (
            "{}(query_field={!r}, schema_field={!r}, schema={!r}, "
            "path={!r}, location={!r}, execution_ctx={!r})".format(
                self.__class__.__name__,
                self.query_field,
                self.schema_field,
                self.schema,
                self.path,
                self.location,
                self.execution_ctx,
            )
        )

    def __str__(self) -> str:
        return repr(self)

    def __eq__(self, other: Any) -> bool:
        return self is other or (
            type(self) is type(other)
            and (
                self.query_field == other.query_field
                and self.schema_field == other.schema_field
                and self.schema == other.schema
                and self.path == other.path
                and self.location == other.location
                and self.execution_ctx == other.execution_ctx
            )
        )
