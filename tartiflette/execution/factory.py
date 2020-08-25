from functools import partial
from typing import Any, AsyncIterable, Callable, Dict, List, Optional, Union

from tartiflette.execution.execute import create_source_event_stream, execute
from tartiflette.execution.parser import parse_and_validate_query
from tartiflette.execution.response import (
    build_response as default_build_response,
)
from tartiflette.schema.registry import SchemaRegistry
from tartiflette.schema.schema import GraphQLSchema
from tartiflette.types.exceptions.tartiflette import (
    ImproperlyConfigured,
    NonCoroutine,
)
from tartiflette.utils.callables import is_valid_coroutine
from tartiflette.utils.errors import (
    default_error_coercer,
    error_coercer_factory,
)

__all__ = ("executor_factory", "subscriptor_factory")


class BaseOperator:
    """
    Base class for operators.
    """

    def __init__(
        self,
        schema: Union[str, "GraphQLSchema"],
        error_coercer: Callable[
            [Exception, Dict[str, Any]], Dict[str, Any]
        ] = None,
        cache_decorator: Optional[Callable] = None,
        parser: Optional[Callable] = None,
        rules: Optional[List["ValidationRule"]] = None,
    ) -> None:
        """
        :param schema: the schema name or instance to operate
        :param error_coercer: callable used to transform an exception into an
        error
        :param cache_decorator: decorator to use over the query parsing
        :param parser: parser to use to parse the query into a document
        :param rules: validation rules to apply to queries
        :type schema: Union[str, "GraphQLSchema"]
        :type error_coercer: Callable[
            [Exception, Dict[str, Any]], Dict[str, Any]
        ]
        :type cache_decorator: Optional[Callable]
        :type parser: Optional[Callable]
        :type rules: Optional[List["ValidationRule"]]
        """
        if isinstance(schema, str):
            if SchemaRegistry.is_schema_registered(schema):
                schema = SchemaRegistry.find_schema(schema)
            else:
                raise ImproperlyConfigured(
                    f"< {schema} > schema isn't registered."
                )
        elif not isinstance(schema, GraphQLSchema):
            raise ImproperlyConfigured(
                "< schema > argument should be either a schema name or a "
                "GraphQLSchema instance."
            )

        if error_coercer and not is_valid_coroutine(error_coercer):
            raise NonCoroutine(
                "Given < error_coercer > is not a coroutine callable."
            )

        prepared_parse_and_validate_query = partial(
            parse_and_validate_query, parser=parser, rules=rules,
        )

        self._schema: "GraphQLSchema" = schema
        self._response_builder: Callable = partial(
            default_build_response,
            error_coercer=error_coercer_factory(
                error_coercer or default_error_coercer
            ),
        )
        self._parse_and_validate_query: Callable = (
            cache_decorator(prepared_parse_and_validate_query)
            if callable(cache_decorator)
            else prepared_parse_and_validate_query
        )


