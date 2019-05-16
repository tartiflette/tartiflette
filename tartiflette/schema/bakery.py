from typing import Callable, Optional

from tartiflette.schema.registry import SchemaRegistry
from tartiflette.schema.transformer import schema_from_sdl

__all__ = ("SchemaBakery",)

_SCHEMA_OBJECT_IDS = [
    "directives",
    "resolvers",
    "type_resolvers",
    "scalars",
    "subscriptions",
]


class SchemaBakery:
    """
    Utility class in charge of baking schemas.
    """

    @staticmethod
    def _preheat(schema_name: str) -> "GraphQLSchema":
        """
        Loads the SDL and converts it to a GraphQLSchema instance before baking
        each registered objects of this schema.
        :param schema_name: name of the schema to treat
        :type schema_name: str
        :return: a pre-baked GraphQLSchema instance
        :rtype: GraphQLSchema
        """
        schema_info = SchemaRegistry.find_schema_info(schema_name)
        sdl = schema_info["sdl"]

        schema = schema_from_sdl(sdl, schema_name=schema_name)

        for object_ids in _SCHEMA_OBJECT_IDS:
            for obj in schema_info.get(object_ids, {}).values():
                obj.bake(schema)

        schema_info["inst"] = schema

        return schema

    @staticmethod
    async def bake(
        schema_name: str, custom_default_resolver: Optional[Callable] = None
    ) -> "GraphQLSchema":
        """
        Bakes and returns a GraphQLSchema instance.
        :param schema_name: name of the schema to bake
        :param custom_default_resolver: callable that will replace the builtin
        default_resolver (called as resolver for each UNDECORATED field)
        :type schema_name: str
        :type custom_default_resolver: Optional[Callable]
        :return: a baked GraphQLSchema instance
        :rtype: GraphQLSchema
        """
        schema = SchemaBakery._preheat(schema_name)
        await schema.bake(custom_default_resolver)
        return schema
