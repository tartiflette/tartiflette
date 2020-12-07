from typing import Callable, Optional

from tartiflette.schema.registry import SchemaRegistry
from tartiflette.schema.transformer import schema_from_sdl

__all__ = ("SchemaBakery",)


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
        schema_info["inst"] = schema
        return schema

    @staticmethod
    async def bake(
        schema_name: str,
        custom_default_resolver: Optional[Callable] = None,
        custom_default_type_resolver: Optional[Callable] = None,
        custom_default_arguments_coercer: Optional[Callable] = None,
        coerce_list_concurrently: Optional[bool] = None,
    ) -> "GraphQLSchema":
        """
        Bakes and returns a GraphQLSchema instance.
        :param schema_name: name of the schema to bake
        :param custom_default_resolver: callable that will replace the builtin
        default_resolver (called as resolver for each UNDECORATED field)
        :param custom_default_type_resolver: callable that will replace the
        tartiflette `default_type_resolver` (will be called on abstract types
        to deduct the type of a result)
        :param custom_default_arguments_coercer: callable that will replace the
        tartiflette `default_arguments_coercer`
        :param coerce_list_concurrently: whether or not list will be coerced
        concurrently
        :type schema_name: str
        :type custom_default_resolver: Optional[Callable]
        :type custom_default_type_resolver: Optional[Callable]
        :type custom_default_arguments_coercer: Optional[Callable]
        :type coerce_list_concurrently: Optional[bool]
        :return: a baked GraphQLSchema instance
        :rtype: GraphQLSchema
        """
        schema = SchemaBakery._preheat(schema_name)
        await schema.bake(
            custom_default_resolver,
            custom_default_type_resolver,
            custom_default_arguments_coercer,
            coerce_list_concurrently,
        )
        return schema
