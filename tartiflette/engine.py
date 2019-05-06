from importlib import import_module, invalidate_caches
from typing import Any, AsyncIterable, Callable, Dict, List, Optional, Union

from tartiflette.execution import (
    build_execution_context,
    build_response,
    parse_and_validate_query,
)
from tartiflette.execution.execute import execute_operation, run_subscription
from tartiflette.parser import TartifletteRequestParser
from tartiflette.resolver.factory import default_error_coercer
from tartiflette.schema.bakery import SchemaBakery
from tartiflette.schema.registry import SchemaRegistry


def _import_modules(modules):
    if modules:
        invalidate_caches()
        return [import_module(x) for x in modules]
    return []


class Engine:
    def __init__(
        self,
        sdl: Union[str, List[str]],
        schema_name: str = "default",
        error_coercer: Callable[[Exception], dict] = default_error_coercer,
        custom_default_resolver: Optional[Callable] = None,
        exclude_builtins_scalars: Optional[List[str]] = None,
        modules: Optional[Union[str, List[str]]] = None,
    ) -> None:
        """Create an engine by analyzing the SDL and connecting it with the imported Resolver, Mutation,
        Subscription, Directive and Scalar linking them through the schema_name.

        Then using `await an_engine.execute(query)` will resolve your GQL requests.

        Arguments:
            sdl {Union[str, List[str]]} -- The SDL to work with.

        Keyword Arguments:
            schema_name {str} -- The name of the SDL (default: {"default"})
            error_coercer {Callable[[Exception], dict]} -- An optional callable in charge of transforming an Exception into an error dict (default: {default_error_coercer})
            custom_default_resolver {Optional[Callable]} -- An optional callable that will replace the tartiflette default_resolver (Will be called like a resolver for each UNDECORATED field) (default: {None})
            exclude_builtins_scalars {Optional[List[str]]} -- An optional list of string containing the names of the builtin scalar you don't want to be automatically included, usually it's Date, DateTime or Time scalars (default: {None})
            modules {Optional[Union[str, List[str]]]} -- An optional list of string containing the name of the modules you want the engine to import, usually this modules contains your Resolvers, Directives, Scalar or Subscription code (default: {None})
        """

        if isinstance(modules, str):
            modules = [modules]

        self._modules = _import_modules(modules)

        self._error_coercer = error_coercer
        self._parser = TartifletteRequestParser()
        SchemaRegistry.register_sdl(schema_name, sdl, exclude_builtins_scalars)
        self._schema = SchemaBakery.bake(
            schema_name, custom_default_resolver, exclude_builtins_scalars
        )

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
        document, errors = parse_and_validate_query(query)
        if errors:
            return build_response(
                errors=errors, error_coercer=self._error_coercer
            )

        execution_context, errors = build_execution_context(
            self._schema,
            document,
            initial_value,
            context,
            variables,
            operation_name,
        )

        if errors:
            return build_response(
                errors=errors, error_coercer=self._error_coercer
            )

        return await execute_operation(
            execution_context, error_coercer=self._error_coercer
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
        document, errors = parse_and_validate_query(query)
        if errors:
            yield build_response(
                errors=errors, error_coercer=self._error_coercer
            )
            return

        execution_context, errors = build_execution_context(
            self._schema,
            document,
            initial_value,
            context,
            variables,
            operation_name,
        )

        if errors:
            yield build_response(
                errors=errors, error_coercer=self._error_coercer
            )
            return

        async for result in run_subscription(
            execution_context, error_coercer=self._error_coercer
        ):
            yield result
