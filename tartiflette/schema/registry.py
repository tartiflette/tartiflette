import os

from glob import glob
from typing import List, Optional, Union

from tartiflette.schema import GraphQLSchema
from tartiflette.types.exceptions.tartiflette import ImproperlyConfigured

_DIR_PATH = os.path.dirname(__file__)

# TODO: re-use "CUSTOM_SCALARS" from tartiflette.scalar (impossible for now  due to cyclic import)
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


def _get_builtins_sdl_files(
    exclude_builtins_scalars: Optional[List[str]]
) -> List[str]:
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
    def _register(
        schema_name: str,
        where: str,
        obj: Optional[
            Union["Directive", "Resolver", "Scalar", "Subscription"]
        ],
    ) -> None:
        if not obj:
            return

        SchemaRegistry._schemas.setdefault(schema_name, {}).setdefault(
            where, {}
        )

        if obj.name in SchemaRegistry._schemas[schema_name][where]:
            raise ImproperlyConfigured(
                "Can't register < %s > to < %s > %s because it's already "
                "registered" % (obj.name, schema_name, where)
            )

        SchemaRegistry._schemas[schema_name][where][obj.name] = obj

    @staticmethod
    def register_directive(
        schema_name: str = "default", directive: Optional["Directive"] = None
    ) -> None:
        SchemaRegistry._register(schema_name, "directives", directive)

    @staticmethod
    def register_resolver(
        schema_name: str = "default", resolver: Optional["Resolver"] = None
    ) -> None:
        SchemaRegistry._register(schema_name, "resolvers", resolver)

    @staticmethod
    def register_scalar(
        schema_name: str = "default", scalar: Optional["Scalar"] = None
    ) -> None:
        SchemaRegistry._register(schema_name, "scalars", scalar)

    @staticmethod
    def register_subscription(
        schema_name: str = "default",
        subscription: Optional["Subscription"] = None,
    ) -> None:
        SchemaRegistry._register(schema_name, "subscriptions", subscription)

    @staticmethod
    def register_sdl(
        schema_name: str,
        sdl: Union[str, List[str], GraphQLSchema],
        exclude_builtins_scalars: Optional[List[str]] = None,
    ) -> None:
        SchemaRegistry._schemas.setdefault(schema_name, {})

        # Maybe read them one and use them a lot :p
        sdl_files_list = _get_builtins_sdl_files(exclude_builtins_scalars)

        full_sdl = ""

        if isinstance(sdl, list):
            sdl_files_list += sdl
        elif os.path.isfile(sdl):
            sdl_files_list.append(sdl)
        elif os.path.isdir(sdl):
            sdl_files_list += glob(
                os.path.join(sdl, "**/*.sdl"), recursive=True
            ) + glob(os.path.join(sdl, "**/*.graphql"), recursive=True)
        else:
            full_sdl = sdl

        # Convert SDL files into big schema and parse it
        for filepath in sdl_files_list:
            with open(filepath, "r") as sdl_file:
                full_sdl += "\n" + sdl_file.read()

        SchemaRegistry._schemas[schema_name]["sdl"] = full_sdl

    @staticmethod
    def find_schema_info(schema_name: str = "default") -> dict:
        return SchemaRegistry._schemas[schema_name]

    @staticmethod
    def find_schema(schema_name: str = "default") -> GraphQLSchema:
        return SchemaRegistry.find_schema_info(schema_name)["inst"]
