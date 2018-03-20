class UnknownVariableException(Exception):
    def __init__(self, varname):
        super(UnknownVariableException,
              self).__init__(message="< %s > is not known" % varname)


class TatifletteException(Exception):
    pass
