import logging

from functools import lru_cache, partial
from importlib import import_module, invalidate_caches
from inspect import isawaitable
from typing import (
    Any,
    AsyncIterable,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.execution.collect import parse_and_validate_query
from tartiflette.execution.execute import create_source_event_stream, execute
from tartiflette.execution.response import build_response
from tartiflette.schema.bakery import SchemaBakery
from tartiflette.schema.registry import SchemaRegistry
from tartiflette.types.exceptions.tartiflette import (
    ImproperlyConfigured,
    NonCallable,
    NonCoroutine,
)
from tartiflette.utils.callables import is_valid_coroutine
from tartiflette.utils.errors import (
    default_error_coercer,
    error_coercer_factory,
)

logger = logging.getLogger(__name__)

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
    Imports and bakes the list of modules filled at engine initialisation
    before importing & baking built-ins modules.
    :param module_definitions: list of modules filled at engine initialisation
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


class Engine:
    """
    Tartiflette GraphQL engine.
    """

    def __init__(
        self,
        sdl=None,
        schema_name=None,
        error_coercer=None,
        custom_default_resolver=None,
        custom_default_type_resolver=None,
        modules=None,
        query_cache_decorator=UNDEFINED_VALUE,
    ) -> None:
        """
        Creates an uncooked Engine instance.
        """
        self._schema = None
        self._schema_name = schema_name
        self._error_coercer = error_coercer
        self._custom_default_resolver = custom_default_resolver
        self._custom_default_type_resolver = custom_default_type_resolver
        self._modules = modules
        self._query_cache_decorator = (
            query_cache_decorator
            if query_cache_decorator is not UNDEFINED_VALUE
            else lru_cache(maxsize=512)
        )
        self._sdl = sdl
        self._cooked = False
        self._build_response = None
        self._query_executor = None
        self._subscription_executor = None
        self._cached_parse_and_validate_query = None

    async def cook(
        self,
        sdl: Union[str, List[str]] = None,
        error_coercer: Callable[
            [Exception, Dict[str, Any]], Dict[str, Any]
        ] = None,
        custom_default_resolver: Optional[Callable] = None,
        custom_default_type_resolver: Optional[Callable] = None,
        modules: Optional[Union[str, List[str], List[Dict[str, Any]]]] = None,
        query_cache_decorator: Optional[Callable] = UNDEFINED_VALUE,
        schema_name: str = None,
    ) -> None:
        """
        Cook the tartiflette, basically prepare the engine by binding it to
        given modules using the schema_name as a key. You wont be able to
        execute a request if the engine wasn't cooked.
        :param sdl: path or list of path to the files / directories containing
        the SDL
        :param error_coercer: callable in charge of transforming a couple
        Exception/error into an error dictionary
        :param custom_default_resolver: callable that will replace the builtin
        default_resolver (called as resolver for each UNDECORATED field)
        :param custom_default_type_resolver: callable that will replace the
        tartiflette `default_type_resolver` (will be called on abstract types
        to deduct the type of a result)
        :param modules: list of string containing the name of the modules you
        want the engine to import, usually this modules contains your
        Resolvers, Directives, Scalar or Subscription code
        :param query_cache_decorator: callable that will replace the
        tartiflette default lru_cache decorator to cache query parsing
        :param schema_name: name of the SDL
        :type sdl: Union[str, List[str]]
        :type error_coercer: Callable[[Exception, Dict[str, Any]], Dict[str, Any]]
        :type custom_default_resolver: Optional[Callable]
        :type custom_default_type_resolver: Optional[Callable]
        :type modules: Optional[Union[str, List[str], List[Dict[str, Any]]]]
        :type query_cache_decorator: Optional[Callable]
        :type schema_name: str
        """
        if self._cooked:
            return

        if modules is None:
            modules = self._modules or []

        if isinstance(modules, str):
            modules = [modules]

        sdl = sdl or self._sdl
        if not sdl:
            raise Exception("Please provide a SDL")

        schema_name = schema_name or self._schema_name or "default"

        custom_error_coercer = error_coercer or self._error_coercer
        if custom_error_coercer and not is_valid_coroutine(
            custom_error_coercer
        ):
            raise NonCoroutine(
                "Given < error_coercer > is not a coroutine callable."
            )

        custom_default_resolver = (
            custom_default_resolver or self._custom_default_resolver
        )
        if custom_default_resolver and not is_valid_coroutine(
            custom_default_resolver
        ):
            raise NonCoroutine(
                "Given < custom_default_resolver > is not a coroutine callable."
            )

        custom_default_type_resolver = (
            custom_default_type_resolver or self._custom_default_type_resolver
        )
        if custom_default_type_resolver and not callable(
            custom_default_type_resolver
        ):
            raise NonCallable(
                "Given < custom_default_type_resolver > is not a coroutine callable."
            )

        self._error_coercer = error_coercer_factory(
            custom_error_coercer or default_error_coercer
        )

        self._modules, modules_sdl = await _import_modules(
            modules, schema_name
        )

        SchemaRegistry.register_sdl(schema_name, sdl, modules_sdl)
        self._schema = await SchemaBakery.bake(
            schema_name, custom_default_resolver, custom_default_type_resolver
        )
        self._build_response = partial(
            build_response, error_coercer=self._error_coercer
        )

        (
            self._query_executor,
            self._subscription_executor,
        ) = self._schema.bake_execute(
            self._perform_query, self._perform_subscription
        )

        if query_cache_decorator is UNDEFINED_VALUE:
            query_cache_decorator = self._query_cache_decorator

        self._cached_parse_and_validate_query = (
            query_cache_decorator(parse_and_validate_query)
            if callable(query_cache_decorator)
            else parse_and_validate_query
        )

        self._cooked = True

    async def _perform_subscription(
        self,
        schema: "GraphQLSchema",
        document: "DocumentNode",
        request_parsing_errors: Optional[List["TartifletteError"]] = None,
        operation_name: Optional[str] = None,
        context: Optional[Any] = None,
        variables: Optional[Dict[str, Any]] = None,
        initial_value: Optional[Any] = None,
    ):
        # pylint: disable=too-many-locals
        if request_parsing_errors:
            yield await self._build_response(errors=request_parsing_errors)
            return

        source_event_stream = await create_source_event_stream(
            schema,
            document,
            self._build_response,
            initial_value,
            context,
            variables,
            operation_name,
        )

        if isinstance(source_event_stream, dict):
            yield source_event_stream
            return

        async for payload in source_event_stream:
            yield await execute(
                self._schema,
                document,
                self._build_response,
                payload,
                context,
                variables,
                operation_name,
            )

    async def _perform_query(
        self,
        schema: "GraphQLSchema",
        document: "DocumentNode",
        request_parsing_errors: Optional[List["TartifletteError"]] = None,
        operation_name: Optional[str] = None,
        context: Optional[Any] = None,
        variables: Optional[Dict[str, Any]] = None,
        initial_value: Optional[Any] = None,
    ):
        if request_parsing_errors:
            return await self._build_response(errors=request_parsing_errors)

        return await execute(
            schema,
            document,
            self._build_response,
            initial_value,
            context,
            variables,
            operation_name,
        )

    async def execute(
        self,
        query: Union[str, bytes],
        operation_name: Optional[str] = None,
        context: Optional[Any] = None,
        variables: Optional[Dict[str, Any]] = None,
        initial_value: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """
        Parses and executes a GraphQL query/mutation request.
        :param query: the GraphQL request / query as UTF8-encoded string
        :param operation_name: the operation name to execute
        :param context: value that can contain everything you need and that
        will be accessible from the resolvers
        :param variables: the variables provided in the GraphQL request
        :param initial_value: an initial value corresponding to the root type
        being executed
        :type query: Union[str, bytes]
        :type operation_name: Optional[str]
        :type context: Optional[Any]
        :type variables: Optional[Dict[str, Any]]
        :type initial_value: Optional[Any]
        :return: computed response corresponding to the request
        :rtype: Dict[str, Any]
        """
        document, errors = self._cached_parse_and_validate_query(
            query, self._schema
        )

        # Goes through potential schema directives and finish in self._perform_query
        return await self._query_executor(
            self._schema,
            document,
            errors,
            operation_name,
            context,
            variables,
            initial_value,
            context_coercer=context,
        )

    async def subscribe(
        self,
        query: Union[str, bytes],
        operation_name: Optional[str] = None,
        context: Optional[Any] = None,
        variables: Optional[Dict[str, Any]] = None,
        initial_value: Optional[Any] = None,
    ) -> AsyncIterable[Dict[str, Any]]:
        """
        Parses and executes a GraphQL subscription request.
        :param query: the GraphQL request / query as UTF8-encoded string
        :param operation_name: the operation name to execute
        :param context: value that can contain everything you need and that
        will be accessible from the resolvers
        :param variables: the variables provided in the GraphQL request
        :param initial_value: an initial value corresponding to the root type
        being executed
        :type query: Union[str, bytes]
        :type operation_name: Optional[str]
        :type context: Optional[Any]
        :type variables: Optional[Dict[str, Any]]
        :type initial_value: Optional[Any]
        :return: computed response corresponding to the request
        :rtype: AsyncIterable[Dict[str, Any]]
        """
        document, errors = self._cached_parse_and_validate_query(
            query, self._schema
        )

        # Goes through potential schema directives and finish in self._perform_subscription
        async for payload in self._subscription_executor(
            self._schema,
            document,
            errors,
            operation_name,
            context,
            variables,
            initial_value,
            context_coercer=context,
        ):
            yield payload
