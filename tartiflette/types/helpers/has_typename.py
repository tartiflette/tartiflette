def has_typename(raw):
    try:
        return bool(raw["_typename"] and True)
    except (KeyError, TypeError):
        pass

    try:
        return bool(raw._typename and True)  # pylint: disable=protected-access
    except AttributeError:
        pass

    return False
