class UnknownVariableException(Exception):
    def __init__(self, varname):
        # TODO: Unify error messages format
        super().__init__(message="< %s > is not known" % varname)


class TatifletteException(Exception):
    # TODO: Rename (there is a typo here)
    # TODO: Move all custom exceptions into a common namespace
    pass
