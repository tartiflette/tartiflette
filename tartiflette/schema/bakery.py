from tartiflette.sdl.builder import build_graphql_schema_from_sdl

from tartiflette.directive import BUILT_IN_DIRECTIVES, Directive
from tartiflette.scalar import CUSTOM_SCALARS, Scalar

from tartiflette.schema.registry import SchemaRegistry
from tartiflette.schema import GraphQLSchema


class SchemaBakery:
    @staticmethod
    def _preheat(schema_name, exclude_builtins_scalars):
        schema_info = SchemaRegistry.find_schema_info(schema_name)
        schema = schema_info.get("inst", GraphQLSchema(name=schema_name))

        sdl = schema_info["sdl"]
        build_graphql_schema_from_sdl(sdl, schema=schema)

        SchemaBakery._inject_default_object(
            schema_name, exclude_builtins_scalars
        )

        for object_ids in ["directives", "resolvers", "scalars"]:
            for obj in schema_info.get(object_ids, []):
                obj.bake(schema)

        schema_info["inst"] = schema

        return schema

    @staticmethod
    def bake(
        schema_name,
        custom_default_resolver=None,
        exclude_builtins_scalars=None,
    ):
        schema = SchemaBakery._preheat(schema_name, exclude_builtins_scalars)
        schema.bake(custom_default_resolver)
        return schema

    @staticmethod
    def _inject_default_object(schema_name, exclude_builtins_scalars):
        for name, scalar_implem in CUSTOM_SCALARS.items():
            if (
                exclude_builtins_scalars is None
                or name not in exclude_builtins_scalars
            ):
                deco = Scalar(name, schema_name)
                deco(scalar_implem)

        for name, directive_implem in BUILT_IN_DIRECTIVES.items():
            deco = Directive(name, schema_name)
            deco(directive_implem)
