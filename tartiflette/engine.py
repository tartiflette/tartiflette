from importlib import import_module, invalidate_caches
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
from tartiflette.types.exceptions.tartiflette import GraphQLError
from tartiflette.utils.errors import to_graphql_error


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
            error_coercer {Callable[[Exception, dict], dict]} -- An optional callable in charge of transforming a couple Exception/error into an error dict (default: {default_error_coercer})
            custom_default_resolver {Optional[Callable]} -- An optional callable that will replace the tartiflette default_resolver (Will be called like a resolver for each UNDECORATED field) (default: {None})
            exclude_builtins_scalars {Optional[List[str]]} -- An optional list of string containing the names of the builtin scalar you don't want to be automatically included, usually it's Date, DateTime or Time scalars (default: {None})
            modules {Optional[Union[str, List[str]]]} -- An optional list of string containing the name of the modules you want the engine to import, usually this modules contains your Resolvers, Directives, Scalar or Subscription code (default: {None})
        """

        if isinstance(modules, str):
            modules = [modules]

        self._modules = _import_modules(modules)

        self._error_coercer = error_coercer_factory(error_coercer)
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
