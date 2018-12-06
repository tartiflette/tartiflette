import os
from tartiflette.schema import GraphQLSchema


class SchemaRegistry:
    _schemas = {}

    @staticmethod
    def _register(schema_name, where, obj):
        if not obj:
            return

        if not SchemaRegistry._schemas.get(schema_name):
            SchemaRegistry._schemas[schema_name] = {}

        if not SchemaRegistry._schemas[schema_name].get(where):
            SchemaRegistry._schemas[schema_name][where] = []

        SchemaRegistry._schemas[schema_name][where].append(obj)

    @staticmethod
    def register_directive(schema_name="default", directive=None):
        SchemaRegistry._register(schema_name, "directives", directive)

    @staticmethod
    def register_resolver(schema_name="default", resolver=None):
        SchemaRegistry._register(schema_name, "resolvers", resolver)

    @staticmethod
    def register_scalar(schema_name="default", scalar=None):
        SchemaRegistry._register(schema_name, "scalars", scalar)

    @staticmethod
    def register_sdl(schema_name, sdl):
        if not SchemaRegistry._schemas.get(schema_name):
            SchemaRegistry._schemas[schema_name] = {}

        # Maybe read them one and use them a lot :p
        sdl_files_list = [
            "%s/builtins/scalar.sdl" % os.path.dirname(__file__),
            "%s/builtins/directives.sdl" % os.path.dirname(__file__),
            "%s/builtins/introspection.sdl" % os.path.dirname(__file__),
        ]
        full_sdl = ""
        if not isinstance(sdl, GraphQLSchema):
            if isinstance(sdl, list):
                sdl_files_list = sdl_files_list + sdl
            elif os.path.isfile(sdl):
                sdl_files_list = sdl_files_list + [sdl]
            elif os.path.isdir(sdl):
                sdl_files_list = sdl_files_list + [
                    os.path.join(sdl, f)
                    for f in os.listdir(sdl)
                    if os.path.isfile(os.path.join(sdl, f))
                    and f.endswith(".sdl")
                ]
            else:
                full_sdl = sdl
        else:
            SchemaRegistry._schemas[schema_name]["inst"] = sdl

        # Convert SDL files into big schema and parse it
        for filepath in sdl_files_list:
            with open(filepath, "r") as sdl_file:
                data = sdl_file.read().replace("\n", " ")
                full_sdl += " " + data

        SchemaRegistry._schemas[schema_name]["sdl"] = full_sdl

    @staticmethod
    def find_schema_info(schema_name="default"):
        return SchemaRegistry._schemas[schema_name]

    @staticmethod
    def find_schema(schema_name="default"):
        return SchemaRegistry.find_schema_info(schema_name)["inst"]
