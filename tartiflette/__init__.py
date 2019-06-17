from typing import Callable, List, Optional, Union

from tartiflette.resolver import Resolver, ResolverExecutorFactory
from tartiflette.subscription import Subscription
from tartiflette.sdl import build_graphql_schema_from_sdl
from tartiflette.engine import Engine
from tartiflette.scalar import Scalar
from tartiflette.directive import Directive
from tartiflette.types.exceptions import TartifletteError


async def create_engine(
    sdl: Union[str, List[str]],
    schema_name: str = "default",
    error_coercer: Callable[[Exception], dict] = None,
    custom_default_resolver: Optional[Callable] = None,
    modules: Optional[Union[str, List[str]]] = None,
) -> Engine:
    """
    Create an engine by analyzing the SDL and connecting it with the imported Resolver, Mutation,
    Subscription, Directive and Scalar linking them through the schema_name.

    Then using `await an_engine.execute(query)` will resolve your GQL requests.

    Arguments:
        sdl {Union[str, List[str]]} -- The SDL to work with.

    Keyword Arguments:
        schema_name {str} -- The name of the SDL (default: {"default"})
        error_coercer {Callable[[Exception, dict], dict]} -- An optional callable in charge of transforming a couple Exception/error into an error dict (default: {default_error_coercer})
        custom_default_resolver {Optional[Callable]} -- An optional callable that will replace the tartiflette default_resolver (Will be called like a resolver for each UNDECORATED field) (default: {None})
        modules {Optional[Union[str, List[str]]]} -- An optional list of string containing the name of the modules you want the engine to import, usually this modules contains your Resolvers, Directives, Scalar or Subscription code (default: {None})

    Returns:
        a Cooked Engine instance
    """
    e = Engine()

    await e.cook(
        sdl=sdl,
        error_coercer=error_coercer,
        custom_default_resolver=custom_default_resolver,
        modules=modules,
        schema_name=schema_name,
    )

    return e
