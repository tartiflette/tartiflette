import asyncio
from typing import List, Any, Dict

from tartiflette.executors.types import Info, CoercedValue
from tartiflette.schema import GraphQLSchema
from tartiflette.types.exceptions.tartiflette import GraphQLError
from tartiflette.types.field import GraphQLField
from tartiflette.types.location import Location
from .node import Node


async def _exec_list(
        parent_result_lst: List, args: Dict[str, Any],
        request_ctx: Dict[str, Any], path: List[str], location: Location,
        schema: GraphQLSchema, schema_field: GraphQLField,
        query_field: 'NodeField',
):
    coroutines = []

    for index, parent_result_item in enumerate(parent_result_lst):
        new_path = path[:]
        new_path.append(index)
        if isinstance(parent_result_item, list):
            coroutines.append(
                _exec_list(
                    parent_result_item,
                    args,
                    request_ctx,
                    new_path[:],
                    location,
                    schema,
                    schema_field,
                    query_field,
                )
            )
        else:
            coroutines.append(
                schema_field.resolver(
                    parent_result_item,
                    args,
                    request_ctx,
                    Info(
                        query_field=query_field,
                        schema_field=schema_field,
                        schema=schema,
                        path=new_path[:],
                        location=location,
                    ),
                )
            )

    raw_results = await asyncio.gather(*coroutines, return_exceptions=True)
    results = []
    coerced_value = CoercedValue(value=[], error=None)
    for tmp_result, tmp_coerced_value in raw_results:
        results.append(tmp_result)
        coerced_value.value.append(tmp_coerced_value.value)
        if tmp_coerced_value.error:
            coerced_value.error = tmp_coerced_value.error
    return results, coerced_value


class NodeField(Node):
    def __init__(
            self,
            name: str,
            schema: GraphQLSchema,
            schema_field: GraphQLField,
            location: Location,
            path: List[str],
            type_condition: str,
    ):
        super().__init__(path, "Field", location, name)
        # Execution
        self.schema = schema
        self.schema_field = schema_field
        self.arguments = {}
        self.type_condition = type_condition
        self.is_leaf = False
        # Result
        self.results = None
        self.coerced = None
        self.error = None

        self.as_jsonable = {}
        # Meta
        self.in_introspection = (
            True if self.schema_field.name in ["__type", "__schema",
                                               "__typename"] else False
        )

    async def _get_results(self, request_ctx):
        if self.parent and isinstance(self.parent.results, list):
            self.results, self.coerced = await _exec_list(
                self.parent.results,
                self.arguments,
                request_ctx,
                self.path,
                self.location,
                self.schema,
                self.schema_field,
                self,
            )
        else:
            self.results, self.coerced = await self.schema_field.resolver(
                self.parent.results if self.parent else {},
                self.arguments,
                request_ctx,
                Info(
                    query_field=self,
                    schema_field=self.schema_field,
                    schema=self.schema,
                    path=self.path,
                    location=self.location,
                ),
            )

    async def __call__(self, request_ctx) -> GraphQLError:
        await self._get_results(request_ctx)

        def manage_list(par, lii):
            for iii, vvv in enumerate(lii):
                if isinstance(par[iii], list):
                    manage_list(par[iii], vvv)
                else:
                    try:
                        par[iii][self.name] = vvv
                    except TypeError:
                        par[iii] = {self.name: vvv}

        self.error = self.coerced.error
        if self.is_leaf:
            self.as_jsonable = self.coerced.value
        elif isinstance(self.coerced.value, dict) or \
                isinstance(self.coerced.value, list):
            self.as_jsonable = self.coerced.value

        if self.parent and self.parent.in_introspection:
            self.in_introspection = True
            # TODO: Make better error management on instrospection
            self.error = None

        if self.parent:
            if isinstance(self.parent.as_jsonable, list):
                for index, value in enumerate(self.as_jsonable):
                    if isinstance(self.parent.as_jsonable[index], list):
                        manage_list(self.parent.as_jsonable[index], value)
                    else:
                        if not isinstance(self.parent.as_jsonable[index], dict):
                            self.parent.as_jsonable[index] = {}
                        self.parent.as_jsonable[index][self.name] = value
            else:
                if not isinstance(self.parent.as_jsonable, dict):
                    self.parent.as_jsonable = {}
                self.parent.as_jsonable[self.name] = self.as_jsonable

        return self.error
