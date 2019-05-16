from typing import Callable

from tartiflette.schema.registry import SchemaRegistry
from tartiflette.types.exceptions.tartiflette import (
    InvalidType,
    MissingImplementation,
    UnknownTypeDefinition,
)

__all__ = ("TypeResolver",)


class TypeResolver:
    """
    This decorator allows you to link a GraphQL Schema abstract type to a type
    resolver.

    For example, for the following SDL:
        type Cat {
          name: String
        }

        type Dog {
          name: String
        }

        union Pet = Cat | Dog

    Use the TypeResolver decorator the following way:

        @TypeResolver("Pet")
        async def resolve_pet_type(result, context, info, abstract_type):
            return "Cat" if "meowVolume" in result else "Dog"
    """

    def __init__(self, name: str, schema_name: str = "default") -> None:
        """
        :param name: name of the abstract type to wrap
        :param schema_name: name of the schema to which link the type resolver
        :type name: str
        :type schema_name: str
        """
        self.name = name
        self._implementation = None
        self._schema_name = schema_name

    def bake(self, schema: "GraphQLSchema") -> None:
        """
        Sets the type resolver into the schema abstract type definition.
        :param schema: the GraphQLSchema instance linked to the type resolver
        :type schema: GraphQLSchema
        """
        if not self._implementation:
            raise MissingImplementation(
                f"No implementation given for type resolver < {self.name} >"
            )

        try:
            graphql_type = schema.find_type(self.name)
            if not graphql_type.is_abstract_type:
                raise InvalidType(
                    f"Type < {self.name} > is not an abstract type."
                )

            graphql_type.type_resolver = self._implementation
        except KeyError:
            raise UnknownTypeDefinition(
                f"Unknown Type Definition < {self.name} >."
            )

    def __call__(self, resolver: Callable) -> Callable:
        """
        Registers the type resolver into the schema.
        :param implementation: implementation of the type resolver
        :type implementation: Callable
        :return: the implementation of the type resolver
        :rtype: Callable
        """
        SchemaRegistry.register_type_resolver(self._schema_name, self)
        self._implementation = resolver
        return resolver
