import os

from glob import glob
from typing import List, Optional, Union

from tartiflette.schema import GraphQLSchema
from tartiflette.types.exceptions.tartiflette import ImproperlyConfigured


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
        modules_sdl: str = None,
    ) -> None:
        SchemaRegistry._schemas.setdefault(schema_name, {})

        sdl_files_list = []
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

        if modules_sdl:
            full_sdl = f"{full_sdl} {modules_sdl}"

        SchemaRegistry._schemas[schema_name]["sdl"] = full_sdl

    @staticmethod
    def find_schema_info(schema_name: str = "default") -> dict:
        return SchemaRegistry._schemas[schema_name]

    @staticmethod
    def find_schema(schema_name: str = "default") -> GraphQLSchema:
        return SchemaRegistry.find_schema_info(schema_name)["inst"]
