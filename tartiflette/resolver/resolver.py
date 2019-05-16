from inspect import iscoroutinefunction
from typing import Callable, Optional

from tartiflette.schema.registry import SchemaRegistry
from tartiflette.types.exceptions.tartiflette import (
    MissingImplementation,
    NonAwaitableResolver,
    UnknownFieldDefinition,
)
from tartiflette.types.helpers.definition import get_wrapped_type
from tartiflette.types.helpers.type import get_graphql_type

__all__ = ("Resolver",)


class Resolver:
    """
    This decorator allows you to link a GraphQL Schema field to a resolver.

    For example, for the following SDL:

        type SomeObject {
            field: Int
        }

    Use the Resolver decorator the following way:

        @Resolver("SomeObject.field")
        async def field_resolver(parent, args, ctx, info):
            # do your stuff
            return 42
    """

    def __init__(
        self,
        name: str,
        schema_name: str = "default",
        type_resolver: Optional[Callable] = None,
    ) -> None:
        """
        :param name: name of the field to wrap
        :param schema_name: name of the schema to which link the resolver
        :param type_resolver: the callable to use to resolve the type of an
        abstract type
        :type name: str
        :type schema_name: str
        :type type_resolver: Optional[Callable]
        """
        self.name = name
        self._type_resolver = type_resolver
        self._implementation = None
        self._schema_name = schema_name

    def bake(self, schema: "GraphQLSchema") -> None:
        """
        Sets the resolver coercers into the schema field definition.
        :param schema: the GraphQLSchema instance linked to the resolver
        :type schema: GraphQLSchema
        """
        if not self._implementation:
            raise MissingImplementation(
                f"No implementation given for resolver < {self.name} >"
            )

        try:
            field = schema.get_field_by_name(self.name)
            field.raw_resolver = self._implementation

            field_wrapped_type = get_wrapped_type(
                get_graphql_type(schema, field.gql_type)
            )
            if self._type_resolver and field_wrapped_type.is_abstract_type:
                field_wrapped_type.add_field_type_resolver(
                    self.name, self._type_resolver
                )
        except KeyError:
            raise UnknownFieldDefinition(
                f"Unknown Field Definition {self.name}"
            )

    def __call__(self, resolver: Callable) -> Callable:
        """
        Registers the resolver into the schema.
        :param implementation: implementation of the resolver
        :type implementation: Callable
        :return: the implementation of the resolver
        :rtype: Callable
        """
        if not iscoroutinefunction(resolver):
            raise NonAwaitableResolver(
                f"The resolver `{repr(resolver)}` given is not awaitable."
            )

        SchemaRegistry.register_resolver(self._schema_name, self)
        self._implementation = resolver
        return resolver
