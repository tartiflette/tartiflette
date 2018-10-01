from tartiflette.sdl.builder import build_graphql_schema_from_sdl

from tartiflette.directive import BUILT_IN_DIRECTIVES, Directive
from tartiflette.scalar import CUSTOM_SCALARS, Scalar

from .registry import SchemaRegistry
from .schema import GraphQLSchema


class SchemaBakery:
    @staticmethod
    def _preheat(schema_name):
        schema_info = SchemaRegistry.find_schema_info(schema_name)
        schema = schema_info.get("inst", GraphQLSchema())

        sdl = schema_info["sdl"]
        build_graphql_schema_from_sdl(sdl, schema=schema)

        SchemaBakery._inject_default_object(schema_name)

        for object_ids in ["directives", "resolvers", "scalars"]:
            for obj in schema_info.get(object_ids, []):
                obj.bake(schema)

        schema_info["inst"] = schema

        return schema

    @staticmethod
    def bake(schema_name):
        schema = SchemaBakery._preheat(schema_name)
        schema.bake()

        return schema

    @staticmethod
    def _inject_default_object(schema_name):
        for name, scalar_implem in CUSTOM_SCALARS.items():
            deco = Scalar(name, schema_name)
            deco(scalar_implem)

        for name, directive_implem in BUILT_IN_DIRECTIVES.items():
            deco = Directive(name, schema_name)
            deco(directive_implem)
