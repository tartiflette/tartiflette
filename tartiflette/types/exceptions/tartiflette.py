from typing import Any, List, Optional

from tartiflette.executors.types import Info
from tartiflette.types.location import Location


class TartifletteError(Exception):
    def __init__(
        self,
        message: str,
        path: Optional[list] = None,
        locations: Optional[List[Location]] = None,
        user_message: str = None,
        more_info: str = "",
        extensions: Optional[dict] = None,
        original_error: Optional[Exception] = None,
    ) -> None:
        super().__init__(message)
        self.message = message  # Developer message by default
        self.user_message = user_message or message
        self.more_info = more_info
        self.path = path or None
        self.locations = locations or []
        self.extensions = extensions or {}
        self.original_error = original_error

    def coerce_value(
        self,
        *_args,
        path: Optional[list] = None,
        locations: Optional[List[Location]] = None,
        **_kwargs,
    ):
        computed_locations = []

        try:
            for location in locations or self.locations:
                computed_locations.append(location.collect_value())
        except (AttributeError, TypeError):
            pass

        errors = {
            "message": self.user_message
            if self.user_message
            else self.message,
            "path": path or self.path,
            "locations": computed_locations,
        }

        if self.extensions:
            errors["extensions"] = dict(self.extensions)
        return errors


class GraphQLError(TartifletteError):
    pass


class MultipleException(Exception):
    exceptions = None

    def __init__(self, exceptions=None):
        super().__init__()
        self.exceptions = exceptions


class ImproperlyConfigured(GraphQLError):
    pass


class InvalidValue(GraphQLError):
    def __init__(self, value: Any, info: Info) -> None:
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


class InvalidType(GraphQLError):
    pass


class NullError(InvalidValue):
    pass


class GraphQLSchemaError(GraphQLError):
    pass


class GraphQLSyntaxError(GraphQLError):
    pass


class NonAwaitableResolver(ImproperlyConfigured):
    pass


class NonAwaitableDirective(ImproperlyConfigured):
    pass


class NonAsyncGeneratorSubscription(ImproperlyConfigured):
    pass


class NotSubscriptionField(ImproperlyConfigured):
    pass


class UnknownSchemaFieldResolver(GraphQLError):
    pass


class UnknownDirectiveDefinition(GraphQLError):
    pass


class UnknownScalarDefinition(GraphQLError):
    pass


class UnknownFieldDefinition(GraphQLError):
    pass


class UnknownTypeDefinition(GraphQLError):
    pass


class UnusedFragment(GraphQLError):
    pass


class MissingImplementation(ImproperlyConfigured):
    pass


class UnexpectedASTNode(GraphQLError):
    pass


class InvalidSDL(GraphQLError):
    pass


class RedefinedImplementation(InvalidSDL):
    pass


class AlreadyDefined(GraphQLError):
    pass


class UndefinedFragment(GraphQLError):
    pass


class NotALeafType(GraphQLError):
    pass


class NotAnObjectType(GraphQLError):
    pass


class NotUniqueOperationName(GraphQLError):
    pass


class NotLoneAnonymousOperation(GraphQLError):
    pass


class MultipleRootNodeOnSubscriptionOperation(GraphQLError):
    pass


class UndefinedFieldArgument(GraphQLError):
    pass


class UndefinedDirectiveArgument(GraphQLError):
    pass


class MissingRequiredArgument(GraphQLError):
    pass


class UniqueArgumentNames(GraphQLError):
    pass


class UnknownNamedOperation(GraphQLError):
    pass


class UnknownAnonymousdOperation(GraphQLError):
    pass


class UnknownVariableException(GraphQLError):
    def __init__(self, varname: str) -> None:
        # TODO: Unify error messages format
        super().__init__(message="< %s > is not known" % varname)


class UnknownGraphQLType(GraphQLError):
    pass


class SkipExecution(Exception):
    pass
