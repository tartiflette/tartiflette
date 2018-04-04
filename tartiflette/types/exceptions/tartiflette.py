
class TartifletteException(Exception):
    pass


class TartifletteSchemaValidationError(Exception):
    pass


class TartifletteUnexpectedASTNode(Exception):
    pass


class TartifletteSDLUnexpectedToken(Exception):
    # TODO: Wrap lark exceptions (UnexpectedToken, UnexpectedInput
    pass


class TartifletteGraphQLTypeException(Exception):
    def __init__(self, message, gql_type=None):
        super().__init__(message)
        self.gql_type = gql_type


class TartifletteSchemaException(Exception):
    def __init__(self, message, gql_type=None):
        super().__init__(message)
        self.gql_type = gql_type
