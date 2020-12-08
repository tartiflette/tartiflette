from typing import Any, Callable, Dict, List, Optional, Union

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.directive.directive import Directive
from tartiflette.engine import Engine
from tartiflette.resolver.resolver import Resolver
from tartiflette.resolver.type_resolver import TypeResolver
from tartiflette.scalar.scalar import Scalar
from tartiflette.subscription.subscription import Subscription
from tartiflette.types.exceptions import TartifletteError

__all__ = (
    "create_engine",
    "Directive",
    "Engine",
    "Resolver",
    "TypeResolver",
    "Scalar",
    "Subscription",
    "TartifletteError",
)


async def create_engine(
    sdl: Union[str, List[str]],
    schema_name: str = "default",
    error_coercer: Callable[
        [Exception, Dict[str, Any]], Dict[str, Any]
    ] = None,
    custom_default_resolver: Optional[Callable] = None,
    custom_default_type_resolver: Optional[Callable] = None,
    modules: Optional[Union[str, List[str], List[Dict[str, Any]]]] = None,
    query_cache_decorator: Optional[Callable] = UNDEFINED_VALUE,
    json_loader: Optional[Callable[[str], Dict[str, Any]]] = None,
    custom_default_arguments_coercer: Optional[Callable] = None,
    coerce_list_concurrently: Optional[bool] = None,
    coerce_parent_concurrently: Optional[bool] = None,
) -> "Engine":
    """
    Create an engine by analyzing the SDL and connecting it with the imported
    Resolver, Mutation, Subscription, Directive and Scalar linking them through
    the `schema_name`.
    :param sdl: the SDL to work with
    :param schema_name: the name of the SDL
    :param error_coercer: callable in charge of transforming a couple
    Exception/error into an error dictionary
    :param custom_default_resolver: callable that will replace the tartiflette
    `default_resolver` (Will be called like a resolver for each UNDECORATED
    field)
    :param custom_default_type_resolver: callable that will replace the
    tartiflette `default_type_resolver` (will be called on abstract types to
    deduct the type of a result)
    :param modules: list of string containing the name of the modules you want
    the engine to import, usually this modules contains your Resolvers,
    Directives, Scalar or Subscription code
    :param query_cache_decorator: callable that will replace the tartiflette
    default lru_cache decorator to cache query parsing
    :param json_loader: A callable that will replace default python
    json module.loads for ast_json loading
    :param custom_default_arguments_coercer: callable that will replace the
    :param coerce_list_concurrently: whether or not list will be coerced
    concurrently
    :param coerce_parent_concurrently: whether or not field will be coerced
    concurrently
    tartiflette `default_arguments_coercer
    :type sdl: Union[str, List[str]]
    :type schema_name: str
    :type error_coercer: Callable[[Exception, Dict[str, Any]], Dict[str, Any]]
    :type custom_default_resolver: Optional[Callable]
    :type custom_default_type_resolver: Optional[Callable]
    :type modules: Optional[Union[str, List[str], List[Dict[str, Any]]]]
    :type query_cache_decorator: Optional[Callable]
    :type json_loader: Optional[Callable[[str], Dict[str, Any]]]
    :type custom_default_arguments_coercer: Optional[Callable]
    :type coerce_list_concurrently: Optional[bool]
    :type coerce_parent_concurrently: Optional[bool]
    :return: a Cooked Engine instance
    :rtype: Engine

    :Example:

    >>> from tartiflette import create_engine
    >>>
    >>>
    >>> engine = await create_engine('''type Query {
    >>>   hello(name: String!): String!
    >>> }''')
    """
    # pylint: disable=too-many-arguments
    e = Engine()

    await e.cook(
        sdl=sdl,
        error_coercer=error_coercer,
        custom_default_resolver=custom_default_resolver,
        custom_default_type_resolver=custom_default_type_resolver,
        modules=modules,
        schema_name=schema_name,
        query_cache_decorator=query_cache_decorator,
        json_loader=json_loader,
        custom_default_arguments_coercer=custom_default_arguments_coercer,
        coerce_list_concurrently=coerce_list_concurrently,
        coerce_parent_concurrently=coerce_parent_concurrently,
    )

    return e
