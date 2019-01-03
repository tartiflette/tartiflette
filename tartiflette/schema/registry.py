import os
from tartiflette.schema import GraphQLSchema

_DIR_PATH = os.path.dirname(__file__)

_BUILTINS_SCALARS = [
    "Boolean",
    "Date",
    "DateTime",
    "Float",
    "ID",
    "Int",
    "String",
    "Time",
]


def _get_builtins_sdl_files(exclude_builtins_scalars):
    return [
        *[
            "%s/builtins/scalars/%s.sdl" % (_DIR_PATH, builtin_scalar.lower())
            for builtin_scalar in _BUILTINS_SCALARS
            if (
                exclude_builtins_scalars is None
                or builtin_scalar not in exclude_builtins_scalars
            )
        ],
        "%s/builtins/directives.sdl" % _DIR_PATH,
        "%s/builtins/introspection.sdl" % _DIR_PATH,
    ]


class SchemaRegistry:
    _schemas = {}

    @staticmethod
    def _register(schema_name, where, obj):
        if not obj:
            return
        SchemaRegistry._schemas.setdefault(schema_name, {}).setdefault(
            where, []
        ).append(obj)

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
    def register_sdl(schema_name, sdl, exclude_builtins_scalars=None):
        SchemaRegistry._schemas.setdefault(schema_name, {})

        # Maybe read them one and use them a lot :p
        sdl_files_list = _get_builtins_sdl_files(exclude_builtins_scalars)

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
