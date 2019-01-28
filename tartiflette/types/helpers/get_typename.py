from typing import Any


def get_typename(raw: Any) -> str:
    try:
        return raw["_typename"]
    except (KeyError, TypeError):
        pass

    try:
        return raw._typename  # pylint: disable=protected-access
    except AttributeError:
        pass

    return raw.__class__.__name__