class ExecutorOperator(BaseOperator):
    def __init__(
        self,
        schema: Union[str, "GraphQLSchema"],
        error_coercer: Callable[
            [Exception, Dict[str, Any]], Dict[str, Any]
        ] = None,
        cache_decorator: Optional[Callable] = None,
        parser: Optional[Callable] = None,
        rules: Optional[List["ValidationRule"]] = None,
    ) -> None:
        """
        :param schema: the schema name or instance to operate
        :param error_coercer: callable used to transform an exception into an
        error
        :param cache_decorator: decorator to use over the query parsing
        :param parser: parser to use to parse the query into a document
        :param rules: validation rules to apply to queries
        :type schema: Union[str, "GraphQLSchema"]
        :type error_coercer: Callable[
            [Exception, Dict[str, Any]], Dict[str, Any]
        ]
        :type cache_decorator: Optional[Callable]
        :type parser: Optional[Callable]
        :type rules: Optional[List["ValidationRule"]]
        """
        super().__init__(schema, error_coercer, cache_decorator, parser, rules)
        self._directived_executor = self._schema.bake_executor(self._executor)

    async def _executor(
        self,
        schema: "GraphQLSchema",
        document: "DocumentNode",
        request_parsing_errors: Optional[List["TartifletteError"]] = None,
        operation_name: Optional[str] = None,
        context: Optional[Any] = None,
        variables: Optional[Dict[str, Any]] = None,
        initial_value: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """
        Execute the query if no parsing errors raised.
        :param schema: the GraphQLSchema linked to the operator
        :param document: DocumentNode parsed query
        :param request_parsing_errors: list of potential parsing errors
        :param operation_name: the operation name to execute
        :param context: value that can contain everything you need and that
        will be accessible from the resolvers
        :param variables: the variables provided in the GraphQL request
        :param initial_value: an initial value corresponding to the root type
        being executed
        :type schema: GraphQLSchema
        :type document: DocumentNode
        :type request_parsing_errors: Optional[List["TartifletteError"]]
        :type operation_name: Optional[str]
        :type context: Optional[Any]
        :type variables: Optional[Dict[str, Any]]
        :type initial_value: Optional[Any]
        :return: computed response corresponding to the request
        :rtype: Dict[str, Any]
        """
        if request_parsing_errors:
            return await self._response_builder(errors=request_parsing_errors)
        return await execute(
            schema,
            document,
            self._response_builder,
            initial_value,
            context,
            variables,
            operation_name,
        )

    async def __call__(
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
        document, errors = self._parse_and_validate_query(query, self._schema)
        return await self._directived_executor(
            self._schema,
            document,
            errors,
            operation_name,
            context,
            variables,
            initial_value,
            context_coercer=context,
        )


class SubscriptorOperator(BaseOperator):
    def __init__(
        self,
        schema: Union[str, "GraphQLSchema"],
        error_coercer: Callable[
            [Exception, Dict[str, Any]], Dict[str, Any]
        ] = None,
        cache_decorator: Optional[Callable] = None,
        parser: Optional[Callable] = None,
        rules: Optional[List["ValidationRule"]] = None,
    ) -> None:
        """
        :param schema: the schema name or instance to operate
        :param error_coercer: callable used to transform an exception into an
        error
        :param cache_decorator: decorator to use over the query parsing
        :param parser: parser to use to parse the query into a document
        :param rules: validation rules to apply to queries
        :type schema: Union[str, "GraphQLSchema"]
        :type error_coercer: Callable[
            [Exception, Dict[str, Any]], Dict[str, Any]
        ]
        :type cache_decorator: Optional[Callable]
        :type parser: Optional[Callable]
        :type rules: Optional[List["ValidationRule"]]
        """
        super().__init__(schema, error_coercer, cache_decorator, parser, rules)
        self._directived_subscriptor = self._schema.bake_subscriptor(
            self._subscriptor
        )

    async def _subscriptor(
        self,
        schema: "GraphQLSchema",
        document: "DocumentNode",
        request_parsing_errors: Optional[List["TartifletteError"]] = None,
        operation_name: Optional[str] = None,
        context: Optional[Any] = None,
        variables: Optional[Dict[str, Any]] = None,
        initial_value: Optional[Any] = None,
    ):
        """
        Execute the subscription query if no parsing errors raised.
        :param schema: the GraphQLSchema linked to the operator
        :param document: DocumentNode parsed query
        :param request_parsing_errors: list of potential parsing errors
        :param operation_name: the operation name to execute
        :param context: value that can contain everything you need and that
        will be accessible from the resolvers
        :param variables: the variables provided in the GraphQL request
        :param initial_value: an initial value corresponding to the root type
        being executed
        :type schema: GraphQLSchema
        :type document: DocumentNode
        :type request_parsing_errors: Optional[List["TartifletteError"]]
        :type operation_name: Optional[str]
        :type context: Optional[Any]
        :type variables: Optional[Dict[str, Any]]
        :type initial_value: Optional[Any]
        :return: computed response corresponding to the request
        :rtype: AsyncIterable[Dict[str, Any]]
        """
        # pylint: disable=too-many-locals
        if request_parsing_errors:
            yield await self._response_builder(errors=request_parsing_errors)
            return

        source_event_stream = await create_source_event_stream(
            schema,
            document,
            self._response_builder,
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
                schema,
                document,
                self._response_builder,
                payload,
                context,
                variables,
                operation_name,
            )

    async def __call__(
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
        document, errors = self._parse_and_validate_query(query, self._schema)

        # Goes through potential schema directives and finish in self._perform_subscription
        async for payload in self._directived_subscriptor(
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


def executor_factory(
    schema: Union[str, "GraphQLSchema"],
    error_coercer: Callable[
        [Exception, Dict[str, Any]], Dict[str, Any]
    ] = None,
    cache_decorator: Optional[Callable] = None,
    parser: Optional[Callable] = None,
    rules: Optional[List["ValidationRule"]] = None,
) -> "ExecutorOperator":
    """
    Create an executor operator for the provided schema.
    :param schema: the schema name or instance to operate
    :param error_coercer: callable used to transform an exception into an error
    :param cache_decorator: decorator to use over the query parsing
    :param parser: parser to use to parse the query into a document
    :param rules: validation rules to apply to queries
    :type schema: Union[str, "GraphQLSchema"]
    :type error_coercer: Callable[
        [Exception, Dict[str, Any]], Dict[str, Any]
    ]
    :type cache_decorator: Optional[Callable]
    :type parser: Optional[Callable]
    :type rules: Optional[List["ValidationRule"]]
    :return: an executor operator for the provided schema
    :rtype: ExecutorOperator
    """
    return ExecutorOperator(
        schema, error_coercer, cache_decorator, parser, rules
    )


def subscriptor_factory(
    schema: Union[str, "GraphQLSchema"],
    error_coercer: Callable[
        [Exception, Dict[str, Any]], Dict[str, Any]
    ] = None,
    cache_decorator: Optional[Callable] = None,
    parser: Optional[Callable] = None,
    rules: Optional[List["ValidationRule"]] = None,
) -> "SubscriptorOperator":
    """
    Create a subscriptor operator for the provided schema.
    :param schema: the schema name or instance to operate
    :param error_coercer: callable used to transform an exception into an error
    :param cache_decorator: decorator to use over the query parsing
    :param parser: parser to use to parse the query into a document
    :param rules: validation rules to apply to queries
    :type schema: Union[str, "GraphQLSchema"]
    :type error_coercer: Callable[
        [Exception, Dict[str, Any]], Dict[str, Any]
    ]
    :type cache_decorator: Optional[Callable]
    :type parser: Optional[Callable]
    :type rules: Optional[List["ValidationRule"]]
    :return: a subscriptor operator for the provided schema
    :rtype: SubscriptorOperator
    """
    return SubscriptorOperator(
        schema, error_coercer, cache_decorator, parser, rules
    )
