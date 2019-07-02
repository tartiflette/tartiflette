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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(
            "GraphQLError is deprecated, please use TartifletteError instead"
        )


class MultipleException(Exception):
    exceptions = None

    def __init__(self, exceptions=None):
        super().__init__()
        self.exceptions = exceptions


class ImproperlyConfigured(TartifletteError):
    pass


class InvalidValue(TartifletteError):
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


class InvalidType(TartifletteError):
    pass


class NullError(InvalidValue):
    pass


class GraphQLSchemaError(TartifletteError):
    pass


class GraphQLSyntaxError(TartifletteError):
    pass


class NonAwaitableResolver(ImproperlyConfigured):
    pass


class NonAwaitableDirective(ImproperlyConfigured):
    pass


class NonAsyncGeneratorSubscription(ImproperlyConfigured):
    pass


class NotSubscriptionField(ImproperlyConfigured):
    pass


class UnknownSchemaFieldResolver(TartifletteError):
    pass


class UnknownDirectiveDefinition(TartifletteError):
    pass


class UnknownScalarDefinition(TartifletteError):
    pass


class UnknownFieldDefinition(TartifletteError):
    pass


class UnknownTypeDefinition(TartifletteError):
    pass


class UnusedFragment(TartifletteError):
    pass


class MissingImplementation(ImproperlyConfigured):
    pass


class UnexpectedASTNode(TartifletteError):
    pass


class InvalidSDL(TartifletteError):
    pass


class RedefinedImplementation(InvalidSDL):
    pass


class AlreadyDefined(TartifletteError):
    pass


class UndefinedFragment(TartifletteError):
    pass


class NotALeafType(TartifletteError):
    pass


class NotAnObjectType(TartifletteError):
    pass


class NotUniqueOperationName(TartifletteError):
    pass


class NotLoneAnonymousOperation(TartifletteError):
    pass


class MultipleRootNodeOnSubscriptionOperation(TartifletteError):
    pass


class UndefinedFieldArgument(TartifletteError):
    pass


class UndefinedDirectiveArgument(TartifletteError):
    pass


class MissingRequiredArgument(TartifletteError):
    pass


class UniqueArgumentNames(TartifletteError):
    pass


class UnknownNamedOperation(TartifletteError):
    pass


class UnknownAnonymousdOperation(TartifletteError):
    pass


class UnknownVariableException(TartifletteError):
    def __init__(self, varname: str) -> None:
        # TODO: Unify error messages format
        super().__init__(message="< %s > is not known" % varname)


class UnknownGraphQLType(TartifletteError):
    pass


class SkipExecution(Exception):
    pass
