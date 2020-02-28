from typing import Any, Callable, Dict, List, Optional, Union

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
    lru_cache_maxsize: Optional[int] = None,
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
    :param lru_cache_maxsize: max number of queries cached with lru_cache
    :type sdl: Union[str, List[str]]
    :type schema_name: str
    :type error_coercer: Callable[[Exception, Dict[str, Any]], Dict[str, Any]]
    :type custom_default_resolver: Optional[Callable]
    :type custom_default_type_resolver: Optional[Callable]
    :type modules: Optional[Union[str, List[str], List[Dict[str, Any]]]]
    :type lru_cache_maxsize: Optional[int]
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
    e = Engine()

    await e.cook(
        sdl=sdl,
        error_coercer=error_coercer,
        custom_default_resolver=custom_default_resolver,
        custom_default_type_resolver=custom_default_type_resolver,
        modules=modules,
        schema_name=schema_name,
        lru_cache_maxsize=lru_cache_maxsize,
    )

    return e
