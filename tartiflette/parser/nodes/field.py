import asyncio

from functools import partial
from typing import Any, Callable, Coroutine, Dict, List, Optional

from tartiflette.executors.types import ExecutionContext, Info
from tartiflette.schema import GraphQLSchema
from tartiflette.types.exceptions.tartiflette import GraphQLError
from tartiflette.types.helpers import get_typename
from tartiflette.types.location import Location
from tartiflette.utils.arguments import coerce_arguments

from .node import Node


class NodeField(Node):
    def __init__(
        self,
        name: str,
        schema: GraphQLSchema,
        field_executor: Callable,
        location: Location,
        path: List[str],
        type_condition: str,
        alias: Optional[str] = None,
        subscribe: Optional[Callable] = None,
    ) -> None:
        # pylint: disable=too-many-arguments
        super().__init__(path, "Field", location, name)
        # Execution
        self.schema = schema
        self.field_executor = field_executor
        self.arguments: Dict[str, Any] = {}
        self.type_condition = type_condition
        self.marshalled: Dict[str, Any] = {}
        self.alias = alias or self.name
        self.subscribe = subscribe

    @property
    def cant_be_null(self) -> bool:
        return self.field_executor.cant_be_null

    @property
    def contains_not_null(self) -> bool:
        return self.field_executor.contains_not_null

    @property
    def shall_produce_list(self) -> bool:
        return self.field_executor.shall_produce_list

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
            for child in self.children
            if (child.type_condition and child.type_condition == raw_typename)
            or not child.type_condition
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
        execution_ctx: ExecutionContext,
        request_ctx: Optional[Dict[str, Any]],
        parent_result: Optional[Any] = None,
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
            execution_ctx=execution_ctx,
        )

        return self.subscribe(
            parent_result,
            await coerce_arguments(
                self.field_executor.schema_field.arguments,
                self.arguments,
                request_ctx,
                info,
            ),
            request_ctx,
            info,
        )

    async def __call__(
        self,
        execution_ctx: ExecutionContext,
        request_ctx: Optional[Dict[str, Any]],
        parent_result: Optional[Any] = None,
        parent_marshalled: Optional[Any] = None,
    ) -> None:
        raw, coerced = await self.field_executor(
            parent_result,
            self.arguments,
            request_ctx,
            Info(
                query_field=self,
                schema_field=self.field_executor.schema_field,
                schema=self.schema,
                path=self.path,
                location=self.location,
                execution_ctx=execution_ctx,
            ),
        )

        if parent_marshalled is not None:
            parent_marshalled[self.alias] = coerced
        else:
            self.marshalled = coerced

        if isinstance(raw, Exception):
            try:
                if callable(raw.coerce_value):
                    gql_error = raw
            except (TypeError, AttributeError):
                gql_error = GraphQLError(str(raw), self.path, [self.location])

            gql_error.coerce_value = partial(
                gql_error.coerce_value,
                path=self.path,
                locations=[self.location],
            )

            if (
                (self.cant_be_null or self.contains_not_null)
                and self.parent
                and self.cant_be_null
            ):
                self.parent.bubble_error()
            execution_ctx.add_error(gql_error)
        elif self.children and raw is not None:
            await self._execute_children(
                execution_ctx, request_ctx, result=raw, coerced=coerced
            )
