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
        schema: Optional = None,
    ):
        self.name = name
        self.gql_type = gql_type
        self.arguments = arguments if arguments else {}

        self._directives = directives
        self._schema = schema
        self.description = description if description else ""
        self._is_deprecated = False

        self.resolver = ResolverExecutorFactory.get_resolver_executor(
            resolver, self, directives
        )
        self.parent_type = None

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
        # TODO to simplify this we need to rework the
        # GraphQLField->Directive->ArgumentsDef->ArgumentInstance interface
        # Can be do "once" at schema bake time
        try:
            directives = {
                name: {
                    "callables": self._schema.find_directive(
                        name
                    ).implementation,
                    "args": {
                        arg_name: self._schema.find_directive(name)
                        .arguments[arg_name]
                        .default_value
                        for arg_name in self._schema.find_directive(
                            name
                        ).arguments
                    },
                }
                for name in self._directives
            }

            for name, directive in directives.items():
                if self._directives[name] is not None:
                    directive["args"].update(self._directives[name])

            return [v for _, v in directives.items()]

        except (AttributeError, KeyError, TypeError):
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

    # Introspection Attribute
    @property
    def kind(self):
        try:
            return self.gql_type.kind
        except AttributeError:
            return "FIELD"

    # Introspection Attribute
    @property
    def type(self):
        if isinstance(self.gql_type, GraphQLType):
            return self.gql_type

        return self.schema.find_type(self.gql_type)

    # Introspection Attribute
    @property
    def isDeprecated(self):  # pylint: disable=invalid-name
        return self._is_deprecated

    @isDeprecated.setter
    def isDeprecated(self, value):  # pylint: disable=invalid-name
        self._is_deprecated = value

    # Introspection Attribute
    @property
    def args(self):
        return [x for _, x in self.arguments.items()]

    @property
    def schema(self):
        return self._schema

    def bake(self, schema, parent_type):
        self._schema = schema

        self.resolver.update_coercer()
        self.resolver.apply_directives()
        self.parent_type = parent_type
