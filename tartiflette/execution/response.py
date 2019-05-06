from collections import Callable


def build_response(error_coercer: Callable, data=None, errors=None):
    """
    TODO:
    :param error_coercer: TODO:
    :param data: TODO:
    :param errors: TODO:
    :type error_coercer: TODO:
    :type data: TODO:
    :type errors: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    coerced_errors = (
        [error_coercer(error) for error in errors] if errors else None
    )
    if coerced_errors:
        return {"data": data, "errors": coerced_errors}
    return {"data": data}
