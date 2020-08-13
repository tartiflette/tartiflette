import os

from glob import glob
from typing import Any, Dict, List, Optional, Union

from tartiflette.types.exceptions.tartiflette import ImproperlyConfigured

__all__ = ("SchemaRegistry",)


_SCHEMA_OBJECT_IDS = [
    "directives",
    "resolvers",
    "type_resolvers",
    "scalars",
    "subscriptions",
]


class SchemaRegistry:
    """
    Utility singleton class which stores data about each registered schema.
    """

    _schemas: Dict[
        str,
        Dict[
            str,
            Union[
                "Directive",
                "Resolver",
                "TypeResolver",
                "Scalar",
                "Subscription",
            ],
        ],
    ] = {}

    @staticmethod
    def _register(
        schema_name: str,
        where: str,
        obj: Optional[
            Union[
                "Directive",
                "Resolver",
                "TypeResolver",
                "Scalar",
                "Subscription",
            ]
        ],
    ) -> None:
        """
        Registers an object to the appropriate key of the store linked to the
        schema name filled in.
        :param schema_name: name of the schema to which link the object
        :param where: type of the object which determines the key where to
        register it
        :param obj: object to register
        :type schema_name: str
        :type where: str
        :type obj: Optional[
            Union[
                Directive,
                Resolver,
                TypeResolver,
                Scalar,
                Subscription,
            ]
        ]
        """
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
        """
        Registers a directive implementation to the store of the schema name
        filled in.
        :param schema_name: name of the schema to which register the directive
        :param directive: implementation of the directive to register
        :type schema_name: str
        :type directive: Optional[Directive]
        """
        SchemaRegistry._register(schema_name, "directives", directive)

    @staticmethod
    def register_resolver(
        schema_name: str = "default", resolver: Optional["Resolver"] = None
    ) -> None:
        """
        Registers a resolver implementation to the store of the schema name
        filled in.
        :param schema_name: name of the schema to which register the resolver
        :param resolver: implementation of the resolver to register
        :type schema_name: str
        :type resolver: Optional[Resolver]
        """
        SchemaRegistry._register(schema_name, "resolvers", resolver)

    @staticmethod
    def register_type_resolver(
        schema_name: str = "default",
        type_resolver: Optional["TypeResolver"] = None,
    ) -> None:
        """
        Registers a type resolver implementation to the store of the schema
        name filled in.
        :param schema_name: name of the schema to which register the type
        resolver
        :param type_resolver: implementation of the type resolver to register
        :type schema_name: str
        :type type_resolver: Optional[TypeResolver]
        """
        SchemaRegistry._register(schema_name, "type_resolvers", type_resolver)

    @staticmethod
    def register_scalar(
        schema_name: str = "default", scalar: Optional["Scalar"] = None
    ) -> None:
        """
        Registers a scalar implementation to the store of the schema name
        filled in.
        :param schema_name: name of the schema to which register the scalar
        :param scalar: implementation of the scalar to register
        :type schema_name: str
        :type scalar: Optional[Scalar]
        """
        SchemaRegistry._register(schema_name, "scalars", scalar)

    @staticmethod
    def register_subscription(
        schema_name: str = "default",
        subscription: Optional["Subscription"] = None,
    ) -> None:
        """
        Registers a subscription implementation to the store of the schema name
        filled in.
        :param schema_name: name of the schema to which register the
        subscription
        :param subscription: implementation of the subscription to register
        :type schema_name: str
        :type subscription: Optional[Subscription]
        """
        SchemaRegistry._register(schema_name, "subscriptions", subscription)

    @staticmethod
    def register_sdl(
        schema_name: str,
        sdl: Union[str, List[str], "GraphQLSchema"],
        modules_sdl: Optional[str] = None,
    ) -> None:
        """
        Computes and registers the final SDL of a schema.
        :param schema_name: name of the schema
        :param sdl: path(s) to the SDL or raw string representing the SDL
        :param modules_sdl: extra SDL from the imported modules
        :type schema_name: str
        :type sdl: Union[str, List[str], GraphQLSchema]
        :type modules_sdl: Optional[str]
        """
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
            with open(filepath, mode="r") as sdl_file:
                full_sdl += "\n" + sdl_file.read()

        if modules_sdl:
            full_sdl = f"{full_sdl} {modules_sdl}"

        SchemaRegistry._schemas[schema_name]["sdl"] = full_sdl

    @staticmethod
    def find_schema_info(schema_name: str = "default") -> Dict[str, Any]:
        """
        Returns the information which has been registered for a schema.
        :param schema_name: name of the schema to find
        :type schema_name: str
        :return: the information about the schema
        :rtype: Dict[str, Any]
        """
        return SchemaRegistry._schemas[schema_name]

    @staticmethod
    def is_schema_registered(schema_name: str) -> bool:
        """
        Determine whether or not the schema is registered.
        :param schema_name: name of the schema to check
        :type schema_name: str
        :return: whether or not the schema is registered
        :rtype: bool
        """
        return schema_name in SchemaRegistry._schemas

    @staticmethod
    def find_schema(schema_name: str = "default") -> "GraphQLSchema":
        """
        Returns the GraphQLSchema instance of a registered schema.
        :param schema_name: name of the schema to return
        :type schema_name: str
        :return: the GraphQLSchema instance of a registered schema
        :rtype: GraphQLSchema
        """
        return SchemaRegistry.find_schema_info(schema_name)["inst"]

    @staticmethod
    def bake_registered_objects(schema: "GraphQLSchema"):
        schema_info = SchemaRegistry._schemas[schema.name]
        for object_id in _SCHEMA_OBJECT_IDS:
            for obj in schema_info.get(object_id, {}).values():
                obj.bake(schema)

    @classmethod
    def clean(cls) -> None:
        """
        Erases all information related to the previous registered schemas.
        """
        cls._schemas = {}
