from tartiflette.types.exceptions.tartiflette import TartifletteError


def is_coercible_exception(exception):
    return hasattr(exception, "coerce_value") and callable(
        exception.coerce_value
    )


def to_graphql_error(exception, message=None):
    if is_coercible_exception(exception):
        return exception
    return TartifletteError(
        message or str(exception), original_error=exception
    )
