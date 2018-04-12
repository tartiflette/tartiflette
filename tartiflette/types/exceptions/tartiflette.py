
class TartifletteException(Exception):
    pass


class TartifletteSchemaValidationError(Exception):
    pass


class TartifletteNonAwaitableResolver(Exception):
    pass


class TartifletteUnexpectedASTNode(Exception):
    pass


class TartifletteSDLUnexpectedToken(Exception):
    # TODO: Wrap lark exceptions (UnexpectedToken, UnexpectedInput
    pass


class TartifletteUnexpectedNullValue(Exception):
    pass


class TartifletteNonListValue(Exception):
    pass


class UnknownVariableException(Exception):
    def __init__(self, varname):
        # TODO: Unify error messages format
        super().__init__(message="< %s > is not known" % varname)


class TartifletteGraphQLTypeException(Exception):
    def __init__(self, message, gql_type=None):
        super().__init__(message)
        self.gql_type = gql_type


class TartifletteSchemaException(Exception):
    def __init__(self, message, gql_type=None):
        super().__init__(message)
        self.gql_type = gql_type
