from collections import OrderedDict
from typing import Optional, Dict, Any

from tartiflette.executors.types import ExecutionData


class GraphQLField:
    """
    Field Definition

    A field is used in Object, Interfaces as its constituents.
    """

    def __init__(self, name: str,
                 gql_type: str,
                 arguments: Optional[Dict] = None,
                 resolver: Optional[callable] = None,
                 description: Optional[str] = None,
                 ):
        self.name = name
        self.gql_type = gql_type
        self.arguments = arguments if arguments else OrderedDict()
        self.resolver = resolver
        self.description = description

    def __repr__(self):
        return "{}(name={!r}, gql_type={!r}, arguments={!r}, " \
               "resolver={!r}, description={!r})".format(
                self.__class__.__name__, self.name, self.gql_type,
            self.arguments, self.resolver, self.description)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self is other or (
                type(self) is type(other) and
                self.name == other.name and
                self.gql_type == other.gql_type and
                self.arguments == other.arguments and
                self.resolver == other.resolver
        )

    def type_check(self, value: Any, execution_data: ExecutionData) -> Any:
        # TODO: IMPORTANT Implement this !!
        return value

    def coerce_value(self, value: Any):
        if value is None:
            return None
        return {self.name: value}

