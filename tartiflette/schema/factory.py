from importlib import import_module, invalidate_caches
from inspect import isawaitable
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from tartiflette.schema.bakery import SchemaBakery
from tartiflette.schema.registry import SchemaRegistry
from tartiflette.types.exceptions.tartiflette import (
    ImproperlyConfigured,
    NonCallable,
    NonCoroutine,
)
from tartiflette.utils.callables import is_valid_coroutine

__all__ = ("create_schema",)

_BUILTINS_MODULES = (
    "tartiflette.directive.builtins.deprecated",
    "tartiflette.directive.builtins.non_introspectable",
    "tartiflette.directive.builtins.skip",
    "tartiflette.directive.builtins.include",
    "tartiflette.scalar.builtins.boolean",
    "tartiflette.scalar.builtins.date",
    "tartiflette.scalar.builtins.datetime",
    "tartiflette.scalar.builtins.float",
    "tartiflette.scalar.builtins.id",
    "tartiflette.scalar.builtins.int",
    "tartiflette.scalar.builtins.string",
    "tartiflette.scalar.builtins.time",
    "tartiflette.schema.builtins.introspection",
)


async def _bake_module(
    module: object, schema_name: str, config: Optional[Dict[str, Any]] = None
) -> str:
    """
    Bakes a module and retrieves its extra SDL content.
    :param module: module instance to bake
    :param schema_name: schema name to link with
    :param config: configuration of the module
    :type module: object
    :type schema_name: str
    :type config: Optional[Dict[str, Any]]
    :return: the extra SDL provided by the module
    :rtype: str
    """
    msdl = module.bake(schema_name, config)
    if isawaitable(msdl):
        msdl = await msdl
    return msdl or ""


async def _import_builtins(
    imported_modules: List[object], sdl: str, schema_name: str
) -> Tuple[List[object], str]:
    """
    Imports and bakes built-ins directives and scalars if not already
    implemented.
    :param imported_modules: list of already imported modules
    :param sdl: SDL with complementary content from already baked modules
    :param schema_name: schema name to link with
    :type imported_modules: List[object]
    :type sdl: str
    :type schema_name: str
    :return: couple list of imported modules instance/final SDL
    :rtype: Tuple[List[object], str]
    """
    for module in _BUILTINS_MODULES:
        try:
            module = import_module(module)
            sdl = "{sdl}\n{msdl}".format(
                sdl=sdl, msdl=await _bake_module(module, schema_name)
            )
            imported_modules.append(module)
        except ImproperlyConfigured:
            pass

    return imported_modules, sdl


async def _import_modules(
    module_definitions: List[Union[str, Dict[str, Any]]], schema_name: str
) -> Tuple[List[object], str]:
    """
    Imports and bakes the list of modules filled at SDL initialisation
    before importing & baking built-ins modules.
    :param module_definitions: list of modules filled at schema initialisation
    :param schema_name: schema name to link with
    :type module_definitions: List[Union[str, Dict[str, Any]]]
    :type schema_name: str
    :return: couple list of imported modules instance/final SDL
    :rtype: Tuple[List[object], str]
    """
    sdl = ""
    imported_modules = []

    invalidate_caches()

    for module_definition in module_definitions:
        if not isinstance(module_definition, dict):
            module_definition = {"name": module_definition, "config": None}

        module = import_module(module_definition["name"])
        if callable(getattr(module, "bake", None)):
            sdl = "{sdl}\n{msdl}".format(
                sdl=sdl,
                msdl=await _bake_module(
                    module, schema_name, module_definition["config"]
                ),
            )
        imported_modules.append(module)

    return await _import_builtins(imported_modules, sdl, schema_name)


async def create_schema(
    sdl: Union[str, List[str]],
    name: str = "default",
    modules: Optional[Union[str, List[str], List[Dict[str, Any]]]] = None,
    default_resolver: Optional[Callable] = None,
    default_type_resolver: Optional[Callable] = None,
    default_arguments_coercer: Optional[Callable] = None,
    parser: Optional[Callable] = None,
) -> "GraphQLSchema":
    """
    Create a GraphQLSchema instance.
    :param sdl: the SDL to related to the schema
    :param name: name of the schema
    :param modules: list Python modules to load
    :param default_resolver: the default resolver to use
    :param default_type_resolver: the default type resolver to use
    :param default_arguments_coercer: callable to use to coerce arguments
    :param parser: parser to use to parse the SDL into a document
    :type sdl: Union[str, List[str]]
    :type name: str
    :type modules: Optional[Union[str, List[str], List[Dict[str, Any]]]]
    :type default_resolver: Optional[Callable]
    :type default_type_resolver: Optional[Callable]
    :type default_arguments_coercer: Optional[Callable]
    :type parser: Optional[Callable]
    :return: a GraphQLSchema instance
    :rtype: GraphQLSchema
    """
    if modules is None:
        modules = []
    elif isinstance(modules, str):
        modules = [modules]

    if not sdl:
        raise ImproperlyConfigured("Please provide a SDL.")

    if default_resolver and not is_valid_coroutine(default_resolver):
        raise NonCoroutine(
            "Given < default_resolver > is not a coroutine callable."
        )

    if default_type_resolver and not callable(default_type_resolver):
        raise NonCallable(
            "Given < default_type_resolver > is not a coroutine callable."
        )

    if default_arguments_coercer and not is_valid_coroutine(
        default_arguments_coercer
    ):
        raise NonCoroutine(
            "Given < default_arguments_coercer > is not a coroutine callable."
        )

    modules, modules_sdl = await _import_modules(modules, name)

    SchemaRegistry.register_sdl(name, sdl, modules_sdl)
    return await SchemaBakery.bake(
        name,
        default_resolver,
        default_type_resolver,
        default_arguments_coercer,
        parser,
    )
