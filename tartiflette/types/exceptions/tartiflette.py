from typing import Any, List, Optional

from tartiflette.executors.types import Info
from tartiflette.types.location import Location


class TartifletteException(Exception):
    pass


class GraphQLError(Exception):
    def __init__(
        self,
        message: str,
        path: Optional[List[Any]] = None,
        locations: Optional[List[Location]] = None,
        user_message: str = None,
        more_info: str = "",
    ):
        super().__init__(message)
        self.message = message  # Developer message by default
        self.user_message = user_message if user_message else message
        self.more_info = more_info
        self.path = path if path else None
        self.locations = locations if locations else []

    def coerce_value(self, *_args, **_kwargs):
        locations = []
        try:
            for loc in self.locations:
                locations.append(loc.collect_value())
        except AttributeError:
            pass
        except TypeError:
            pass
        return {
            "message": self.user_message
            if self.user_message
            else self.message,
            "path": self.path,
            "locations": locations,
        }


class InvalidValue(GraphQLError):
    def __init__(self, value: Any, info: Info):
        self.value = value
        self.info = info
        message = "Invalid value (value: {!r})".format(value)
        try:
            if self.info.schema_field:
                message += " for field `{}`".format(
                    self.info.schema_field.name
                )
            if self.info.schema_field.gql_type:
                message += " of type `{}`".format(
                    str(self.info.schema_field.gql_type)
                )
        except (AttributeError, TypeError, ValueError):
            pass
        super().__init__(
            message=message,
            path=self.info.path,
            locations=[self.info.location],
        )


class NullError(InvalidValue):
    pass


class GraphQLSchemaError(GraphQLError):
    pass


class NonAwaitableResolver(GraphQLError):
    pass


class NonAwaitableDirective(GraphQLError):
    pass


class UnknownSchemaFieldResolver(GraphQLError):
    pass


class UnknownDirectiveDefinition(GraphQLError):
    pass


class MissingImplementation(GraphQLError):
    pass


class UnexpectedASTNode(GraphQLError):
    pass


class InvalidSDL(GraphQLError):
    pass


class UnknownVariableException(GraphQLError):
    def __init__(self, varname):
        # TODO: Unify error messages format
        super().__init__(message="< %s > is not known" % varname)


class UnknownGraphQLType(GraphQLError):
    pass
