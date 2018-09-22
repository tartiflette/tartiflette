from typing import Dict, Optional
from tartiflette.resolver import ResolverExecutorFactory
from tartiflette.types.type import GraphQLType


class GraphQLField:
    """
    Field Definition

    A field is used in Object, Interfaces as its constituents.
    """

    def __init__(
        self,
        name: str,
        gql_type: str,
        arguments: Optional[Dict] = None,
        resolver: Optional[callable] = None,
        description: Optional[str] = None,
        directives: Optional[Dict] = None,
    ):
        self.name = name
        self.gql_type = gql_type
        self.arguments = arguments if arguments else {}

        self._directives = directives
        self.resolver = ResolverExecutorFactory.get_resolver_executor(
            resolver, self, directives
        )
        self.description = description if description else ""

    def __repr__(self):
        return (
            "{}(name={!r}, gql_type={!r}, arguments={!r}, "
            "resolver={!r}, description={!r}, directives={!r})".format(
                self.__class__.__name__,
                self.name,
                self.gql_type,
                self.arguments,
                self.resolver,
                self.description,
                self.directives,
            )
        )

    @property
    def directives(self):
        try:
            return [x for _, x in self._directives.items()]
        except AttributeError:
            return []

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self is other or (
            type(self) is type(other)
            and self.name == other.name
            and self.gql_type == other.gql_type
            and self.arguments == other.arguments
            and self.resolver == other.resolver
            and self.directives == other.directives
        )

    @property
    def kind(self):
        try:
            return self.gql_type.kind
        except AttributeError:
            return "FIELD"

    @property
    def ofType(self):
        return self.type

    @property
    def type(self):
        if isinstance(self.gql_type, GraphQLType):
            return self.gql_type

        return {
            "name": self.gql_type,
            "kind": "SCALAR",
            "description": self.description,
        }

    @property
    def args(self):
        return [x for _, x in self.arguments.items()]
