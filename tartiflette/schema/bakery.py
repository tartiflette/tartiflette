from typing import Callable, Optional

from tartiflette.schema.registry import SchemaRegistry
from tartiflette.schema.schema import GraphQLSchema
from tartiflette.sdl.builder import build_graphql_schema_from_sdl

_SCHEMA_OBJECT_IDS = ["directives", "resolvers", "scalars", "subscriptions"]


class SchemaBakery:
    @staticmethod
    def _preheat(schema_name: str) -> GraphQLSchema:
        schema_info = SchemaRegistry.find_schema_info(schema_name)
        schema = schema_info.get("inst", GraphQLSchema(name=schema_name))

        sdl = schema_info["sdl"]
        build_graphql_schema_from_sdl(sdl, schema=schema)

        for object_ids in _SCHEMA_OBJECT_IDS:
            for obj in schema_info.get(object_ids, {}).values():
                obj.bake(schema)

        schema_info["inst"] = schema

        return schema

    @staticmethod
    def bake(
        schema_name: str, custom_default_resolver: Optional[Callable] = None
    ) -> GraphQLSchema:
        schema = SchemaBakery._preheat(schema_name)
        schema.bake(custom_default_resolver)
        return schema
