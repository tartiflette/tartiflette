from typing import Any, Dict, List, Optional


class SkipCollection(Exception):
    pass


class TartifletteError(Exception):
    """
    Base exceptions of all internal errors raised by the Tartiflette engine.
    """

    def __init__(
        self,
        message: str,
        path: Optional[List[str]] = None,
        locations: Optional[List["Location"]] = None,
        user_message: Optional[str] = None,
        more_info: Optional[str] = None,
        extensions: Optional[Dict[str, Any]] = None,
        original_error: Optional[Exception] = None,
    ) -> None:
        """
        :param message: message explaining the error which occurred
        :param path: path on the query where the error occurred
        :param locations: locations on the document where the error occurred
        :param user_message: more detailed human message explaining the error
        :param more_info: extra information for the error
        :param extensions: extra information for the error which will be added
        to the `extensions` key once coerced
        :param original_error: instance of the original exception which lead to
        the error
        :type message: str
        :type path: Optional[List[str]]
        :type locations: Optional[List[Location]]
        :type user_message: Optional[str]
        :type more_info: Optional[str]
        :type extensions: Optional[Dict[str, Any]]
        :type original_error: Optional[Exception]
        """
        super().__init__(message)
        self.message = message  # Developer message by default
        self.user_message = user_message
        self.more_info = more_info or ""
        self.path = path or None
        self.locations = locations or []
        self.extensions = extensions or {}
        self.original_error = original_error

    def __repr__(self) -> str:
        """
        Returns the representation of a TartifletteError instance.
        :return: the representation of a TartifletteError instance
        :rtype: str
        """
        return f"{self.__class__.__name__}(message=%r, locations=%r)" % (
            self.user_message or self.message,
            self.locations,
        )

    def coerce_value(
        self,
        *_args,
        path: Optional[List[str]] = None,
        locations: Optional[List["Location"]] = None,
        **_kwargs,
    ) -> Dict[str, Any]:
        """
        Converts the TartifletteError instance into a valid GraphQL error
        output.
        :param path: path on the query where the error occurred
        :param locations: locations on the document where the error occurred
        :type path: Optional[List[str]]
        :type locations: Optional[List[Location]]
        :return: a valid GraphQL error output
        :rtype: Dict[str, Any]
        """
        computed_locations = []

        try:
            for location in locations or self.locations:
                computed_locations.append(location.collect_value())
        except (AttributeError, TypeError):
            pass

        errors = {
            "message": self.user_message or self.message,
            "path": path or self.path,
            "locations": computed_locations,
        }

        if self.extensions:
            errors["extensions"] = dict(self.extensions)
        return errors


class MultipleException(Exception):
    """
    Utility exception which allows to handle multiple errors at once.
    """

    def __init__(self, exceptions: Optional[List[Exception]] = None) -> None:
        """
        :param exceptions: list of exceptions to handle
        :type exceptions: Optional[List[Exception]]
        """
        super().__init__()
        self.exceptions = exceptions or []

    def __bool__(self) -> bool:
        """
        Determines whether or not there is exceptions.
        :return: whether or not there is exceptions
        :rtype: bool
        """
        return bool(self.exceptions)

    def __add__(self, other: "MultipleException") -> "MultipleException":
        """
        Concatenates the exception list of both MultipleException to return a
        new MultipleException instance containing both exception list.
        :param other: an MultipleException instance
        :type other: MultipleException
        :return: a new MultipleException containing both exception list
        :rtype: MultipleException
        """
        return MultipleException(self.exceptions + other.exceptions)


class ImproperlyConfigured(TartifletteError):
    pass


class InvalidType(TartifletteError):
    pass


class GraphQLSchemaError(TartifletteError):
    pass


class GraphQLSyntaxError(TartifletteError):
    pass


class NonAwaitableResolver(ImproperlyConfigured):
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


class MissingImplementation(ImproperlyConfigured):
    pass


class RedefinedImplementation(TartifletteError):
    pass
