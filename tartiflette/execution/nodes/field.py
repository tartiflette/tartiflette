import asyncio

from functools import partial
from typing import Any, Callable, Coroutine, Dict, List, Optional, Union

from tartiflette.executors.types import Info
from tartiflette.types.exceptions import GraphQLError
from tartiflette.types.exceptions.tartiflette import (
    MultipleException,
    SkipExecution,
)
from tartiflette.types.helpers import get_typename
from tartiflette.utils.arguments import coerce_arguments
from tartiflette.utils.errors import is_coercible_exception


class ExecutableFieldNode:
    """
    Node representing a GraphQL executable field.
    """

    def __init__(
        self,
        name: str,
        schema: "GraphQLSchema",
        resolver: Callable,
        path: List[str],
        type_condition: str,
        alias: Optional[str] = None,
        subscribe: Optional[Callable] = None,
        parent: Optional["ExecutableFieldNode"] = None,
        fields: Optional[List["ExecutableFieldNode"]] = None,
        arguments: Optional[Dict[str, Any]] = None,
        directives: Optional[List["DirectiveNode"]] = None,
    ) -> None:
        """
        :param name: name of the field
        :param schema: GraphQLSchema to use while executing the field
        :param resolver: callable to use to resolve the field
        :param path: path of the field in the query
        :param type_condition: type condition of the field
        :param alias: alias of the field
        :param subscribe: callable to use on subscription requests
        :param parent: parent executable field of the field
        :param fields: collected executable fields of the field
        :param arguments: arguments of the field
        :param directives: directives of the field
        :type name: str
        :type schema: GraphQLSchema
        :type resolver: Callable
        :type path: List[str]
        :type type_condition: str
        :type alias: Optional[str]
        :type subscribe: Optional[Callable]
        :type parent: Optional[ExecutableFieldNode]
        :type fields: Optional[List[ExecutableFieldNode]]
        :type arguments: Optional[Dict[str, Any]]
        :type directives: Optional[List[DirectiveNode]]
        """
        # pylint: disable=too-many-arguments,too-many-locals
        self.name = name
        self.schema = schema
        self.resolver = resolver
        self.path = path
        self.type_condition = type_condition
        self.alias = alias
        self.subscribe = subscribe
        self.parent = parent
        self.fields = fields if fields is not None else {}
        self.arguments = arguments if arguments is not None else {}
        self.directives = directives if directives is not None else []
        self.definitions: List["FieldNode"] = []

        # TODO: retrocompatibility old execution style
        self.children = fields
        self.field_executor = resolver
        self.marshalled: Dict[str, Any] = {}
        self.alias = alias or self.name
        self.is_execution_stopped = False
        self.execution_directives = directives
        self.location = None

    def __repr__(self) -> str:
        """
        Returns the representation of an ExecutableFieldNode instance.
        :return: the representation of an ExecutableFieldNode instance
        :rtype: str
        """
        return (
            "ExecutableFieldNode(alias=%r, name=%r, type_condition=%r, "
            "path=%r, fields=%r, arguments=%r, directives=%r, "
            "definitions=%r)"
            % (
                self.alias,
                self.name,
                self.type_condition,
                self.path,
                self.fields,
                self.arguments,
                self.directives,
                self.definitions,
            )
        )

    @property
    def cant_be_null(self) -> bool:
        return self.field_executor.cant_be_null

    @property
    def contains_not_null(self) -> bool:
        return self.field_executor.contains_not_null

    @property
    def shall_produce_list(self) -> bool:
        return self.field_executor.shall_produce_list

    def add_directive(
        self, directive: Dict[str, Union["Directive", Dict[str, Any]]]
    ):
        self.execution_directives.append(directive)

    def bubble_error(self) -> None:
        if self.cant_be_null is False:
            # mean i can be null
            if self.parent and self.parent.marshalled is not None:
                self.parent.marshalled[self.alias] = None
            else:
                self.marshalled = None
        else:
            if self.parent:
                self.parent.bubble_error()
            else:
                self.marshalled = None

    def _get_coroutz_from_child(
        self,
        execution_ctx: "ExecutionContext",
        request_ctx: Optional[Dict[str, Any]],
        result: Optional[Any],
        coerced: Optional[Any],
        raw_typename: str,
    ) -> List[Coroutine]:
        return [
            child(
                execution_ctx,
                request_ctx,
                parent_result=result,
                parent_marshalled=coerced,
            )
            for child in list(self.fields[raw_typename].values())
        ]

    async def _execute_children(
        self,
        execution_ctx: "ExecutionContext",
        request_ctx: Optional[Dict[str, Any]],
        result: Optional[Any],
        coerced: Optional[Any],
    ) -> None:
        coroutz = []
        if self.shall_produce_list:
            # TODO Better manage of None values here. (Should be transformed by coerce)
            if isinstance(result, list) and isinstance(coerced, list):
                for index, raw in enumerate(result):
                    raw_typename = get_typename(raw)
                    coroutz = coroutz + self._get_coroutz_from_child(
                        execution_ctx,
                        request_ctx,
                        raw,
                        coerced[index],
                        raw_typename,
                    )
        else:
            raw_typename = get_typename(result)
            coroutz = self._get_coroutz_from_child(
                execution_ctx, request_ctx, result, coerced, raw_typename
            )

        await asyncio.gather(*coroutz, return_exceptions=False)

    async def create_source_event_stream(
        self,
        execution_context: "ExecutionContext",
        initial_value: Optional[Any],
    ):
        if not self.subscribe:
            raise GraphQLError(
                "Can't execute a subscription query on a field which doesn't "
                "provide a source event stream with < @Subscription >."
            )

        info = Info(
            query_field=self,
            schema_field=self.field_executor.schema_field,
            schema=self.schema,
            path=self.path,
            location=self.location,
            execution_ctx=execution_context,
        )

        from tartiflette.execution import get_argument_values

        return self.subscribe(
            initial_value,
            await coerce_arguments(
                self.field_executor.schema_field.arguments,
                get_argument_values(
                    self.field_executor.schema_field.arguments,
                    self.definitions[0],
                    execution_context.variable_values,
                ),
                execution_context.context,
                info,
            ),
            execution_context.context,
            info,
        )

    async def __call__(
        self,
        execution_ctx: "ExecutionContext",
        request_ctx: Optional[Dict[str, Any]],
        parent_result: Optional[Any] = None,
        parent_marshalled: Optional[Any] = None,
    ) -> None:
        from tartiflette.execution import get_argument_values

        try:
            raw, coerced = await self.field_executor(
                execution_ctx,
                parent_result,
                request_ctx,
                Info(
                    query_field=self,
                    schema_field=self.field_executor.schema_field,
                    schema=self.schema,
                    path=self.path,
                    location=self.location,
                    execution_ctx=execution_ctx,
                ),
                execution_directives=self.directives,
                field_nodes=self.definitions,
            )
        except SkipExecution:
            self.is_execution_stopped = True
            return  # field_executor asked execution to be stopped for this branch

        if parent_marshalled is not None:
            parent_marshalled[self.alias] = coerced
        else:
            self.marshalled = coerced

        if isinstance(raw, Exception):
            if (
                (self.cant_be_null or self.contains_not_null)
                and self.parent
                and self.cant_be_null
            ):
                self.parent.bubble_error()

            execution_ctx.add_error(
                raw,
                path=self.path,
                locations=[
                    definition.location for definition in self.definitions
                ],
            )
        elif self.fields and raw is not None:
            await self._execute_children(
                execution_ctx, request_ctx, result=raw, coerced=coerced
            )
