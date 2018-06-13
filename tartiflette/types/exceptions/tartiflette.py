from typing import List, Any, Optional

from tartiflette.executors.types import ExecutionData
from tartiflette.types.field import GraphQLField
from tartiflette.types.location import Location


class TartifletteException(Exception):
    pass


class GraphQLError(Exception):

    def __init__(self, message: str, path: Optional[List[Any]] = None,
                 locations: Optional[List[Location]] = None,
                 user_message: str=None, more_info: str=""):
        super().__init__(message)
        self.message = message  # Developer message by default
        self.user_message = user_message if user_message else message
        self.more_info = more_info
        self.path = path if path else None
        self.locations = locations if locations else []

    def to_jsonable(self):
        return self.collect_value()

    def collect_value(self):
        locations = []
        try:
            for loc in self.locations:
                locations.append(loc.collect_value())
        except AttributeError:
            pass
        except TypeError:
            pass
        return {
            "message": self.user_message if self.user_message else self.message,
            "path": self.path,
            "locations": locations,
        }


class InvalidValue(GraphQLError):

    def __init__(self, value: Any, gql_type=None,
                 field: Optional[GraphQLField]=None,
                 path: Optional[List[Any]] = None,
                 locations: Optional[List[Location]]=None):
        self.value = value
        self.field = field
        self.gql_type = gql_type
        message = "Invalid value (value: {!r})".format(
            value
        )
        if self.field:
            message += " for field `{}`".format(self.field.name)
        if self.gql_type:
            message += " of type `{}`".format(str(self.gql_type))
        super().__init__(message=message, path=path,
                         locations=locations)


class GraphQLSchemaError(GraphQLError):

    def __init__(self, message):
        super().__init__(message=message)


class NonAwaitableResolver(GraphQLError):

    def __init__(self, message):
        super().__init__(message=message)


class UnexpectedASTNode(GraphQLError):
    def __init__(self, message):
        super().__init__(message=message)


class InvalidSDL(GraphQLError):
    def __init__(self, message):
        super().__init__(message=message)


class UnknownVariableException(GraphQLError):
    def __init__(self, varname):
        # TODO: Unify error messages format
        super().__init__(message="< %s > is not known" % varname)

class UnknownGraphQLType(GraphQLError):
    def __init__(self, message):
        super().__init__(message=message)
