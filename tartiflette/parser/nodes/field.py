import asyncio
import traceback
from typing import List, Any, Dict

from tartiflette.executors.types import Info, ExecutionContext
from tartiflette.schema import GraphQLSchema
from tartiflette.types.exceptions.tartiflette import InvalidValue
from tartiflette.types.field import GraphQLField
from tartiflette.types.location import Location
from .node import Node


async def default_resolver(parent_result, _arguments, _request_ctx, info: Info):
    try:
        return getattr(
            parent_result, info.schema_field.name
        )
    except AttributeError:
        pass

    try:
        return parent_result[info.schema_field.name]
    except (KeyError, TypeError):
        pass

    return None


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
        self.is_leaf = False  # TODO: Still used ?
        self.info: Info = None
        # Result
        self.result = None
        self.coerced = None
        self.error = None

        self.as_jsonable = {}
        # Meta
        self.in_introspection = (
            True if self.schema_field.name in ["__type", "__schema",
                                               "__typename"] else False
        )

    async def get_result(self, exec_ctx: ExecutionContext,
                         request_ctx: Dict[str, Any]):
        if self.parent and self.parent.error:
            # Parent has error, stop exec.
            self.error = self.parent.error
            return
        self.info = Info(
            query_field=self,
            schema_field=self.schema_field,
            schema=self.schema,
            path=self.path,
            location=self.location,
            execution_ctx=exec_ctx,
        )
        try:
            self.result = await self._get_result(
                self.parent.result if self.parent else None,
                request_ctx,
                self.info)
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            exec_ctx.add_error(e)
            self.error = e

    async def _get_result(self, parent_result: Any,
                          request_ctx: Dict[str, Any], info: Info):
        if isinstance(parent_result, list):
            coroutines = []
            for index, parent_result_item in enumerate(parent_result):
                if isinstance(parent_result_item, list):
                    coroutines.append(
                        self._get_result(
                            parent_result_item,
                            request_ctx,
                            info.clone_with_path(index),
                        )
                    )
                else:
                    resolver = info.schema_field.resolver or default_resolver
                    coroutines.append(
                        resolver(
                            parent_result_item,
                            self.arguments,
                            request_ctx,
                            info.clone_with_path(index),
                        )
                    )
            return await asyncio.gather(*coroutines)
        else:
            resolver = info.schema_field.resolver or default_resolver
            return await resolver(
                parent_result,
                self.arguments,
                request_ctx,
                info.clone(),
            )

    def coerce_result(self):
        if self.error:
            return
        try:
            self.coerced = self._coerce_value(self.result,
                                              self.parent.result if self.parent else None,
                                              self.info)
            return self.coerced
        except Exception as e:
            print(repr(e))
            traceback.print_tb(e.__traceback__)
            self.info.execution_ctx.add_error(e)
            self.error = e

    def _coerce_value(self, current_result: Any, parent_result: Any,
                      info: Info):
        if isinstance(parent_result, list):
            coerced_values = []
            for index, parent_result_item in enumerate(parent_result):
                if isinstance(parent_result_item, list):
                    coerced_values.append(self._coerce_value(
                        current_result[index],
                        parent_result_item,
                        info.clone_with_path(index),
                    ))
                else:
                    coerced_values.append(
                        info.schema_field.gql_type.coerce_value(
                            current_result[index],
                            info.clone(),
                        ))
            return coerced_values
        else:
            return info.schema_field.gql_type.coerce_value(
                current_result,
                info.clone(),
            )

    async def __call__(self, exec_ctx: ExecutionContext,
                      request_ctx: Dict[str, Any]) -> Any:
        # TODO: This should not be called anymore.
        # The above methods are called for trying to coerce
        # values after results calculations.
        self.info = Info(
            query_field=self,
            schema_field=self.schema_field,
            schema=self.schema,
            path=self.path,
            location=self.location,
            execution_ctx=exec_ctx,
        )
        # Parent has error, stop exec.
        if self.parent and self.parent.error:
            self.error = self.parent.error
            return

        try:
            self.result = await self._get_result(
                self.parent.result if self.parent else {},
                request_ctx,
                self.info)
            self.coerced = self._coerce_value(self.result,
                                              self.parent.result if self.parent else {},
                                              self.info)
            self.as_jsonable = self.coerced
        except InvalidValue as e:
            exec_ctx.add_error(e)
            self.error = e
            if self.is_leaf:
                self.as_jsonable = None
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            if self.is_leaf:
                self.as_jsonable = None

        def manage_list(par, lii):
            for iii, vvv in enumerate(lii):
                if isinstance(par[iii], list):
                    manage_list(par[iii], vvv)
                else:
                    try:
                        par[iii][self.name] = vvv
                    except TypeError:
                        par[iii] = {self.name: vvv}

        if self.parent:
            if isinstance(self.parent.as_jsonable, list):
                for index, value in enumerate(self.as_jsonable):
                    if isinstance(self.parent.as_jsonable[index], list):
                        manage_list(self.parent.as_jsonable[index], value)
                    else:
                        self.parent.as_jsonable[index][self.name] = value
            else:
                self.parent.as_jsonable[self.name] = self.as_jsonable
