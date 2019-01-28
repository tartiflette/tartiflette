from typing import Any


def has_typename(raw: Any) -> bool:
    try:
        return bool(raw["_typename"])
    except (KeyError, TypeError):
        pass

    try:
        return bool(raw._typename)  # pylint: disable=protected-access
    except AttributeError:
        pass

    return False
