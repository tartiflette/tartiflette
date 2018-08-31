from typing import List


class ExecutionContext:
    # See if we should keep it here or move it to the visitor ?
    def __init__(self):
        self._errors: List[Exception] = []

    @property
    def errors(self):
        return self._errors

    def add_error_and_raise(self, error: Exception):
        self.add_error(error)
        raise error

    def add_error(self, error: Exception):
        self._errors.append(error)


class Info:

    __SAMEVALUE__ = "__SAMEVALUE__"

    def __init__(
        self,
        query_field,
        schema_field,
        schema,
        path,
        location,
        execution_ctx: ExecutionContext,
    ):
        self.query_field: "NodeField" = query_field
        self.schema_field: "GraphQLField" = schema_field
        self.schema: "GraphQLSchema" = schema
        self.path: List[str] = path
        self.location: "Location" = location
        self.execution_ctx: ExecutionContext = execution_ctx

    def __repr__(self):
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

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
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

    def clone(
        self,
        query_field=__SAMEVALUE__,
        schema_field=__SAMEVALUE__,
        schema=__SAMEVALUE__,
        path=__SAMEVALUE__,
        location=__SAMEVALUE__,
        execution_ctx=__SAMEVALUE__,
    ):
        return Info(
            query_field=self.query_field
            if query_field == self.__SAMEVALUE__
            else query_field,
            schema_field=self.schema_field
            if schema_field == self.__SAMEVALUE__
            else schema_field,
            schema=self.schema if schema == self.__SAMEVALUE__ else schema,
            path=self.path[:] if path == self.__SAMEVALUE__ else path,
            location=self.location
            if location == self.__SAMEVALUE__
            else location,
            execution_ctx=self.execution_ctx
            if execution_ctx == self.__SAMEVALUE__
            else execution_ctx,
        )

    def clone_with_path(self, new_path_part):
        new_path = self.path[:]
        new_path.append(new_path_part)
        return self.clone(path=new_path)
