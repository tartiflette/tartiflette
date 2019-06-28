import logging

from importlib import import_module, invalidate_caches
from inspect import isawaitable
from typing import Any, AsyncIterable, Callable, Dict, List, Optional, Union

from tartiflette.executors.basic import (
    execute as basic_execute,
    subscribe as basic_subscribe,
)
from tartiflette.parser import TartifletteRequestParser
from tartiflette.resolver.factory import (
    default_error_coercer,
    error_coercer_factory,
)
from tartiflette.schema.bakery import SchemaBakery
from tartiflette.schema.registry import SchemaRegistry
from tartiflette.types.exceptions.tartiflette import (
    GraphQLError,
    ImproperlyConfigured,
)
from tartiflette.utils.errors import to_graphql_error

logger = logging.getLogger(__name__)

_BUILTINS_MODULES = [
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
]


async def _bake_module(module, schema_name, config=None):
    msdl = module.bake(schema_name, config)
    if isawaitable(msdl):
        msdl = await msdl

    return msdl


async def _import_builtins(imported_modules, sdl, schema_name):
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


async def _import_modules(modules, schema_name):
    imported_modules = []
    sdl = ""

    invalidate_caches()

    for module in modules:
        if not isinstance(module, dict):
            module = {"name": module, "config": {}}

        config = module["config"]
        module = import_module(module["name"])

        if callable(getattr(module, "bake", None)):
            sdl = "{sdl}\n{msdl}".format(
                sdl=sdl,
                msdl=await _bake_module(module, schema_name, config) or "",
            )

        imported_modules.append(module)

    return await _import_builtins(imported_modules, sdl, schema_name)


class Engine:
    def __init__(
        self,
        sdl=None,
        schema_name=None,
        error_coercer=None,
        custom_default_resolver=None,
        modules=None,
    ) -> None:
        """
        Create an uncooked Engine instance
        """
        self._parser = TartifletteRequestParser()
        self._schema = None
        self._schema_name = schema_name
        self._error_coercer = error_coercer
        self._custome_default_resolver = custom_default_resolver
        self._modules = modules
        self._sdl = sdl

    async def cook(
        self,
        sdl: Union[str, List[str]] = None,
        error_coercer: Callable[[Exception], dict] = None,
        custom_default_resolver: Optional[Callable] = None,
        modules: Optional[Union[str, List[str]]] = None,
        schema_name: str = None,
    ):
        """
        Cook the tartiflette, basicly prepare the engine by binding it to given modules using the schema_name as a key.
        You wont be able to execute a request if the engine wasn't cooked.

        Keyword Arguments:
            sdl {Union[str, List[str]]} -- The SDL to work with.
            schema_name {str} -- The name of the SDL (default: {"default"})
            error_coercer {Callable[[Exception, dict], dict]} -- An optional callable in charge of transforming a couple Exception/error into an error dict (default: {default_error_coercer})
            custom_default_resolver {Optional[Callable]} -- An optional callable that will replace the tartiflette default_resolver (Will be called like a resolver for each UNDECORATED field) (default: {None})
            modules {Optional[Union[str, List[str]]]} -- An optional list of string containing the name of the modules you want the engine to import, usually this modules contains your Resolvers, Directives, Scalar or Subscription code (default: {None})
        """

        if not modules:
            modules = self._modules or []

        if isinstance(modules, str):
            modules = [modules]

        schema_name = schema_name or self._schema_name or "default"

        self._error_coercer = error_coercer_factory(
            error_coercer or self._error_coercer or default_error_coercer
        )

        self._modules, modules_sdl = await _import_modules(
            modules, schema_name
        )

        SchemaRegistry.register_sdl(schema_name, sdl or self._sdl, modules_sdl)
        self._schema = SchemaBakery.bake(schema_name, custom_default_resolver)

    async def execute(
        self,
        query: str,
        operation_name: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        variables: Optional[Dict[str, Any]] = None,
        initial_value: Optional[Any] = None,
    ) -> dict:
        """
        Parse and execute a GraphQL request (as string).
        :param query: the GraphQL request / query as UTF8-encoded string
        :param operation_name: the operation name to execute
        :param context: a dict containing anything you need
        :param variables: the variables used in the GraphQL request
        :param initial_value: an initial value corresponding to the root type being executed
        :return: a GraphQL response (as dict)
        """
        operations, errors = self._parse_query_to_operations(query, variables)

        if errors:
            return errors

        return await basic_execute(
            operations,
            operation_name,
            request_ctx=context,
            initial_value=initial_value,
            error_coercer=self._error_coercer,
        )

    async def subscribe(
        self,
        query: str,
        operation_name: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        variables: Optional[Dict[str, Any]] = None,
        initial_value: Optional[Any] = None,
    ) -> AsyncIterable[Dict[str, Any]]:
        """
        Parse and execute a GraphQL request (as string).
        :param query: the GraphQL request / query as UTF8-encoded string
        :param operation_name: the operation name to execute
        :param context: a dict containing anything you need
        :param variables: the variables used in the GraphQL request
        :param initial_value: an initial value corresponding to the root type being executed
        :return: a GraphQL response (as dict)
        """
        operations, errors = self._parse_query_to_operations(query, variables)

        if errors:
            yield errors
        else:
            async for result in basic_subscribe(  # pylint: disable=not-an-iterable
                operations,
                operation_name,
                request_ctx=context,
                initial_value=initial_value,
                error_coercer=self._error_coercer,
            ):
                yield result

    def _parse_query_to_operations(self, query, variables):
        try:
            operations, errors = self._parser.parse_and_tartify(
                self._schema,
                query,
                variables=dict(variables) if variables else variables,
            )
        except GraphQLError as e:
            errors = [e]
        except Exception as e:  # pylint: disable=broad-except
            errors = [
                to_graphql_error(e, message="Server encountered an error.")
            ]

        if errors:
            return (
                None,
                {
                    "data": None,
                    "errors": [self._error_coercer(err) for err in errors],
                },
            )
        return operations, None
