from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from tartiflette.directive.directive import Directive
from tartiflette.execution.factory import executor_factory, subscriptor_factory
from tartiflette.resolver.resolver import Resolver
from tartiflette.resolver.type_resolver import TypeResolver
from tartiflette.scalar.scalar import Scalar
from tartiflette.schema.factory import create_schema
from tartiflette.subscription.subscription import Subscription
from tartiflette.types.exceptions import TartifletteError

__all__ = (
    "Directive",
    "Resolver",
    "TypeResolver",
    "Scalar",
    "Subscription",
    "TartifletteError",
    "create_schema",
    "executor_factory",
    "subscriptor_factory",
    "create_schema_with_operators",
)


async def create_schema_with_operators(
    sdl: Union[str, List[str]],
    name: str = "default",
    modules: Optional[Union[str, List[str], List[Dict[str, Any]]]] = None,
    default_resolver: Optional[Callable] = None,
    default_type_resolver: Optional[Callable] = None,
    default_arguments_coercer: Optional[Callable] = None,
    sdl_parser: Optional[Callable] = None,
    error_coercer: Callable[
        [Exception, Dict[str, Any]], Dict[str, Any]
    ] = None,
    query_cache_decorator: Optional[Callable] = None,
    query_parser: Optional[Callable] = None,
    rules: Optional[List["ValidationRule"]] = None,
) -> Tuple["GraphQLSchema", Callable, Callable]:
    """
    Create a GraphQLSchema along with their operators.
    :param sdl: the SDL to related to the schema
    :param name: name of the schema
    :param modules: list Python modules to load
    :param default_resolver: the default resolver to use
    :param default_type_resolver: the default type resolver to use
    :param default_arguments_coercer: callable to use to coerce arguments
    :param sdl_parser: parser to use to parse the SDL into a document
    :param error_coercer: callable used to transform an exception into an error
    :param query_cache_decorator: decorator to use over the query parsing
    :param query_parser: parser to use to parse the query into a document
    :param rules: validation rules to apply to queries
    :type sdl: Union[str, List[str]]
    :type name: str
    :type modules: Optional[Union[str, List[str], List[Dict[str, Any]]]]
    :type default_resolver: Optional[Callable]
    :type default_type_resolver: Optional[Callable]
    :type default_arguments_coercer: Optional[Callable]
    :type sdl_parser: Optional[Callable]
    :type error_coercer: Callable[
        [Exception, Dict[str, Any]], Dict[str, Any]
    ]
    :type query_cache_decorator: Optional[Callable]
    :type query_parser: Optional[Callable]
    :type rules: Optional[List["ValidationRule"]]
    :return: a GraphQLSchema along with their operators
    :rtype: Tuple["GraphQLSchema", Callable, Callable]
    """
    # pylint: disable=too-many-arguments
    schema = await create_schema(
        sdl,
        name=name,
        modules=modules,
        default_resolver=default_resolver,
        default_type_resolver=default_type_resolver,
        default_arguments_coercer=default_arguments_coercer,
        parser=sdl_parser,
    )
    return (
        schema,
        executor_factory(
            schema,
            error_coercer=error_coercer,
            cache_decorator=query_cache_decorator,
            parser=query_parser,
            rules=rules,
        ),
        subscriptor_factory(
            schema,
            error_coercer=error_coercer,
            cache_decorator=query_cache_decorator,
            parser=query_parser,
            rules=rules,
        ),
    )
