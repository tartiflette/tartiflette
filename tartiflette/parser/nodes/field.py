import asyncio
from typing import Any, Callable, Dict, List

from tartiflette.executors.types import ExecutionContext, Info
from tartiflette.schema import GraphQLSchema
from tartiflette.types.exceptions.tartiflette import GraphQLError
from tartiflette.types.location import Location
from tartiflette.types.helpers import get_typename

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
        alias: str = None,
    ):
        super().__init__(path, "Field", location, name)
        # Execution
        self.schema = schema
        self.field_executor = field_executor
        self.arguments = {}
        self.type_condition = type_condition
        self.marshalled = {}
        self.alias = alias if alias is not None else self.name

    @property
    def cant_be_null(self) -> bool:
        return self.field_executor.cant_be_null

    @property
    def contains_not_null(self) -> bool:
        return self.field_executor.contains_not_null

    @property
    def shall_produce_list(self) -> bool:
        return self.field_executor.shall_produce_list

    def bubble_error(self):
        if self.cant_be_null is False:
            # mean i can be null
            if self.parent:
                self.parent.marshalled[self.alias] = None
            else:
                self.marshalled = None
        else:
            if self.parent:
                self.parent.bubble_error()
            else:
                self.marshalled = None

    def _get_coroutz_from_child(
        self, exec_ctx, request_ctx, result, coerced, raw_typename
    ):
        coroutz = []
        for child in self.children:
            if (
                child.type_condition
                and child.type_condition == raw_typename
                or not child.type_condition
            ):
                coroutz.append(
                    child(
                        exec_ctx,
                        request_ctx,
                        parent_result=result,
                        parent_marshalled=coerced,
                    )
                )
        return coroutz

    async def _execute_children(self, exec_ctx, request_ctx, result, coerced):
        coroutz = []
        if self.shall_produce_list:
            for index, raw in enumerate(result):
                raw_typename = get_typename(raw)
                coroutz = coroutz + self._get_coroutz_from_child(
                    exec_ctx, request_ctx, raw, coerced[index], raw_typename
                )
        else:
            raw_typename = get_typename(result)
            coroutz = self._get_coroutz_from_child(
                exec_ctx, request_ctx, result, coerced, raw_typename
            )

        await asyncio.gather(*coroutz, return_exceptions=False)

    async def __call__(
        self,
        exec_ctx: ExecutionContext,
        request_ctx: Dict[str, Any],
        parent_result=None,
        parent_marshalled=None,
    ) -> Any:

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
                execution_ctx=exec_ctx,
            ),
        )

        if parent_marshalled is not None:
            parent_marshalled[self.alias] = coerced
        else:
            self.marshalled = coerced

        if isinstance(raw, Exception):
            gql_error = GraphQLError(str(raw), self.path, [self.location])
            if (
                (self.cant_be_null or self.contains_not_null)
                and self.parent
                and self.cant_be_null
            ):
                self.parent.bubble_error()
            exec_ctx.add_error(gql_error)
        else:
            if self.children:
                await self._execute_children(
                    exec_ctx, request_ctx, result=raw, coerced=coerced
                )
